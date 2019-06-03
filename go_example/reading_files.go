package main

import (
	"io"
	"os"
	"fmt"
	"bufio"
	"io/ioutil"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {
	dat, err := ioutil.ReadFile("../dat") // 将文件内容读取到内存中
	check(err)
	fmt.Print(string(dat))

	f, err := os.Open("../dat") // 使用 os.Open 打开一个文件获取一个 os.File 值
	check(err)

	b1 := make([]byte, 5) // 最多读取 5 个字节
	n1, err := f.Read(b1)
	check(err)
	fmt.Printf("%d bytes: %s\n", n1, string(b1))

	o2, err := f.Seek(6, 0) // 可以 Seek 到一个文件中已知的位置并从这个位置开始进行读取
	check(err)
	b2 := make([]byte, 2)
	n2, err := f.Read(b2)
	check(err)
	fmt.Printf("%d bytes @ %d: %s\n", n2, o2, string(b2))

	o3, err := f.Seek(6, 0)
	check(err)
	b3 := make([]byte, 2)
	n3, err := io.ReadAtLeast(f, b3, 2) // 读取可以使用 ReadAtLeast 得到一个更健壮的实现
	check(err)
	fmt.Printf("%d bytes @ %d: %s\n", n3, o3, string(b3))

	_, err = f.Seek(0, 0)
	check(err)

	r4 := bufio.NewReader(f) // 实现了带缓冲的读取，这不仅对于很多小的读取操作能够提升性能，也提供了很多附加的读取函数
	b4, err := r4.Peek(5) // 返回缓存的一个Slice(引用,不是拷贝)，引用缓存中前n字节数据
	check(err)
	fmt.Printf("5 bytes: %s\n", string(b4))

	f.Close()
}