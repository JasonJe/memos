package main

import "os"

func main() {
	panic("a problem") // 产生一个中止程序的运行时错误

	_, err := os.Create("../test")
	if err != nil {
		panic(err)
	}
}