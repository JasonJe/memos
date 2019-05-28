package main

import (
	"time"
	"fmt"
)

func main() {
	c1 := make(chan string, 1)
	go func() { // 执行一个外部调用，并在 2 秒后 通过通道 c1 返回它的执行结果
		time.Sleep(time.Second * 2)
		c1 <- "result 1"
	}()
	select {
	case res := <- c1:
		fmt.Println(res)
	case <-time.After(time.Second * 1): // 进入超时的case
		fmt.Println("timeout 1")
	}

	c2 := make(chan string, 1)
	go func() {
		time.Sleep(time.Second * 2)
		c2 <- "result 2"
	}()
	select {
	case res:= <-c2: // 未超时，打印 c2
		fmt.Println(res)
	case <-time.After(time.Second * 3):
		fmt.Println("timeout 2")
	}
}