__author__ = 'coderlin'
# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import os
import chardet
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')


def logD(msg):
	sys.stdout.write(msg)
	f = open("getpics.log","a+")
	#print("file save to"+fileName)
	f.write(msg.encode('utf-8'))
	f.close()
	
def log(msg):
	prefix="["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]"
	logtext=prefix+"\t"+msg
	logD(logtext)
def logl(msg):
	log(msg+"\n")

class Spider:

	def __init__(self):
		#print("init...")
		self.site= 'http://www.kifaonline.com.cn'

	def urlencode(self,val):
		if isinstance(val,unicode):
			return urllib.quote(str(val),safe='/:?=')
		return urllib.quote(val,safe='/:?=')
	
	def getEncoding(self,data):
		chardit1 = chardet.detect(data)
		encoding=chardit1['encoding']
		#print("encode:"+encoding)
		return encoding
		
	def getUrlContent(self,url):
		#print("getUrlContent url:"+url)
		request=urllib2.Request(self.urlencode(url))
		response=urllib2.urlopen(request)
		page=response.read()
		encoding=self.getEncoding(page)
		return page.decode(encoding)
		
	def postUrlContent(self,url,postdata):
		postdata=urllib.urlencode(postdata)
		request=urllib2.Request(self.urlencode(url),postdata)
		response=urllib2.urlopen(request)
		page=response.read()
		encoding=self.getEncoding(page)
		return page.decode(encoding)
	
	def getBreadList(self):
		content=self.getUrlContent(self.site+'/webProductContent')
		#print("content"+content)
		pattern = re.compile('prdBreedName=(.*?)"',re.S)
		items = re.findall(pattern,content)
		BreadList = []
		for item in items:
			BreadList.append(item)
		return BreadList
		
	def downloadBread(self,breadName):
		curPage=1
		while True:
			#print("downloading bread "+breadName+"...")
			content=self.nextPageContent(breadName,curPage)
			#print content
			self.saveText(content,breadName+".txt")
			pattern = re.compile(u'共(\d*?)页',re.S)
			pageNums = re.findall(pattern,content)
			if(len(pageNums)<1):
				logl(u"[x]错误: 页数失败")
				break;
			if(curPage>int(pageNums[0])):
				logl("[+]完成: "+breadName+"类 共"+str(curPage-1)+"页")
				break;
			self.downloadPage(content)
			curPage+=1
		
	def nextPageContent(self,breadName,cp):
		logl("[+]分类: "+breadName +" 第"+str(cp)+"页\t\t\t<---");
		BreadUrl=self.site+'/webProductContent'
		postdata={'prdBreedName': breadName, 'curPage': cp}
		return self.postUrlContent(BreadUrl,postdata)
		
	def downloadPage(self,pageContent):
		pattern = re.compile('class="sit-preview"\shref="(.*?)"><img src="(.*?)".*?center">(.*?)</div>',re.S|re.M)
		webProductContentItems = re.findall(pattern,pageContent)
		#url,imageUrl,name
		i=0
		for webProductContentItem in webProductContentItems:
			#print("webProductContentItem["+str(i)+"]:<"+webProductContentItem[0]+"><"+webProductContentItem[1]+"><"+webProductContentItem[2]+">")
			i+=1
			self.downloadProductItemToFolder(webProductContentItem,breadName)
			#break
		
	def downloadProductItemToFolder(self,productItem,folderName):
		self.mkdir(folderName)
		detailUrl=productItem[0]
		imageUrl=productItem[1]
		productName=productItem[2]
		imagePath=folderName+"/"+productName+".jpg"
		self.downloadImg(self.site+imageUrl,imagePath)
		#detail image
		content=self.getUrlContent(self.site+detailUrl)
		pattern = re.compile('<p><img src="(.*?upload.*?)"\stitle="',re.S)
		detailImgs = re.findall(pattern,content)
		if(len(detailImgs)>0):
			#print("downloading detail image:"+detailImgs[0])
			imagePath=folderName+"/"+productName+"D.jpg"
			self.downloadImg(self.site+detailImgs[0],imagePath)
		#self.saveText(content,imagePath+".txt")
		
	def mkdir(self,path):
		path = path.strip()
		isExists=os.path.exists(path)
		if not isExists:
			os.makedirs(path)
			return True
		else:
			return False
			
	def downloadImg(self,imageURL,fileName):
		if(os.path.exists(fileName)):
			logl("[!]存在: "+fileName);
			return
		try:
			log("[*]下载: "+fileName+" ...")
			u = urllib.urlopen(imageURL)
			data = u.read()
			#uipath = unicode(fileName , "utf8")
			#print fileName
			f = open(fileName,'wb')
			f.write(data)
			f.close()
		except:
			logD(u"失败\n");
		else:
			logD(u"成功\n");
		
	def saveText(self,text,fileName):
		f = open(fileName,"w+")
		#print("file save to"+fileName)
		f.write(text.encode('utf-8'))

logl(u"========== 开始 getpics v1.0 ==============");
logl(u"\tby coderlin for yya ")
spider = Spider()
breadNameList=spider.getBreadList()
del breadNameList[0]
i=0
for breadName in breadNameList:
	#print("breadName["+str(i)+"]:<"+breadName+">")
	spider.downloadBread(breadName)
	i+=1
logl(u"[.]完成.")
