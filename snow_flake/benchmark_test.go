package snowFlake

import (
	"fmt"
	"testing"
)

func BenchmarkSnowFlakeByOneWorker(b *testing.B) {
	worker, err := NewWorker(1)
	if err != nil {
		fmt.Println(err)
		return
	}

	for i := 0; i < b.N; i++ {
		go func() {
			_ = worker.GetId()
		}()
	}
}
