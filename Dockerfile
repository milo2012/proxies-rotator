FROM debian:sid
MAINTAINER milo2012 "keith.lee2012@gmail.com"
COPY proxyTester.py /scripts/proxyTester.py

COPY proxist.py /scripts/proxist.py
COPY parseProxyList.py /scripts/parseProxyList.py
COPY haproxy.cfg /scripts/haproxy.cfg
COPY run.sh /scripts/run.sh
COPY get-pip.py /scripts/get-pip.py
#RUN chmod 755 /scripts/run.sh
RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
RUN apt-get clean autoclean
RUN apt-get autoremove -y
RUN apt-get clean
RUN apt-get update 
RUN apt-get install iptables zlib1g zlib1g-dev curl python-dev sudo  -y
#RUN apt-get install iptables zlib1g zlib1g-dev openssl libssl-dev build-essential curl python-dev sudo  -y

RUN echo "deb http://httpredir.debian.org/debian jessie-backports main" >> /etc/apt/sources.list.d/backports.list 
RUN echo "deb http://haproxy.debian.net jessie-backports-1.6 main" >> /etc/apt/sources.list.d/haproxy.list 
RUN curl http://haproxy.debian.net/bernat.debian.org.gpg | apt-key add - 
RUN apt-get update 
RUN apt-get install haproxy -t jessie-backports-1.6 -y --force-yes --fix-missing
RUN apt-get clean & rm -rf /var/lib/apt/lists/*

RUN curl -o /scripts/get-pip.py https://bootstrap.pypa.io/get-pip.py
RUN bash -c "/usr/bin/python /scripts/get-pip.py" 
RUN pip install requests requesocks extraction 
RUN rm -rf /var/lib/{apt,dpkg,cache,log}/

#RUN chmod -R 777 /usr/local/lib/ruby/
RUN chmod -R 777 /scripts
RUN chmod -R 777 /etc/haproxy
RUN echo "docker ALL=(ALL) NOPASSWD:ALL " >> /etc/sudoers			
USER docker

CMD ["/scripts/run.sh"]
#CMD ["/usr/sbin/haproxy","-f", "/scripts/haproxy.cfg"]
EXPOSE 5566
