package main

import (
	"bufio"
    "fmt"
    "os"
    "strings"
)

func main() {
	// 对 os.Stdin 使用一个带缓冲的 scanner，可以直接使用方便的 Scan 方法来直接读取一行，每次调用该方法可以让 scanner 读取下一行
	scanner := bufio.NewScanner(os.Stdin)

	for scanner.Scan() {
		ucl := strings.ToUpper(scanner.Text())
		fmt.Println(ucl)
	}

	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, "error", err)
		os.Exit(1)
	}
}