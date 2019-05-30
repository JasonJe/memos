package main

import (
	"fmt"
	"math/rand"
	"runtime"
	"sync"
	"sync/atomic"
	"time"
)

func main() {
	var state = make(map[int]int)
	var mutex = &sync.Mutex{} // 定义互斥锁
	var ops int64 = 0

	for r := 0; r < 100; r++ {
		go func() {
			total := 0
			for {
				key := rand.Intn(5)
				mutex.Lock() // 确保对 state 的 独占访问
				total += state[key]
				mutex.Unlock() // 读取选定的键的值，Unlock()
				atomic.AddInt64(&ops, 1)
				runtime.Gosched() // 明确使用 runtime.Gosched() 进行释放 CPU
			}
		}()
	}

	for w := 0; w < 10; w++ { // 运行 10 个 Go 协程来模拟写入操作
		go func() {
			key := rand.Intn(5)
			val := rand.Intn(100)
			mutex.Lock()
			state[key] = val 
			mutex.Unlock()
			atomic.AddInt64(&ops, 1)
			runtime.Gosched()
		}()
	}

	time.Sleep(time.Second)

	opsFinal := atomic.LoadInt64(&ops)
	fmt.Println("ops:", opsFinal)

	mutex.Lock()
	fmt.Println("state:", state)
	mutex.Unlock()
}