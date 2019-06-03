package main

import (
    "bufio"
    "fmt"
    "io/ioutil"
    "os"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {
	d1 := []byte("hello\ngo\n")
	err := ioutil.WriteFile("../dat", d1, 0644) // 写入一个字符串（或者只是一些 字节）到一个文件
	check(err)

	f, err := os.Create("../dat") // 打开一个文件
	check(err)
	defer f.Close() //  defer 调用文件的 Close 操作

	d2 := []byte{115, 111, 109, 101, 10}
	n2, err := f.Write(d2)
	check(err)
	fmt.Printf("wrote %d bytes\n", n2)

	n3, err := f.WriteString("writes\n")
	fmt.Printf("wrote %d bytes\n", n3)

	f.Sync() // 调用 Sync 来将缓冲区的信息写入磁盘

	w := bufio.NewWriter(f)
	n4, err := w.WriteString("buffered\n")
	fmt.Printf("wrote %d bytes\n", n4)
	w.Flush() // 使用 Flush 来确保所有缓存的操作已写入底层写入器
}