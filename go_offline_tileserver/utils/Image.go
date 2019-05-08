package utils

import (
    "fmt"
    "io"
    "os"
    "time"
    "net/http"
    "gopkg.in/mgo.v2"
    "gopkg.in/mgo.v2/bson"
)

type Coordinate struct {
    X, Y, Z string
}

func PathExist(path string) bool {
    p, err := os.Stat(path)
    if err != nil {
        return os.IsExist(err)
    } else {
        return p.IsDir()
    }
}

type Tile struct {
    Id_ bson.ObjectId   `bson:"_id"`
    ChunkSize   int `bson:"chunkSize"`
    UploadDate  time.Time   `bson:"uploadDate"`
    Length  int `bson:"length"`
    Md5 string  `bson:"md5"`
    FileName    string  `bson:"filename"`
}

func SaveImage(baseurl string, coordinate Coordinate) bool {
    savepath := fmt.Sprintf("./tilefile/%s/", coordinate.Z)
    if !PathExist(savepath) {
        os.Mkdir(savepath, 0755)
        fmt.Printf("[I] Dir %s created\n", savepath)
    }

    filename := fmt.Sprintf("%s_%s.png", coordinate.X, coordinate.Y)

    filepath, err := os.Create(savepath + filename)
    if err != nil {
        fmt.Println(err)
        return false
    }

    url := fmt.Sprintf(baseurl, coordinate.X, coordinate.Y, coordinate.Z)

    response, err := http.Get(url)
    if err != nil {
        fmt.Println(err)
        return false
    }
    fmt.Println("[I] Get url: ", os.Getpid(), url, response.StatusCode)

    defer response.Body.Close()

    io.Copy(filepath, response.Body)
    return true
}

func SaveToDB(baseurl string, coordinate Coordinate, db *mgo.Database) bool {
    filename := fmt.Sprintf("%s_%s.png", coordinate.X, coordinate.Y)
    c := db.GridFS(coordinate.Z)

    var tile Tile
    c.Find(bson.M{"filename": filename}).One(&tile)

    if tile.FileName == "" {
        url := fmt.Sprintf(baseurl, coordinate.X, coordinate.Y, coordinate.Z)

        response, err := http.Get(url)
        if err != nil {
            fmt.Println(err)
            return false
        }
        fmt.Println("[I] Get url: ", os.Getpid(), url, response.StatusCode)

        defer response.Body.Close()

        mongofile, err := c.Create(filename)
        if err != nil {
            fmt.Println(err)
            return false
        }

        written, err := io.Copy(mongofile, response.Body)
        fmt.Println("Written: ", written)
        if err != nil {
            fmt.Println(err)
            return false
        }

        err = mongofile.Close()
        if err != nil {
            fmt.Println(err)
            return false
        }
    } else {
        fmt.Println("File exist: ", filename)
    }

    return true
}

func RestoreImage(x, y, z, savepath string, db *mgo.Database) {
    filename := fmt.Sprintf("%s_%s.png", x, y)
    c := db.GridFS(z)

    file, err := c.Open(filename)
    if err !=nil {
        fmt.Println(err)
        return
    }

    savepath = fmt.Sprintf(savepath + "%s/", z)
    if !PathExist(savepath) {
        os.Mkdir(savepath, 0755)
        fmt.Printf("[I] Dir %s created\n", savepath)
    }

    filepath := fmt.Sprintf(savepath + "%s", filename)
    fmt.Println(filepath)

    out, _ := os.OpenFile(filepath, os.O_CREATE|os.O_WRONLY, 0666)
    _, err = io.Copy(out, file)
    if err !=nil {
        fmt.Println(err)
        return
    }

    err = file.Close()
    if err !=nil {
        fmt.Println(err)
        return
    }
}
