package main

import "fmt"

func main() {
	jobs := make(chan int, 5)
	done := make(chan bool)
	
	go func() {
		for {
			j, more := <- jobs
			if more { //  如果 jobs 已经关闭，并且通道中所有的值都已经接收完毕，那么 more 的值将是 false
				fmt.Println("received job", j)
			} else {
				fmt.Println("received all jobs")
				done <- true
				return
			}
		}
	}()

	for j := 1; j <= 3; j++ {
		jobs <- j
		fmt.Println("send job", j)
	}
	close(jobs) // 使用 close() 关闭通道
	fmt.Println("sent all jobs")
	
	<- done
}