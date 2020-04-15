# Simple dockerized permission server

## Installation
1. Clone: `git clone https://github.com/rrrealman/permission-server.git` and `cd permission-server`
2. Run `docker-compose up --build`
3. Run database migrations `docker exec -it permissionserver_web_1 python manage.py db upgrade -d /migrations`

## Usage

