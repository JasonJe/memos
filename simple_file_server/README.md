# `Go`实现一个即开即用的文件服务

## 1. 使用说明

```bash
# chmod +x fileServer
# ./fileServer -h
Usage:
  -b, --bind string      specify bind address (default "127.0.0.1")
  -h, --help             show this help message and exit
  -l, --log string       output log (default "stdout")
  -p, --port string      specify port (default "8080")
      --workdir string   specify work dir (default "./")
```

运行`./fileServer`，然后打开浏览器后访问`127.0.0.1:8080`即可。