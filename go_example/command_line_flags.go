package main

import (
	"fmt"
	"flag"
)

func main() {
	// 基本的标记声明仅支持字符串、整数和布尔值选项
	// 第一个参数为标志，第二个参数为默认值，第三个参数为简短的描述
	wordPtr := flag.String("word", "foo", "a string")
	numbPtr := flag.Int("numb", 42, "an int")
	boolPtr := flag.Bool("fork", false, "a bool")

	// 用程序中已有的参数来声明一个标志也是可以的
	// 注意在标志声明函数中需要使用该参数的指针
	var svar string
	flag.StringVar(&svar, "svar", "bar", "a string var")
	flag.Parse()

	// 使用类似 *wordPtr 这样的语法来对指针解引用，从而得到选项的实际值
	fmt.Println("word:", *wordPtr)
	fmt.Println("numb:", *numbPtr)
	fmt.Println("fork:", *boolPtr)
	fmt.Println("svar:", svar)
	fmt.Println("tail:", flag.Args())
}