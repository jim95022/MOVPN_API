# MOVPN - My Own VPN project

This project provides a simple API for external control of [Algo VPN](https://github.com/trailofbits/algo) server.

## Requirements:
- [Ubuntu](https://ubuntu.com/)/[Debian](https://www.debian.org/)
- [Python 3.11+](https://www.python.org/)
- [Algo VPN](https://github.com/trailofbits/algo)

## Available endpoints

> **user** - VPN user of Algo VPN
> 
> **user creds** - QR code and/or connection cert


- `GET /users`                   get all **users**
- `POST /users/<username>`       add new **user**
- `GET /users/<username>/qr`     retrieve **user qr code**
- `GET /users/<username>/conf`   retrieve **user cert**
- `DELETE /users/<username>`     remove **user**

🚨 _endpoints below are not implemented yet_

- `POST /users/sync`             synchronize all users
- `GET /stat`                    load statistics


## Installation

> ⚠️ Work In Progress ⚠️
