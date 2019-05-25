package main

import "fmt"

func sum(nums ...int) { // 类似python可变参数中的数组参数*args，但是可以扩展变成类似python可变参数的字典参数**kwargs 
	fmt.Println(nums, " ")
	total := 0
	for _, num := range nums {
		total += num
	}
	fmt.Println(total)
}

func main() {
	sum(1, 2)
	sum(1, 2, 3)

	nums := []int{1, 2, 3, 4}
	sum(nums...)
}