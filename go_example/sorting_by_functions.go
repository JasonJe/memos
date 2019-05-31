package main

import (
	"sort"
	"fmt"
)


//  sort.Interface 内置了 Len，Less 和 Swap 方法，需要对这三个方法进行重载
type ByLength []string

func (s ByLength) Len() int {
	return len(s)
}
func (s ByLength) Swap(i, j int) {
	s[i], s[j] = s[j], s[i]
}
func (s ByLength) Less(i, j int) bool {
	return len(s[i]) < len(s[j])
}

func main() {
	fruits := []string{"peach", "banan", "kiwi"}
	sort.Sort(ByLength(fruits))
	fmt.Println(fruits)
}