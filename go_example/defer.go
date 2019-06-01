package main

import (
	"fmt"
	"os"
)

func main() {
	f := createFile("../defer.txt")
	defer closeFile(f) // 使用 defer 通过 closeFile 来在 writeFile 结束后关闭这个文件
	writeFile(f)
}

func createFile(p string) *os.File {
	fmt.Println("createing")
	f, err := os.Create(p)
	if err != nil {
		panic(err)
	}
	return f
}

func writeFile(f *os.File) {
	fmt.Println("writing")
	fmt.Fprintln(f, "data")
}

func closeFile(f *os.File) {
	fmt.Println("closing")
	f.Close()
}