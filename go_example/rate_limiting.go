package main

import (
	"fmt"
	"time"
)

func main() {
	requests := make(chan int, 5)
	for i := 1; i <= 5; i++ {
		requests <- i
	}
	close(requests)

	limiter := time.Tick(time.Millisecond * 200) // 每隔 200 ms 打点一次

	for req := range requests {
		<- limiter // 阻塞 limiter 的一个接受，200ms 进行一次 request
		fmt.Println("request", req, time.Now())
	}

	burstyLimiter := make(chan time.Time, 3) // 进行 3 次临时的脉冲型速率限制
	for i := 0; i < 3; i++ {
		burstyLimiter <- time.Now()
	}
	go func() {
		for t := range time.Tick(time.Millisecond * 200) { // 每 200 ms 添加一个新的值到 burstyLimiter 中
			burstyLimiter <- t
		}
	}()
	burstyRequests := make(chan int, 5) // 模拟超过 5 个的接入请求
	for i := 1; i <= 5; i++ {
		burstyRequests <- i
	}
	close(burstyRequests)
	for req := range burstyRequests {
		<- burstyLimiter // 阻塞，每 200ms 处理一批请求
		fmt.Println("request", req, time.Now())
	}

}