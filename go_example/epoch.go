package main

import (
	"fmt"
	"time"
)

func main() {
	now := time.Now()
	secs := now.Unix()
	nanos := now.UnixNano()
	fmt.Println(now)

	millis := nanos / 1000000 // UnixMillis 不存在，要得到毫秒数的话， 需要自己手动转化一下
	fmt.Println(secs)
	fmt.Println(millis)
	fmt.Println(nanos)

	// 协调世界时起的整数秒或者纳秒转化到相应的时间
	fmt.Println(time.Unix(secs, 0))
	fmt.Println(time.Unix(0, nanos))
}