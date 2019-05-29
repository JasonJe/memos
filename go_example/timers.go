package main

import (
	"time"
	"fmt"
)

func main() {
	timer := time.NewTimer(time.Second * 2)
	
	<- timer.C // 创建一个 Timer，它会在最少过去时间段 d 后到期，向其自身的 C 字段发送当时的时间
	fmt.Println("Timer 1 expired")

	timer2 := time.NewTimer(time.Second)

	go func() {
		<- timer2.C
		fmt.Println("Timer 2 expired")
	}()
	stop2 := timer2.Stop() // 在定时器失效前取消
	if stop2 {
		fmt.Println("Timer 2 stopped")
	}
}