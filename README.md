# proxies-rotator
Dockerfile for Proxies Testing/Rotation  
  
1) Pulls proxies from HideMyAss  
2) Test the proxies  
3) Rotate the proxies using HAProxy (round robin)  
4) Repeat every 5 minutes  
5) Expose port 5566 as a proxy to be used by other penetration testing tools  
    
#Below are the basic steps  
docker pull milo2012/proxies  
docker run -p 5566:5566 --privileged=true -t milo2012/proxies:1.0  
