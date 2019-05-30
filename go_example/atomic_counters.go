package main

import (
	"fmt"
	"time"
	"runtime"
	"sync/atomic"
)

func main() {
	var ops uint64 = 0

	for i := 0; i < 50; i++ { // 模拟并发更新
		go func() {
			atomic.AddUint64(&ops, 1) // 计数器自增，传入内存地址进行
			runtime.Gosched()
		}()
	}

	time.Sleep(time.Second)

	opsFinal := atomic.LoadUint64(&ops) // 为了在计数器还在被其它 Go 协程更新时，安全的使用它，通过 LoadUint64 将当前值的拷贝提取到 opsFinal 中
	fmt.Println("ops:", opsFinal)
}