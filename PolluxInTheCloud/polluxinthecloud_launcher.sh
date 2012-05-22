#!/bin/sh

cd `dirname $0`
if [ -x /usr/bin/x-www-browser ]; then
    /usr/bin/env x-www-browser http://127.0.0.1/ &
    echo "Please input your user password to use 'sudo': "
    sudo /usr/bin/env python ./polluxinthecloud.py -p 80 -vvv
else
    echo "couldn't find a browser. Press a key to close this program"
    read
fi

