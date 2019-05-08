package config

import (
    "fmt"
    "gopkg.in/gcfg.v1"
)

type Config struct {
    MongoDB struct {
        DBHost, DBPort, DBName string
    }
    Map struct {
        BaseUrl string
        MinLon, MinLat, MaxLon, MaxLat float64
        MinZoom, MaxZoom int
    }
    Redis struct {
        RDHost, RDPort, RDPassword string
        RDDB int
    }
}

func ReadConfig(path string, config *Config) (error) {
    err := gcfg.ReadFileInto(config, path)
    if err != nil {
        fmt.Println(err)
        return err
    }
    return nil
}
