package main

import (
	"fmt"
	"strconv"
)

func main() {
	f, _ := strconv.ParseFloat("1.234", 64) // 解析浮点数，这里的 64 表示解析的数的位数
	fmt.Println(f)

	i, _ := strconv.ParseInt("123", 0, 64) // 参数 0 表示自动推断字符串所表示的数字的进制。64 表示返回的整型数是以 64 位存储的
	fmt.Println(i)

	d, _ := strconv.ParseInt("0x1c8", 0, 64) // 自动识别出十六进制数
	fmt.Println(d)

	u, _ := strconv.ParseUint("789", 0, 64)
	fmt.Println(u)
	
	k, _ := strconv.Atoi("135") // 基础的 10 进制整型数转换函数
	fmt.Println(k)
	
	_, e := strconv.Atoi("wat")
    fmt.Println(e)
}