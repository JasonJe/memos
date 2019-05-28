package main

import "fmt"

func ping(pings chan <- string, msg string){ // 定义一个值允许发送数据的通道
	pings <- msg
}

func pong(pings <- chan string, pongs chan<- string) { // 接收 pings 的数据，使用 pongs 发送数据
	msg := <-pings
	pongs <- msg
}

func main() {
	pings := make(chan string, 1)
	pongs := make(chan string, 1)
	ping(pings, "passed message")
	pong(pings, pongs)
	fmt.Println(<-pongs)
}