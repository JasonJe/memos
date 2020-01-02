# `SnowFlake` 算法实现

## 使用方法

```go
package main

import (
	"fmt"

	snowFlake "github.com/JasonJe/memos/snow_flake"

	"github.com/imroc/biu"
)

func main() {
	worker, err := snowFlake.NewWorker(5)

	if err != nil {
		fmt.Println(err)
	}
	ID := worker.GetId()
	fmt.Println(ID)
	fmt.Println(biu.ToBinaryString(ID))
}
```
