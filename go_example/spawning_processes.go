package main

import (
	"fmt"
	"io/ioutil"
	"os/exec"
)

func main()  {
	dateCmd := exec.Command("date") // exec.Command 创建一个表示外部进程的对象
	dateOut, err := dateCmd.Output() // 处理运行一个命令
	if err != nil {
		panic(err)
	}
	fmt.Println("> date")
	fmt.Println(string(dateOut))

	grepCmd := exec.Command("grep", "hello")
	grepIn, _ := grepCmd.StdinPipe() // 明确的获取输入管道
	grepOut, _ := grepCmd.StdoutPipe() // 明确的获取输出管道
	grepCmd.Start()
	grepIn.Write([]byte("hello grep\ngoodbye grep"))
	grepIn.Close()

	grepBytes, _ := ioutil.ReadAll(grepOut)
	grepCmd.Wait()
	fmt.Println("> grep hello")
	fmt.Println(string(grepBytes))

	lsCmd := exec.Command("bash", "-c", "ls -a -l -h")
	lsOut, err := lsCmd.Output()
	if err != nil {
		panic(err)
	}
	fmt.Println("> ls -a -l -h")
	fmt.Println(string(lsOut))
}