package main

import "fmt"

func f(from string) {
	for i := 0; i< 3; i++ {
		fmt.Println(from, ":", i)
	}
}

func main()  {
	f("direct") // 同步调用

	go func(msg string) { // 匿名函数进行 Go 协程
		fmt.Println(msg)
	}("going")

	go f("goroutine") // 开启 Go 协程，并发执行函数

	fmt.Scanln()
	fmt.Println("done")
}