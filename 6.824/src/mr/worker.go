package mr

import "os"
import "fmt"
import "log"
import "io/ioutil"
import "strings"
import "sort"
import "net/rpc"
import "hash/fnv"
import "strconv"


//
// Map functions return a slice of KeyValue.
//
type KeyValue struct {
	Key   string
	Value string
}

//for sorting 
type ByKey []KeyValue
func (a ByKey) Len() int           { return len(a) }
func (a ByKey) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }
func (a ByKey) Less(i, j int) bool { return a[i].Key < a[j].Key }

//
// use ihash(key) % NReduce to choose the reduce
// task number for each KeyValue emitted by Map.
//
func ihash(key string) int {
	h := fnv.New32a()
	h.Write([]byte(key))
	return int(h.Sum32() & 0x7fffffff)
}


//
// main/mrworker.go calls this function.
//
func Worker(mapf func(string, string) []KeyValue,
	reducef func(string, []string) string) {
    id := strconv.Itoa(os.Getpid())
    fmt.Println("worker %s started", id)

	// Your worker implementation here.
    var lastTaskType string
    var lastTaskIndex int
    var tempofilename string
    for {
        args := ApplyForTaskArgs{
            WorkerID:       id,
            LastTaskType:   lastTaskType,
            LastTaskIndex:  lastTaskIndex,
        }
        reply := ApplyForTaskReply{}
        ok := call("Coordinator.ApplyForTask", &args, &reply)
        if !ok {
            fmt.Println("Call failed")
        }
        if reply.TaskType == "" {
            //mr task finished
            fmt.Println("MR task finished")
            break
        }

        fmt.Println("Received %s task %d from coordinator", reply.TaskType, reply.TaskIndex)
        if reply.TaskType == "Map" {
                file, _ := os.Open(reply.MapInputFile)
                content, _ := ioutil.ReadAll(file)

                kva := mapf(reply.MapInputFile, string(content))
                hashedkva := make(map[int][]KeyValue)
                for _, kv := range kva {
                    hashed := ihash(kv.Key) % reply.nReduce
                    hashedkva[hashed] = append(hashedkva[hashed], kv)
                }

                for i:=0; i<reply.nReduce; i++ {
                    tmpfilename := "maptemp-"+strconv.Itoa(reply.TaskIndex)+"-"+strconv.Itoa(i)
                    ofile, _ := os.Create(tmpfilename)
                    for _, kv := range hashedkva[i]{
                        fmt.Fprintf(ofile, "%v\t%v\n", kv.Key, kv.Value)
                    }
                }
        } else if reply.TaskType == "Reduce" {
            var lines []string
            for i:=0; i<=reply.nMap; i++ {
                inputFile := "map-"+strconv.Itoa(i)+"-"+strconv.Itoa(reply.TaskIndex)
                file, _ := os.Open(inputFile)
                content, _ := ioutil.ReadAll(file)

                lines = append(lines, strings.Split(string(content), "\n")...)
            }
            var kva []KeyValue
            for _, line := range lines{
                parts := strings.Split(line, "\t")
                kva = append(kva, KeyValue{Key: parts[0], Value: parts[1]})
            }
            sort.Sort(ByKey(kva))
            tempofilename = "reducetemp-"+strconv.Itoa(reply.TaskIndex)
            ofile, _  := os.Create(tempofilename)
            i := 0
            for i < len(kva) {
                j := i + 1
                for j < len(kva) && kva[j].Key == kva[i].Key {
                    j++
                }
                var values []string
                for k := i; k < j; k++ {
                    values = append(values, kva[k].Value)
                }
                output := reducef(kva[i].Key, values)
                fmt.Fprintf(ofile, "%v %v\n", output)
                i = j
            }
            ofile.Close()
          }
          lastTaskType = reply.TaskType
          lastTaskIndex = reply.TaskIndex
          fmt.Println("Finished %s task %d", reply.TaskType, reply.TaskIndex)
    }
    // uncomment to send the Example RPC to the coordinator.
	// CallExample()
}


//
// example function to show how to make an RPC call to the coordinator.
//
// the RPC argument and reply types are defined in rpc.go.
//
func CallExample() {

	// declare an argument structure.
	args := ExampleArgs{}

	// fill in the argument(s).
	args.X = 99

	// declare a reply structure.
	reply := ExampleReply{}

	// send the RPC request, wait for the reply.
	// the "Coordinator.Example" tells the
	// receiving server that we'd like to call
	// the Example() method of struct Coordinator.
	ok := call("Coordinator.Example", &args, &reply)
	if ok {
		// reply.Y should be 100.
		fmt.Println("reply.Y %v\n", reply.Y)
	} else {
		fmt.Println("call failed!\n")
	}
}

//
// send an RPC request to the coordinator, wait for the response.
// usually returns true.
// returns false if something goes wrong.
//
func call(rpcname string, args interface{}, reply interface{}) bool {
	// c, err := rpc.DialHTTP("tcp", "127.0.0.1"+":1234")
	sockname := coordinatorSock()
	c, err := rpc.DialHTTP("unix", sockname)
	if err != nil {
		log.Fatal("dialing:", err)
	}
	defer c.Close()

	err = c.Call(rpcname, args, reply)
	if err == nil {
		return true
	}

	fmt.Println(err)
	return false
}
