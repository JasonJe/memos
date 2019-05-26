package main

import "fmt"

func zeroval(ival int) { // 值传递，传入值为值的拷贝
	ival = 0
}

func zeroptr(iptr *int) { // 指针传递，
	*iptr = 0 //  *iptr 解引用指针，从其内存地址得到这个地址对应的当前值，对一个解引用的指针赋值将会改变这个指针引用的真实地址的值
}

func main() {
	i := 1
	fmt.Println("initial:", i)

	zeroval(i)
	fmt.Println("zeroval:", i)

	zeroptr(&i) // &i 语法来取得 i 的内存地址，即指向 i 的指针
	fmt.Println("zeroptr:", i)

	fmt.Println("pointer:", &i)
}