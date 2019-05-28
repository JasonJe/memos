package main

import "fmt"

func main() {
	messages := make(chan string) // make(chan val-type)创建一个新的通道

	go func() {
		messages <- "ping" // channel <- 语法发送(send) 一个新的值到通道中
	}()

	msg := <- messages // <-channel 语法从通道中 接收(receives) 一个值
	fmt.Println(msg)
}