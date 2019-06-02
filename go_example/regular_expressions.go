package main

import (
	"fmt"
	"bytes"
	"regexp"
)

func main() {
	match, _ := regexp.MatchString("p([a-z]+)ch", "peach") // 测试字符串是否符合一个表达式
	fmt.Println(match)

	r, _ := regexp.Compile("p([a-z]+)ch")
	fmt.Println(r.MatchString("peach"))
	fmt.Println(r.FindString("peach punch")) // 查找匹配的字符串
	fmt.Println(r.FindStringIndex("peach punch")) // 查找匹配的开始-结束索引
	fmt.Println(r.FindStringSubmatch("peach punch")) // 返回完全匹配和局部匹配的字符串
	fmt.Println(r.FindStringSubmatchIndex("peach punch")) // 返回完全匹配和局部匹配的索引
	// 带 All 的这个函数返回所有的匹配项，而不仅仅是首次匹配项
	fmt.Println(r.FindAllString("peach punch pinch", -1))
	fmt.Println(r.FindAllStringSubmatchIndex("peach punch pinch", -1))
	fmt.Println(r.FindAllString("peach punch pinch", 2)) // 正整数 2 限制匹配次数

	// 可以提供 []byte 参数并将 String 从函数命中去掉
	fmt.Println(r.Match([]byte("peach")))

	r = regexp.MustCompile("p([a-z]+)ch")
	fmt.Println(r)
	fmt.Println(r.ReplaceAllString("a peach", "<fruit>")) // 字符串替换
	
	in := []byte("a peach")
	out := r.ReplaceAllFunc(in, bytes.ToUpper) // 允许传递匹配内容到一个给定的函数中
	fmt.Println(string(out))
}