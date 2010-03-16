#!/bin/bash
# start/stop Skript for datenfresser
#Sebastian Moors 31.07.2007
# sebastian.moors@gmail.com

if [ $# -ne 1 ]; then
	echo "Usage: /etc/init.d/datenfresser start | stop"
	exit 1
fi

binfile=/usr/sbin/datenfresser

if [ ! -x $binfile ]; then
	echo "datenfresser binary not found"
	exit 1
fi

if [ ! -f $pidfile ]; then
	touch $pidfile
fi

if [ ! -w $pidfile ]; then
	exit 1
fi


if [  $1 == "start" ]; then
	start-stop-daemon -x $binfile  --start -c datenfresser
fi

if [ $1 == "stop" ]; then
	start-stop-daemon  --stop -n datenfresser
fi
