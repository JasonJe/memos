package main

import (
    "net/http"
    "fmt"
    "os"
    "time"

    flag "github.com/spf13/pflag"
)

var logFile *os.File

type loggingResponseWriter struct {
    http.ResponseWriter
    statusCode int
}

func NewLoggingResponseWriter(w http.ResponseWriter) *loggingResponseWriter {
    return &loggingResponseWriter{w, http.StatusOK}
}
func (lrw *loggingResponseWriter) WriteHeader(code int) {
    lrw.statusCode = code
    lrw.ResponseWriter.WriteHeader(code)
}

func Log(handler http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        lrw := NewLoggingResponseWriter(w)
        handler.ServeHTTP(lrw, r)

        fmt.Fprintf(logFile, "[%s] %s %s [%s] %d\n", time.Now().Format("2006-01-02 15:04:05"), r.RemoteAddr, r.Method, r.URL, lrw.statusCode)
    })
}

func main() {
    flag.Usage = func() {
        fmt.Fprintf(os.Stdout, "Usage: \n")
        flag.PrintDefaults()
    }
    helpPtr := flag.BoolP("help", "h", false, "show this help message and exit")
    bindPtr := flag.StringP("bind", "b", "127.0.0.1", "specify bind address")
    portPtr := flag.StringP("port", "p", "8080", "specify port")
    logPtr  := flag.StringP("log", "l", "stdout", "output log")
    dirPtr  := flag.String("workdir", "./", "specify work dir")

    flag.Parse()
    if *helpPtr {
        flag.Usage()
        return
    }

    var err error  
    if *logPtr != "stdout" {
        logFile, err = os.Create(*logPtr)
        if err != nil {
            fmt.Fprintf(logFile, "Log file create: %s\n", err)
            return
        }
        defer logFile.Close() 
    } else {
        logFile = os.Stdout
    }

    fmt.Fprintf(logFile, "Server bind in %s:%s, work dir is: %s\n", *bindPtr, *portPtr, *dirPtr)
    
    http.Handle("/", http.StripPrefix("/", Log(http.FileServer(http.Dir(*dirPtr)))))
    err = http.ListenAndServe(fmt.Sprintf("%s:%s", *bindPtr, *portPtr), nil)
    if err != nil {
        fmt.Fprintf(logFile, "Server start: %s\n", err)
        return
    }
}
