#!/bin/bash
# start/stop Skript for datenfresser
#Sebastian Moors 31.07.2007
# sebastian.moors@gmail.com

if [ $# -ne 1 ]; then
	echo "Usage: /etc/init.d/datenfresser start | stop"
	exit 1
fi

binfile=/usr/sbin/datenfresser
pidfile=/var/run/datenfresser.pid

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

chown datenfresser $pidfile

if [  $1 == "start" ]; then
	start-stop-daemon -x $binfile  --start --pidfile $pidfile -c datenfresser
fi

if [ $1 == "stop" ]; then
	start-stop-daemon  --stop --pidfile $pidfile
fi
