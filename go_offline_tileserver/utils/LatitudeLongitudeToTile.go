package utils

import (
    "math"
)

func LatitudeLongitudeToTile(longitude, latitude float64, zoom int) (int, int) {
    var x, y float64

    level := float64(zoom)

    x = math.Floor((longitude + 180.0)/360 * math.Pow(2, level))

    y = math.Floor((1 - math.Log(math.Tan(- latitude * math.Pi/180.0) + 1/math.Cos(- latitude * math.Pi/180.0))/math.Pi) * math.Pow(2, level - 1))

    return int(x), int(y)
}
