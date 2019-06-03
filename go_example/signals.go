package main

import (
	"os"
	"fmt"
	"syscall"
	"os/signal"
)

func main() {
	sigs := make(chan os.Signal, 1)
	done := make(chan bool, 1)

	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM) // 通过向一个通道发送 os.Signal 值来进行信号通知，注册这个给定的通道用于接收特定信号

	go func() { // 程序将在这里进行等待，直到它得到了期望的信号
		sig := <- sigs
		fmt.Println()
		fmt.Println(sig)
		done <- true
	}()

	fmt.Println("awaiting signal")
	<- done
	fmt.Println("exiting")
}