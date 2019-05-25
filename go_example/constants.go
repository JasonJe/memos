package main

import (
	"fmt"
	"math"
)

const s string = "constant"

func main() {
	fmt.Println(s)

	const n = 500000000

	const d = 3e20 / n
	fmt.Println(d)
	fmt.Println(int64(d)) // 数值型常量没有确定的类型，直到被给定

	fmt.Println(math.Sin(n))
}