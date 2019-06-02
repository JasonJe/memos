package main

import (
	"fmt"
	"encoding/base64"
)

func main() {
	data := "abc123!?$*&()'-=@~"

	sEnc := base64.StdEncoding.EncodeToString([]byte(data)) // 编码需要 使用 []byte 类型的参数
	fmt.Println(sEnc)
	
	sDec, _ := base64.StdEncoding.DecodeString(sEnc)
    fmt.Println(string(sDec))
	fmt.Println()
	
	// 使用 URL 兼容的 base64 格式进行编解码
	uEnc := base64.URLEncoding.EncodeToString([]byte(data))
    fmt.Println(uEnc)
    uDec, _ := base64.URLEncoding.DecodeString(uEnc)
	fmt.Println(string(uDec))
	
	// 标准 base64 编码和 URL 兼容 base64 编码的编码字符串存在 稍许不同（后缀为 + 和 -），但是两者都可以正确解码为 原始字符串
}