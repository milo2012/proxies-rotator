#!/bin/bash
#while true
echo "Press [CTRL+C] to stop.."
while :
do
	cd /scripts
	echo "Downloading Proxies"
	python /scripts/proxist.py -o /scripts/proxies.txt
	echo "Testing Proxies"
	python -W ignore /scripts/proxyTester.py -i /scripts/proxies.txt -n 100 -skipSocks -v -silent > /scripts/proxies1.txt
	sudo iptables -I INPUT -p tcp --dport $PORT 5566 -j DROP
	sleep 1
	sudo python /scripts/parseProxyList.py
	sudo service haproxy restart
	sudo iptables -D INPUT -p tcp --dport $PORT 5566 -j DROP
	echo "Sleeping for 5 minutes"
	sleep 300
done
