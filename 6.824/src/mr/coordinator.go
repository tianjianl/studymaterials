package mr

import "log"
import "net"
import "os"
import "net/rpc"
import "net/http"
import "strconv"
import "sync"
import "fmt"
import "time"
import "math"

type Coordinator struct {
	// Your definitions here.
    lock sync.Mutex

    now string // now = Map/Reduce
    nMap int
    nReduce int
    tasks map[string]Task
    unfinishedtasks chan Task
}

// Your code here -- RPC handlers for the worker to call.

//
// an example RPC handler.
//
// the RPC argument and reply types are defined in rpc.go.
//
func (c *Coordinator) Example(args *ExampleArgs, reply *ExampleReply) error {
	reply.Y = args.X + 1
	return nil
}

func (c *Coordinator) ApplyForTask(args *ApplyForTaskArgs, reply *ApplyForTaskReply) error {

    if args.LastTaskType != "" {
        c.lock.Lock()
        LastTaskName := args.LastTaskType + "-" + strconv.Itoa(args.LastTaskIndex)
        var temp, final, rtemp, rfinal, taskid string
        if task, exists := c.tasks[LastTaskName]; exists && task.WorkerID == args.WorkerID {
            if args.LastTaskType == "Map"{
                //for each of nReduce temp map output files, rename them into final map output files
                for i := 0; i < c.nReduce; i++ {
                    temp = "maptemp-"+strconv.Itoa(args.LastTaskIndex)+"-"+strconv.Itoa(i)
                    final = "map-"+strconv.Itoa(args.LastTaskIndex)+"-"+strconv.Itoa(i)
                    err := os.Rename(temp, final)
                    if err != nil {
                        log.Fatalf("Failed to rename map file to %s, error is %e", final, err)
                    }
                }
            } else if args.LastTaskType == "Reduce" {
                //rename the temp reduce file(last task index) into final output file  
                rtemp  = "reducetemp-"+strconv.Itoa(args.LastTaskIndex)
                rfinal = "mr-out-"+strconv.Itoa(args.LastTaskIndex)
                err := os.Rename(rtemp, rfinal)
                if err != nil {
                    log.Fatalf("Failed to rename reduce file to %s, error is %e", rfinal, err)
                }
            }
        }
        delete(c.tasks, LastTaskName)

        //
        if len(c.tasks) == 0 {
            if c.now == "Map" {
                //c.now = "Reduce"
                c.now = "Reduce"
                //generate nReduce reduce tasks into c and
                for i := 0; i < c.nReduce; i++ {
                    task := Task{
                        Type: "Reduce",
                        Index: i,
                    }
                    taskid = "Reduce-"+strconv.Itoa(i)
                    c.tasks[taskid] = task
                    c.unfinishedtasks <- task
                }

            } else if c.now == "Reduce" {
                fmt.Println("Finished all reduce tasks")
                close(c.unfinishedtasks)
                c.now = ""
            }
        }
        c.lock.Unlock()
    }
    //get a new task from unfinished tasks and write it into the reply 
    task, ok := <-c.unfinishedtasks
    if !ok { //ALl tasks finished
        return nil
    }
    c.lock.Lock()
    defer c.lock.Unlock()
    task.WorkerID = args.WorkerID
    task.Deadline = time.Now().Add(10 * time.Second)
    taskname := task.Type + "-" + strconv.Itoa(task.Index)
    c.tasks[taskname] = task
    reply.TaskType = task.Type
    reply.TaskIndex = task.Index
    reply.MapInputFile = task.MapInputFile
    reply.nMap = c.nMap
    reply.nReduce = c.nReduce
    return nil
}

//
// start a thread that listens for RPCs from worker.go
//
func (c *Coordinator) server() {
	rpc.Register(c)
	rpc.HandleHTTP()
	//l, e := net.Listen("tcp", ":1234")
	sockname := coordinatorSock()
	os.Remove(sockname)
	l, e := net.Listen("unix", sockname)
	if e != nil {
		log.Fatal("listen error:", e)
	}
	go http.Serve(l, nil)
}

//
// main/mrcoordinator.go calls Done() periodically to find out
// if the entire job has finished.
//
func (c *Coordinator) Done() bool {
	ret := false
	// Your code here.
	c.lock.Lock()
    defer c.lock.Unlock()
    if c.now == "" {
        ret = true
    }
    return ret
}

//
// create a Coordinator.
// main/mrcoordinator.go calls this function.
// nReduce is the number of reduce tasks to use.
//
func MakeCoordinator(files []string, nReduce int) *Coordinator {
    c := Coordinator{
        now: "Map",
        nMap: len(files),
        nReduce: nReduce,
        tasks: make(map[string]Task),
        unfinishedtasks: make(chan Task, int(math.Max(float64(len(files)), float64(nReduce)))),
    }
	// Your code here.
    // Generate one map task for each file 
    var taskname string
    for index, file := range files {
        task := Task{
            Type: "Map",
            Index: index,
            MapInputFile: file,
        }
        taskname = "Map-"+strconv.Itoa(index)
        c.tasks[taskname] = task
        c.unfinishedtasks <- task
    }
    fmt.Println("Coordinator launched")
    //find workers that did not finished the task before the deadline and reassign
    go func() {
        for {
            time.Sleep(1000 * time.Millisecond)

            c.lock.Lock()
            for _, task := range c.tasks {
                if task.WorkerID != "" && time.Now().After(task.Deadline) {
                    fmt.Println("found task",task.Index,"past deadline, recycling it")
                    task.WorkerID = ""
                    c.unfinishedtasks <- task

                }
            }
            c.lock.Unlock()

        }
    }()
    c.server()
	return &c
}
