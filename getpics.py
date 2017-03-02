__author__ = 'coderlin'
# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import os
import chardet

class Spider:

	def __init__(self):
		print("init...")
		self.siteURL = 'http://www.kifaonline.com.cn/webProductContent'

	def getEncoding(self,data):
		chardit1 = chardet.detect(data)
		encoding=chardit1['encoding']
		print("encode:"+encoding)
		return encoding
		
	def getUrlContent(self,url):
		request=urllib2.Request(url)
		response=urllib2.urlopen(request)
		page=response.read()
		encoding=self.getEncoding(page)
		return page.decode(encoding)
	
	def getBreadList(self):
		content=self.getUrlContent(self.siteURL)
		#print("content"+content)
		pattern = re.compile('prdBreedName=(.*?)"',re.S)
		items = re.findall(pattern,content)
		BreadList = []
		for item in items:
			BreadList.append(item)
		return BreadList
		
	def downloadBread(self,breadName):
		urlprefix='/webProductContent?prdBreedName='
		
		
	def mkdir(self,path):
		path = path.strip()
		# 判断路径是否存在
		# 存在	 True
		# 不存在   False
		isExists=os.path.exists(path)
		# 判断结果
		if not isExists:
			# 如果不存在则创建目录
			# 创建目录操作函数
			os.makedirs(path)
			return True
		else:
			# 如果目录存在则不创建，并提示目录已存在
			return False
			
	def saveImg(self,imageURL,fileName):
		u = urllib.urlopen(imageURL)
		data = u.read()
		f = open(fileName, 'wb')
		f.write(data)
		f.close()

spider = Spider()
breadNameList=spider.getBreadList()
i=0
for breadName in breadNameList:
	print("breadName["+str(i)+"]:<"+breadName+">")
	i+=1
print("done.")
