# Simple dockerized permission server

## Installation
1. Clone: `git clone https://github.com/rrrealman/permission-server.git` and `cd permission-server`
2. Run `docker-compose up --build`
3. Run database migrations `docker exec -it permissionserver_web_1 python manage.py db upgrade -d /migrations`

## Usage
`docker exec -it permissionserver_web_1 python manage.py --help`:
```
usage: manage.py [-?]
                 {db,install_roles,grant_role_command,withdraw_role_command,shell,runserver}
                 ...

positional arguments:
  {db,install_roles,grant_role_command,withdraw_role_command,shell,runserver}
    db                  Perform database migrations
    install_roles       Install predefined roles list
    grant_role_command  Grant role to user
    withdraw_role_command
                        Withdraw role from user
    shell               Runs a Python shell inside Flask application context.
    runserver           Runs the Flask development server i.e. app.run()

optional arguments:
  -?, --help            show this help message and exit
```
