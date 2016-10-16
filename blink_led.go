package main

import (
    "fmt"
    "os"
    "time"
    "github.com/stianeikeland/go-rpio"
)

func main() {
    err := rpio.Open()
    if  err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
    defer rpio.Close()

    pin := rpio.Pin(26)

    pin.Output()

    for {
        pin.High()
        time.Sleep(time.Millisecond * 200)
        pin.Low()
        time.Sleep(time.Millisecond * 200)
    }
}
