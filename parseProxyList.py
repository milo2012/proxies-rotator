s = """ 
global
        log 127.0.0.1   local0
        log 127.0.0.1   local1 notice
	#local0.*  /var/log/haproxy.log
        #log /var/log/haproxy.log local0 debug
        #log loghost    local0 info
        maxconn 4096
        #chroot /usr/share/haproxy
        user haproxy
        group haproxy
        daemon
        debug
        #quiet
        stats socket /tmp/haproxy

defaults
        log global
        mode http
        option httplog
        option dontlognull
        retries 3
        option redispatch
        maxconn 2000
        timeout connect 5000
        timeout client 50000
        timeout server 50000 
        #clitimeout 50000
        #srvtimeout 50000

frontend rotating_proxies
  bind *:5566
  default_backend tor
  option http_proxy

backend tor
  balance roundrobin """
hostCount=1
#print s
f = open("/scripts/proxies1.txt")
lines = f.readlines()
for x in lines:	
	x = x.strip()
	if len(x)>0:
		results = "\nserver srv"+str(hostCount)+" "+x.strip()+" weight 1 maxconn 100 check"
		#print results+"\n"
		s += results
	hostCount+=1
	
#print s
with open("/etc/haproxy/haproxy.cfg", "w") as text_file:
	text_file.write(s)
with open("/scripts/haproxy.cfg", "w") as text_file:
	text_file.write(s)
