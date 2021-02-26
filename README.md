A program I use to show the temperature on my desktop (in i3 status bar)

## Arduino project

- define a BLE peripheral device (that's a server) that will post the temperature

## Python project

- read temperature via BLE
- serve it over HTTP

## To show in i3

- make a script that `curl -s http://localhost:8500`
