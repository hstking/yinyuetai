#!/usr/bin/env python
#-*- coding: utf-8 -*-
__author__ = 'hstking hstking@hotmail.com'

import urllib2
import re
import os
import time
import multiprocessing
from myLog import MyLog
from cls import clear

class DownloadYinyuetaiMv(object):
	def __init__(self):
		clear()
		self.tip()
		self.log = MyLog()
		self.title = 'unknow'
		self.packageSize = 1024*1024
		self.mvPlayUrl = self.getMvPlayUrl()

	def getMvPlayUrl(self):
		'''获取音乐台mv的播放地址 '''
		self.log.info('获取mv的播放地址')
		self.mvPlayUrl = raw_input('输入音乐台中MV的播放地址\n如http://v.yinyuetai.com/video/615494:\n')
		self.checkMvPlayUrl(self.mvPlayUrl)
			

	def checkMvPlayUrl(self,url):
		'''检查输入的mv播放地址是否有效 '''
		self.log.info('检查mv播放地址')
		try:
			id = url.replace('http://v.yinyuetai.com/video/','')
			idNum = int(id)
		except ValueError:
			self.log.error('输入的mv播放地址有误，退出程序')
		res = urllib2.urlopen(url,timeout=5)
		mat = re.compile(r'<h3 class="fl f18">(.*?)</h3>')
		self.title = re.findall(mat,res.read())[0]

		print('MV:%s' %self.title)

		downUrl = self.getMvDownloadUrl(id)
		self.downloadMv(downUrl)

	def getMvDownloadUrl(self,id):
		'''获取mv的下载地址 '''
		self.log.info('获取mv下载地址')
		url = 'http://www.yinyuetai.com/insite/get-video-info?flex=true&videoId=' + id
		try:
			res = urllib2.urlopen(url,timeout=5)
		except:
			self.log.error('网页连接错误')
		mat = re.compile(r'http://h.?.yinyuetai.com/uploads/videos/common/.*?\.flv')
		urls = re.findall(mat,res.read())
		return urls[-1]

	def downloadMv(self,url):
		'''开始下载mv '''
		fileName = './' + self.title + '.mp4'
		res = urllib2.urlopen(url,timeout=5)
		self.log.info('开始下载MV %s' %fileName)
		rSize = int(dict(res.headers).get('content-length'))
		t1 = time.time()
		with open(fileName,'wb') as fp:
			st = res.read(self.packageSize)
			offset = 0
			while st:
				fp.write(st)
				st = res.read(self.packageSize)
				offset += len(st)
				p = multiprocessing.Process(target=self.pLen,args=(fileName,offset,rSize,))
				p.start()
		t2 = time.time()
		time.sleep(2)
		print(u'\n下载时间共%ds\n' %(t2 - t1))

	def pLen(self,fileName,offset,rSize):
		if offset < rSize:
			print('%s\t%dbytes/%dbytes\r' %(fileName,offset,rSize)),
			time.sleep(1)

	def tip(self):
		print('|' + '-'*40)
		print('|' + u'这是一个下载音悦台MV的脚本')
		print('|' + '-'*40)

if __name__ == '__main__':
	dym = DownloadYinyuetaiMv()
