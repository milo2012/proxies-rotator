import httplib
import operator
import timeit
import socket
import urllib2
import requests
import sys
import argparse
import requesocks
import multiprocessing
import extraction
import random
import time
import socket
import urllib2

optionSilent=False
skipTime=False
skipSocks=False
urlType="http"
timeoutTime=10
numThreads=35
resultList=[]
proxyList=[]

socks4List=[]
socks5List=[]
httpList=[]
httpsList=[]

urlList = []
urlList.append(["https://www.tracemyip.org/","Trace My IP"])
urlList.append(["http://jmpserver.ddns.net:61001/test.txt","Hello World Page"])
#urlList.append(["http://whatismyipaddress.com/","What Is My IP Address?"])


def execute1(jobs, num_processes=2):
    	work_queue = multiprocessing.Queue()
    	for job in jobs:
        	work_queue.put(job)

    	result_queue = multiprocessing.Queue()
	
	worker = []
    	for i in range(num_processes):
       		worker.append(Worker1(work_queue, result_queue))
       	 	worker[i].start()

	results = []
    	while len(results) < len(jobs):
       	 	result = result_queue.get()
       		results.append(result)
    	results.sort()
    	return (results)
	
class Worker1(multiprocessing.Process):
	def __init__(self,work_queue,result_queue,):
        	multiprocessing.Process.__init__(self)
        	self.work_queue = work_queue
        	self.result_queue = result_queue
        	self.kill_received = False
   	def run(self):
        	while (not (self.kill_received)) and (self.work_queue.empty()==False):
           		try:
                		job = self.work_queue.get_nowait()
            		except:
                		break
            		(jobid,urlType,proxyHost) = job
            		rtnVal = (jobid,proxyHost,getURL1(proxyHost,"head"))
            		self.result_queue.put(rtnVal)

def chunk(input, size):
    	return map(None, *([iter(input)] * size))

def testSocks4(proxyHost,urlType):
	if skipSocks==False:
		global timeoutTime
	
		hostNo = proxyHost.split(":")[0]
		portNo = proxyHost.split(":")[1]
			
		proxyTypeList=[]
		proxyTypeList.append("socks4")
			
		for proxyType in proxyTypeList:
			session = requesocks.session()
			session.timeout = timeoutTime
			if proxyType=="socks4":
				if urlType=="https":
					session.proxies = {'https': 'socks4://'+hostNo+':'+portNo}
					urlPosition = urlList[0]
				else:
					session.proxies = {'http': 'socks4://'+hostNo+':'+portNo}
					urlPosition = urlList[1]	

			try:
				url = urlPosition[0]
				urlTitle = urlPosition[1]
				r = session.get(url)

				statusCode = str(r.status_code)

				if statusCode=="200":
					result = ((proxyHost,"",proxyType))
					resultList.append(result)
					if proxyType=="socks4":
						return proxyHost+"\tsocks4\t200"
				else:
					return proxyHost+"\t"+proxyType+"\t"+statusCode
			except Exception as e:
				return proxyHost+"\t"+proxyType+"\t503"

def testSocks5(proxyHost,urlType):
	if skipSocks==False:
		global timeoutTime
		hostNo = proxyHost.split(":")[0]
		portNo = proxyHost.split(":")[1]
				
		proxyTypeList=[]
		proxyTypeList.append("socks5")
				
		for proxyType in proxyTypeList:
			session = requesocks.session()
			session.timeout = timeoutTime
			if proxyType=="socks5":
				if urlType=="https":
					urlPosition = urlList[0]
					session.proxies = {'https': 'socks5://'+hostNo+':'+portNo}
				else:
					urlPosition = urlList[1]
					session.proxies = {'http': 'socks5://'+hostNo+':'+portNo}
			try:
		
				url = urlPosition[0]
				urlTitle = urlPosition[1]
	
				r = session.get(url)	

				statusCode = str(r.status_code)

				if statusCode=="200":
					result = ((proxyHost,"",proxyType))
					resultList.append(result)
					if proxyType=="socks5":
						return proxyHost+"\tsocks5\t200"
				else:
					return proxyHost+"\t"+proxyType+"\t"+statusCode
			except Exception as e:
				return proxyHost+"\t"+proxyType+"\t503"


def getURL1(proxyHost,requestType):
	global timeoutTime
	hostNo = proxyHost.split(":")[0]
	portNo = proxyHost.split(":")[1]
			
	global statusCode
	try:
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

		hostNo = proxyHost.split(":")[0]
		portNo = proxyHost.split(":")[1]

		session = requesocks.session()
		session.timeout = timeoutTime
		if urlType=="https":
			urlPosition = urlList[0]
			session.proxies = {'https': 'https://'+hostNo+':'+portNo}
		if urlType=="http":
			urlPosition = urlList[1]
			session.proxies = {'http': 'http://'+hostNo+':'+portNo}
		url = urlPosition[0]
		urlTitle = urlPosition[1]
		
		if requestType=="head":
			r = session.get(url)
			#try:
			extracted = extraction.Extractor().extract(r.text, source_url=url)
			if urlTitle not in extracted.title:
				statusCode="503"
			else:		
				statusCode="200"
		elif requestType=="get":
			r = session.head(url)
			statusCode=str(r.status_code)

		result2 = proxyHost+"\t"+urlType+"\t"+statusCode

		if statusCode!="200":
			if skipSocks==False:
				result1 = testSocks4(proxyHost,urlType)
				if "503" in str(result1):
					result = testSocks5(proxyHost,urlType)
					return result1
					#return result2+"\n"+results1+"\n"+result
				else:
					return result1
		else:
			return statusCode
			return proxyHost+"\t"+urlType+"\t"+statusCode

	except requests.exceptions.ConnectionError as e:
		return proxyHost+"\t"+urlType+"\t503"	

	except Exception as e: 
		result2 = proxyHost+"\t"+urlType+"\t503"

		result1 = testSocks4(proxyHost,urlType)
		if "503" in str(result1):
			if skipSocks==False:
				result = testSocks5(proxyHost,urlType)
				return result2+"\n"+result1+"\n"+result
		else:
			if options.v:
				if result1!=None:
					if optionSilent==False:	
						print "Found1: "+str(result1)
				else:
					return ""
			return result1
def getURL2(proxyHost,requestType):
	hostNo = proxyHost.split(":")[0]
	portNo = proxyHost.split(":")[1]
			
	global statusCode
	try:
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

		hostNo = proxyHost.split(":")[0]
		portNo = proxyHost.split(":")[1]

		session = requesocks.session()
		session.timeout = timeoutTime
		if urlType=="https":
			urlPosition = urlList[0]
			session.proxies = {'https': 'https://'+hostNo+':'+portNo}
		if urlType=="http":
			urlPosition = urlList[1]
			session.proxies = {'http': 'http://'+hostNo+':'+portNo}
		url = urlPosition[0]
		urlTitle = urlPosition[1]
		
		if requestType=="head":
			r = session.get(url)
			extracted = extraction.Extractor().extract(r.text, source_url=url)
			if urlTitle not in extracted.title:
				statusCode="503"
			else:
				statusCode="200"
		elif requestType=="get":
			r = session.head(url)
			statusCode=str(r.status_code)

		result2 = proxyHost+"\t"+urlType+"\t"+statusCode

		if statusCode!="200":
			if skipSocks==False:
				result1 = testSocks4(proxyHost,urlType)
				if "503" in str(result1):
					result = testSocks5(proxyHost,urlType)
					return result2+"\n"+results1+"\n"+result
				else:
					return result1
		else:
			return proxyHost+"\t"+urlType+"\t"+statusCode

	except requests.exceptions.ConnectionError as e:
		return proxyHost+"\t"+urlType+"\t503"	

	except Exception as e: 
		result2 = proxyHost+"\t"+urlType+"\t503"
		result1 = testSocks4(proxyHost,urlType)
		if "503" in str(result1):
			if skipSocks==False:
				result = testSocks5(proxyHost,urlType)
				return result2+"\n"+result1+"\n"+result
			else:
				if options.v:
					if result1!=None:
						if optionSilent==False:	
							print result1
				return result1


if __name__ == '__main__':
    	parser = argparse.ArgumentParser()
    	parser.add_argument('-i',dest='ipFile',action='store',help='[file containing list of proxies]')
    	parser.add_argument('-n',dest='threads',action='store',help='[number of threads]')
    	parser.add_argument('-t',dest='urlType',action='store',help='[type of website to test (https or http) ]')
    	parser.add_argument('-skipSocks', action='store_true', help='[skip testing for socks proxies]')
    	parser.add_argument('-silent', action='store_true', help='[silent mode, only display results]')
    	parser.add_argument('-v', action='store_true', help='[verbose mode]')
    	options = parser.parse_args()

    	if len(sys.argv)==1:
        	parser.print_help()
        	sys.exit()
    	else:
		if options.silent:
			optionSilent=True
		if options.skipSocks:
			skipSocks=True
		with open(options.ipFile) as f:
			proxyList = f.read().splitlines()
			proxyList=list( set(proxyList))
			proxyList = [x for x in proxyList if x]
	
		if options.threads:
			tempList1 = chunk(proxyList, int(options.threads))
		else:
			tempList1 = chunk(proxyList, 35)

		totalCount=len(tempList1)
		count = 1 
		for proxyList in tempList1:
			jobs = [] 
			jobid=0
			if optionSilent==False:
				print "- Set "+str(count)+" of "+str(len(tempList1))
			for proxyHost in proxyList:
				try:
					if proxyHost!=None:
						if optionSilent==False:	
							print "- Testing: "+proxyHost
						if options.urlType:
							urlType = options.urlType
							jobs.append((jobid,options.urlType,proxyHost))
						else:
							jobs.append((jobid,urlType,proxyHost))
						jobid = jobid+1
				except TypeError:
					continue
		
			numProcesses = numThreads
			resultList = execute1(jobs,numProcesses)
			for result in resultList:
				if result[2]!=None:
					if "200" in result[2]:
						if options.v:
							if optionSilent==False:
								print "Found: "+str(result[1])	
						httpList.append(result[1])
					#else:
						#if "socks4" in str(result[2]):
						#	socks4List.append(result[2])
						#elif "socks5" in str(result[2]):
						#	socks5List.append(result[2])
						#elif "https" in str(result[2]):
						#	httpsList.append(result[2])
						#else:
						#	httpList.append(result[2])
			#statusCode=""
			count+=1


		if optionSilent==False:	
			print "\n------------------------------------------------------------------"
		proxyID=100
		proxyIDList=[]
		chainID=""


		if len(httpsList)>0:
			if optionSilent==False:	
				print "\nWorking HTTPs Proxies"
			for x in httpsList:
				print x

			if optionSilent==False:	
				print "\n------------------------------------------------------------------"
		if len(httpList)>0:
			if optionSilent==False:	
				print "\nWorking HTTP Proxies"
			for x in httpList:
				print x

			if optionSilent==False:	
				print "\n------------------------------------------------------------------"

