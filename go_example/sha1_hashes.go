package main

import (
	"crypto/sha1"
	"fmt"
)

func main() {
	s := "sha1 this string"

	// 产生一个散列值
	h := sha1.New()
	h.Write([]byte(s)) // 得到最终的散列值的字符切片
	bs := h.Sum(nil) // 给现有的字符切片追加额外的字节切片

	fmt.Println(s)
	fmt.Printf("%x\n", bs) // 以可读 16 进制格式输出
}