package snowFlake

import (
	"errors"
	"sync"
	"time"
)

// -1 的二进制为 [11111111 11111111 11111111 11111111 11111111 11111111 11111111 11111111]
// (-1 << 10) 结果为 [11111111 11111111 11111111 11111111 11111111 11111111 11111100 00000000]
// -1 ^ (-1 << 10) 结果为 [00000000 00000000 00000000 00000000 00000000 00000000 00000011 11111111]，十进制为 1023

const (
	workerBits   uint8 = 10
	numberBits   uint8 = 12
	maxWorker    int64 = -1 ^ (-1 << workerBits) // 使用位运算，防止溢出, 1023
	maxNumber    int64 = -1 ^ (-1 << numberBits) // 4095
	timeOffset   uint8 = workerBits + numberBits //
	workerOffset uint8 = numberBits
	startEpoch   int64 = 1577932132000
)

type Worker struct {
	mu        sync.Mutex
	timestamp int64
	workerId  int64
	number    int64
}

func NewWorker(workerId int64) (*Worker, error) {
	if workerId < 0 || workerId > maxWorker {
		return nil, errors.New("Worker ID excess of quantity")
	}
	return &Worker{
		timestamp: 0,
		workerId:  workerId,
		number:    0}, nil
}

func (w *Worker) GetId() int64 {
	w.mu.Lock()
	defer w.mu.Unlock()

	now := time.Now().UnixNano()
	if w.timestamp == now {
		w.number++
		if w.number > maxNumber {
			for now <= w.timestamp {
				now = time.Now().UnixNano() / 1e6
			}
		}
	} else {
		w.number = 0
		w.timestamp = now
	}

	ID := int64((now-startEpoch)<<timeOffset | (w.workerId << workerOffset) | (w.number)) //
	return ID
}
