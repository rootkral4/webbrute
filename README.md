# webbrute
tool for web brute forcing

## SETUP

chmod +x webbrute

## USAGE

./webbrute -h

./webbrute -u url -l username or userlist -p password or passlist -m method get or post -d "username param&password param:error text"

./webbrute -u http://1.1.1.1 -l kral4 -p rockyou.txt -m post -d "username&password:invalid username or password"
