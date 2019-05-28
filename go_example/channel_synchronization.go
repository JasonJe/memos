package main

import (
	"fmt"
	"time"
)

func worker(done chan bool)  { // done 通道 将被用于通知其他 Go 协程这个函数已经工作完毕
	fmt.Println("working...")
	time.Sleep(time.Second)
	fmt.Println("done")

	done <- true
}

func main() {
	done := make(chan bool, 1)
	go worker(done)

	<- done
}