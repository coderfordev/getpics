__author__ = 'coderlin'
# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import os
import chardet
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class Spider:

	def __init__(self):
		print("init...")
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
		print("getUrlContent url:"+url)
		request=urllib2.Request(self.urlencode(url))
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
		print("downloading bread "+breadName+"...")
		BreadUrl=self.site+'/webProductContent?prdBreedName='+breadName
		content=self.getUrlContent(BreadUrl)
		#print content
		#self.saveText(content,breadName+".txt")
		pattern = re.compile('class="sit-preview"\shref="(.*?)"><img src="(.*?)".*?center">(.*?)</div>',re.S|re.M)
		webProductContentItems = re.findall(pattern,content)
		#url,imageUrl,name
		i=0
		for webProductContentItem in webProductContentItems:
			#print("webProductContentItem["+str(i)+"]:<"+webProductContentItem[0]+"><"+webProductContentItem[1]+"><"+webProductContentItem[2]+">")
			i+=1
			self.downloadProductItemToFolder(webProductContentItem,breadName)
			break
		
	def downloadProductItemToFolder(self,productItem,folderName):
		self.mkdir(folderName)
		detailUrl=productItem[0]
		imageUrl=productItem[1]
		productName=productItem[2]
		imagePath=folderName+"/"+productName+".jpg"
		self.saveImg(self.site+imageUrl,imagePath)
		
		#detail image
		content=self.getUrlContent(self.site+detailUrl)
		pattern = re.compile('<p><img src="(.*?upload.*?)"\stitle="',re.S)
		detailImgs = re.findall(pattern,content)
		if(len(detailImgs)>0):
			print("downloading detail image:"+detailImgs[0])
			imagePath=folderName+"/"+productName+"D.jpg"
			self.saveImg(self.site+detailImgs[0],imagePath)
		#self.saveText(content,imagePath+".txt")
		
	def mkdir(self,path):
		path = path.strip()
		isExists=os.path.exists(path)
		if not isExists:
			os.makedirs(path)
			return True
		else:
			return False
			
	def saveImg(self,imageURL,fileName):
		if(os.path.exists(fileName)):
			print(fileName+" exist already.");
			return
		print("downloading "+fileName)
		u = urllib.urlopen(imageURL)
		data = u.read()
		#uipath = unicode(fileName , "utf8")
		print fileName
		f = open(fileName,'wb')
		f.write(data)
		f.close()
		
	def saveText(self,text,fileName):
		f = open(fileName,"w+")
		#print("file save to"+fileName)
		f.write(text.encode('utf-8'))

spider = Spider()
breadNameList=spider.getBreadList()
del breadNameList[0]
i=0
for breadName in breadNameList:
	#print("breadName["+str(i)+"]:<"+breadName+">")
	if(i>2):
		break
	spider.downloadBread(breadName)
	i+=1
print("done.")
