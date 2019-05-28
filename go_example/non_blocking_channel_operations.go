package main

import "fmt"

// 带一个 default 子句的 select 来实现非阻塞 的 发送、接收，甚至是非阻塞的多路 select
// https://www.jianshu.com/p/52fb12d17399
func main() {
	messages := make(chan string)
	signals := make(chan bool)

	select {
	case msg := <- messages:
		fmt.Println("received message", msg)
	default:
		fmt.Println("no messages reveived")
	}

	msg := "hi"
	select {
	case messages <- msg:
		fmt.Println("send message", msg)
	default:
		fmt.Println("np message sent")
	}

	select {
	case msg := <- messages:
		fmt.Println("received message", msg)
	case sig:= <-signals:
		fmt.Println("received signal", sig)
	default:
		fmt.Println("no activity")
	}
}