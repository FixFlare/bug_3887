# bug_3887

## Required Redis Install for both

1. ```sudo zypper install redis```  (command may differ depending on your distribution)
1. Copy default redis config ```sudo cp /etc/redis/default.conf.example /etc/redis/redis.conf```
1. Start Redis (default port 6379)



## Testing on Uvicorn (working)
1. Git clone this repository
1. cd to that directory and run `pdm sync` to install packages
1. Open cloned folder in VSCode
1. Using vscode launch configuration run "Debug Server (bug_3887)" <br>
This will run on port 8081 by default, access http://localhost:8081/api/public/client.html
1. Click "Connect Websocket on Uvicorn" button - note the printed "test" message on console. Works fine


## Testing on Nginx Unit (not working)
Install Nginx Unit, I recommend docker for ease of use: [Nginx Unit Docker](https://unit.nginx.org/howto/docker/)

An example "config.json" for this bug is provided. You will need to adjust the paths for wherever you cloned the directory. (Look for YOURUSERNAME)

Once nginx unit is up and running and you've uploaded the config.json you should be able to access [http://localhost/index.html](http://localhost/index.html).

This will be the basic html file served by nginx unit (client) using websockets to connect to our python app (server) also running on nginx unit.

Traffic is directed to one or the other based on the "match" of the /api uri in our config.json

`tail` the unit log so you can see the error happen

Your path may vary based on your setup but something like: 
```bash
sudo tail -f /usr/local/var/log/unit/unit.log
```


You should see the 
```bash
litestar.exceptions.http_exceptions.MethodNotAllowedException: 405: Method Not Allowed
```
Mentioned in [Bug 3887](https://github.com/litestar-org/litestar/issues/3887) that this repo is all about







