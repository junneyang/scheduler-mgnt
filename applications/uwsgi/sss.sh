#!/bin/sh
set -e

user=rootdss
ret=`egrep "^$user" /etc/passwd | awk -F':' '{ print $1 }'`
if [ x$ret = x ] ; then
    echo "user not exist!"
fi
