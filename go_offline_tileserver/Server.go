package main

import (
    "os"
    "log"
    "fmt"
    "flag"
    "runtime"
    "net/http"

    "gopkg.in/mgo.v2"
    "github.com/go-redis/redis"
    "github.com/NYTimes/gziphandler"

    "./utils"
    "./config"
)

var session *mgo.Session
var db *mgo.Database
var redisclient *redis.Client

var confpath = "config/config.ini"
var NewLine = flag.Bool("c", false, "Example: -c /path/to/configfile")

var serverconfig config.Config

const (
    Space   = " "
    Newline = "\n"
)

func init() {
    flag.Parse()

    var s string = ""
    if !*NewLine {
        log.Println("[*]", os.Getpid(), "Program startup. Using default config.")
    } else {
        for i := 0; i < flag.NArg(); i++ {
            if i > 0 {
                s += " "
                if *NewLine {
                    s += Newline
                }
            }
            s += flag.Arg(i)
        }
        confpath = s
        log.Println("Program startup.Using config:", confpath)
    }

    err := config.ReadConfig(confpath, &serverconfig)
    if err != nil {
        log.Println("[E]", "config init error")
        os.Exit(1)
    }

    log.Printf("[.] %d MongoDB Addr: %s, MongoDB DB: %s, Redis Addr: %s\n", os.Getpid(), serverconfig.MongoDB.DBHost + ":" + serverconfig.MongoDB.DBPort, serverconfig.MongoDB.DBName, serverconfig.Redis.RDHost + ":" + serverconfig.Redis.RDPort)

    var maddr, mdb string = serverconfig.MongoDB.DBHost + ":" + serverconfig.MongoDB.DBPort, serverconfig.MongoDB.DBName

    session, _ = mgo.Dial(maddr)
    session.SetMode(mgo.Eventual, true)
    db = session.DB(mdb)

    var rdaddr, rdpassword string = serverconfig.Redis.RDHost + ":" + serverconfig.Redis.RDPort, serverconfig.Redis.RDPassword
    var rddb int = serverconfig.Redis.RDDB

    redisclient = utils.CreateClient(rdaddr, rdpassword, rddb)
}

func TileHandler(w http.ResponseWriter, r *http.Request, x, y, z string) {
    w.Header().Set("Content-Type", "image/png")
    w.Header().Set("Cache-Control", "max-age=3600")

    filename := fmt.Sprintf("%s_%s.png", x, y)

    if utils.HashExists(redisclient, z, filename) {
        log.Println("[I]", os.Getpid(), r.RemoteAddr, r.Method, r.Proto, r.URL, 200)
        redisbyte := []byte(utils.HashGet(redisclient, z, filename))

        w.WriteHeader(200)
        _, err := w.Write(redisbyte)
        if err !=nil {
            log.Println("[E]", os.Getpid(), r.RemoteAddr, r.Method, r.Proto, r.URL, "write to response error", err, 500)
            w.WriteHeader(500)
            return
        }
    } else {
        log.Println("[I]", os.Getpid(), r.RemoteAddr, r.Method, r.Proto, r.URL, 201)
        c := db.GridFS(z)

        file, err := c.Open(filename)
        if err !=nil {
            log.Println("[E]", os.Getpid(), r.RemoteAddr, r.Method, r.Proto, r.URL, "file error", file, err, 500)
            return
        }

        dataBytes := make([]byte, file.Size())
        written, err := file.Read(dataBytes)
        if err !=nil {
            log.Println("[E]", os.Getpid(), r.RemoteAddr, r.Method, r.Proto, r.URL, "load binary error", written, err, 500)
            return
        }
        defer file.Close()

        utils.HashAdd(redisclient, z, filename, dataBytes)

        _, err = w.Write(dataBytes)
        w.WriteHeader(200)
        if err !=nil {
            log.Println("[E]", os.Getpid(), r.RemoteAddr, r.Method, r.Proto, r.URL, "write to response error", err, 500)
            w.WriteHeader(500)
            return
        }
    }
}

func TileServer(w http.ResponseWriter, r *http.Request) {
    r.ParseForm()
    if len(r.Form) == 0 {
        log.Println("[E]", os.Getpid(), r.RemoteAddr, r.Method, r.Proto, r.URL, "Missing parse", 500)
        w.WriteHeader(500)
    } else if r.Method != "GET" {
        log.Println("[E]", os.Getpid(), r.RemoteAddr, r.Method, r.Proto, r.URL, "Missing parse", 500)
        w.WriteHeader(501)
    } else {
        x, y, z := r.Form["x"][0], r.Form["y"][0], r.Form["z"][0]
        TileHandler(w, r, x, y, z)
    }
}

func main() {
    runtime.GOMAXPROCS(runtime.NumCPU())
    TileServer := http.HandlerFunc(TileServer)

	withGz := gziphandler.GzipHandler(TileServer)
    http.Handle("/", withGz)

    // http.HandleFunc("/", TileServer)

    err := http.ListenAndServe(":7777", nil)
    if err != nil {
        log.Fatal("ListenAndServe: ", err)
    }
}
