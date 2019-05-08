package utils

import (
    "fmt"
    "time"
    "github.com/go-redis/redis"
)

const lifetime time.Duration = 1e9 * 60 * 60 * 24

func CreateClient(addr, password string, dbname int) *redis.Client {
    client := redis.NewClient(&redis.Options{
        Addr: addr,
        Password: password,
        DB: dbname,
    })
    pong, err := client.Ping().Result()
    if err != nil {
        fmt.Println(pong, err)
    }
    return client
}

func HashAdd(client *redis.Client, hashName, hashKey string, hashValue interface{}) {
    client.HSet(hashName, hashKey, hashValue)
    client.Expire(hashName, lifetime)
}

func HashExists(client *redis.Client, hashName, hashKey string) bool {
    return client.HExists(hashName, hashKey).Val()
}

func HashGet(client *redis.Client, hashName, hashKey string) string {
    return client.HGet(hashName, hashKey).Val()
}
