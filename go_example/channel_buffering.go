package main

import "fmt"

func main() {
	messages := make(chan string, 2) // 最多允许缓存 2 个值
	
	messages <- "buffered"
	messages <- "channel"

	fmt.Println(<-messages)
	fmt.Println(<-messages)
}