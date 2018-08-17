#!/bin/python

from bs4 import BeautifulSoup
import urllib2 as u
import datetime as dt


#####################
#	Definitions:	#
#####################

class Article(object):
	'''
	Journal article class. 
	'''
	def __init__(self, jrnl, title, authors, pub_date, link_str):
		self.jrnl = jrnl
		self.title = title 
		self.authors = authors
		self.pub_date = pub_date
		self.link_str = link_str
	#end_def
	def get_pub_day(self):
		return self.pub_date[1]
	#end_def
	def get_title(self):
		return self.title
	#end_def
	def get_authors(self):
		return self.authors
	#end_def
	def get_link(self):
		return self.link_str
	#end_def
	def info_str(self):
		print(self.get_title())
		print(self.get_authors())
		print(self.get_link())
		print("\n")
	#end_def
#end_class


#############
#	CODE:	#
#############

# Get today's date:
today = dt.date.today().timetuple()
#print(today[0])	#year
#print(today[1])	#month
#print(today[2])	#day

# URL of scrape site:
site = 'http://journals.aps.org/prl/recent'

# Soup it up:
page = u.urlopen(site).read()
soup = BeautifulSoup(page, 'lxml')

element_list = []
for element in soup.find_all(class_='article panel article-result'):
	# get data elements:
	title = element.find(class_='title').get_text()
	date_tup = element.find(class_='pub-info').get_text().split('Published')[-1].strip().split()
	authors = element.find(class_='authors').get_text()
	link = element.a['href']
	# create class instances with articles published today:
	if date_tup[0] == "2": #### NOTE:2 is placeholder for now ... will be the current date ####
		element_list.append(Article("PRL", title, authors, date_tup, link))
	#end_if
#end_for

## TESTING: ##
for a in element_list:
	a.info_str()
#end_if


