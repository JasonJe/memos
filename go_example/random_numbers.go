package main

import (
	"fmt"
	"time"
	"math/rand"
)

func main() {
	fmt.Print(rand.Intn(100), ",") // 返回一个随机的整数 n，0 <= n <= 100
	fmt.Print(rand.Intn(100))
	fmt.Println()

	fmt.Println(rand.Float64())
	fmt.Print((rand.Float64() * 5) + 5, ",")
	fmt.Print((rand.Float64() * 5) + 5)
	fmt.Println()

	s1 := rand.NewSource(time.Now().UnixNano())
	r1 := rand.New(s1)
	fmt.Print(r1.Intn(100), ",")
	fmt.Print(r1.Intn(100))
	fmt.Println()

	// 默认情况下，给定的种子是确定的，每次都会产生相同的随机数数字序列。要产生变化的序列，需要给定一个变化的种子。
	// 需要注意的是，如果你出于加密目的，需要使用随机数的话，请使用 crypto/rand 包， 此方法不够安全。
	s2 := rand.NewSource(42)
	r2 := rand.New(s2)
	fmt.Print(r2.Intn(100), ",")
	fmt.Print(r2.Intn(100))
	fmt.Println()

	s3 := rand.NewSource(42)
	r3 := rand.New(s3)
	fmt.Print(r3.Intn(100), ",")
	fmt.Print(r3.Intn(100))
}