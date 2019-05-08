package main

import (
    "os"
    "flag"
    "fmt"
    "strconv"
    "time"
    "sync"
    "runtime"
    // "gopkg.in/mgo.v2"

    "./utils"
    "./config"
)

func Produce(wg *sync.WaitGroup, ch chan<- utils.Coordinate, mintileX, mintileY, maxtileX, maxtileY, zoom int) {
    for X := mintileX; X <= maxtileX; X++ {
        for Y := maxtileY; Y <= mintileY; Y++ {
            ch <- utils.Coordinate{strconv.Itoa(X), strconv.Itoa(Y), strconv.Itoa(zoom)}
            runtime.Gosched()
        }
    }
    wg.Done()
}

func Consumer(wg *sync.WaitGroup, ch <-chan utils.Coordinate, baseurl string) {
    for url := range ch {
        // result := utils.SaveToDB(baseurl, url, db)
        result := utils.SaveImage(baseurl, url)
        if !result {
            fmt.Printf("False Coordinate: %v", url)
        }
        runtime.Gosched()
    }
    wg.Done()
}

// var db *mgo.Database
// var session *mgo.Session

var confpath = "./config/config.ini"
var NewLine = flag.Bool("c", false, "Example: -c /path/to/configfile")

var crawlconfig config.Config

const (
    Space   = " "
    Newline = "\n"
)

func init() {
    runtime.GOMAXPROCS(runtime.NumCPU())
    fmt.Println("[.] Init...")

    flag.Parse()

    var s string = ""
    if !*NewLine {
        fmt.Println("[I] Program startup. Using default config.")
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
        fmt.Println("Program startup.Using config:", confpath)
    }

    err := config.ReadConfig(confpath, &crawlconfig)
    if err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
}

func main() {
    t1 := time.Now()

    // var mhost, mdb string = crawlconfig.MongoDB.DBHost + ":" + crawlconfig.MongoDB.DBPort, crawlconfig.MongoDB.DBName

    var minlon, minlat, maxlon, maxlat float64 = crawlconfig.Map.MinLon, crawlconfig.Map.MinLat, crawlconfig.Map.MaxLon, crawlconfig.Map.MaxLat
    var minzoom, maxzoom int = crawlconfig.Map.MinZoom, crawlconfig.Map.MaxZoom
    var baseurl string = crawlconfig.Map.BaseUrl

    var wgp sync.WaitGroup
    var wgc sync.WaitGroup

    // session, _ = mgo.Dial(mhost)
    // db = session.DB(mdb)

    // Save image in local
    rootpath := "./tilefile/"
    if !utils.PathExist(rootpath) {
        os.Mkdir(rootpath, 0755)
        fmt.Printf("[I] Root dir: %s created\n", rootpath)
    }

    buffersize := 12

    coordinates := make(chan utils.Coordinate, buffersize)

    for i := minzoom; i <= maxzoom; i++ {
        mintileX, mintileY := utils.LatitudeLongitudeToTile(minlon, minlat, i)
        maxtileX, maxtileY := utils.LatitudeLongitudeToTile(maxlon, maxlat, i)
        go Produce(&wgp, coordinates, mintileX, mintileY, maxtileX, maxtileY, i)
        wgp.Add(1)
        for j:= 0; j <= buffersize; j++ {
            go Consumer(&wgc, coordinates, baseurl)
            wgc.Add(1)
        }
    }

    wgp.Wait()
    close(coordinates)
    wgc.Wait()

    elapsed := time.Since(t1)
    fmt.Println("[*] Using time: ", elapsed)
}
