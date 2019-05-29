package main

import (
	"fmt"
	"time"
)

func worker(id int, jobs <- chan int, result chan <- int) {
	for j := range jobs {
		fmt.Println("worker", id, "processing job", j)
		time.Sleep(time.Second)
		result <- j * 2
	}
}

func main() {
	jobs := make(chan int, 100)
	results := make(chan int, 100)

	for w := 1; w <= 3; w++ { // 启动 3 个 worker，3 个 worker 并行执行
		go worker(w, jobs, results)
	}

	for j := 1; j <= 9; j++ { // 9 个任务被执行，任务执行 3 秒，不是 9 秒
		jobs <- j
	}
	close(jobs)

	for a := 1; a <= 9; a++ {
		msg := <- results
		fmt.Println(msg)
	}
}