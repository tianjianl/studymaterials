package mr

//
// RPC definitions.
//
// remember to capitalize all names.
//

import "os"
import "strconv"
import "time"
//
// example to show how to declare the arguments
// and reply for an RPC.
//

type ExampleArgs struct {
	X int
}

type ExampleReply struct {
	Y int
}

// Add your RPC definitions here
type ApplyForTaskArgs struct{
    LastTaskType string
    LastTaskIndex int
    WorkerID string
}

type Task struct {
    Type string
    Index int
    WorkerID string
    MapInputFile string
    Deadline time.Time
}
type ApplyForTaskReply struct {
    TaskType string
    TaskIndex int
    MapInputFile string
    nMap int
    nReduce int
}
// Cook up a unique-ish UNIX-domain socket name
// in /var/tmp, for the coordinator.
// Can't use the current directory since
// Athena AFS doesn't support UNIX-domain sockets.
func coordinatorSock() string {
	s := "/var/tmp/824-mr-"
	s += strconv.Itoa(os.Getuid())
	return s
}
