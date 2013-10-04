#Simple Web Crawler

#A web crawler (also known as a web spider or web robot) is a program or automated script which browses the World Wide Web in a methodical, automated manner

#This python based crawler works on the logic that if there is a http or '/' after a "(quote symbol) it should be a link.


import httplib
from urllib import urlopen, urlretrieve
from sys import stdout
from os import fsync, rename, remove, mkdir

#The WebCrawler class
class WebCrawler:
	def __init__(self, show=False):
		'''Web Crawler'''
		self.show = show
		self.links = set()
		self.crawled = set()

	def __len__(self):
		return len(self.links)
	
	
	def all_links(self):
		"""return all links found"""
		return list(self.links)

	def webcrawl(self, link):
		'''Recursive Functions to crawl the links'''
		for url in self.get_links(link):
			try:
				self.webcrawl(url)
			except (IOError, RuntimeError):
				pass


	def get_links(self, link):
		'''This method loads a page and returns all external links,
		it also add links to the list of links accessible with self.all_links()
		raise an IOError if any errors'''
		if (link in self.crawled):
			raise IOError("link already found")
		
		self.crawled.add(link)
		try:
			page = urlopen(link).read()
		except (IOError, httplib.InvalidURL, httplib.LineTooLong, TypeError):
			return []
		links = set()
		new = ''
		domain = ("http://%s" % link.split("/")[2])
		page_contents = (page.split('"') + page.split("'")) 
		for current_link in page_contents:
			if (current_link.startswith("http")):new = current_link
			elif (current_link.startswith("/")):new = domain + current_link
			#begin cut and repair non html links
			if ("/>" in new):new = new[:new.find("/>")+1]
			if ("/*" in new):new = new[:new.find("/*")]
			if (new.count("//") >= 2):new = 'http://' + new.split("//")[2]
			#end cut and repair non html links
			links.add(new)
		self.links = self.links.union(links)
		if (self.show):
			stdout.write("\rCrawled and found %i urls and %i requests done." % (len(self), len(self.crawled)))
			stdout.flush()
		return list(links)

def main():
	'''Initiating Webcrawler......'''
	
	crawler = WebCrawler(show=True)
	site = "http://" + raw_input("{0}\nEnter first link to be crawled\n{0}\nhttp://".format("-"*40))
		
	print("\n{0}\nCrawler Released...\npress CTRL+C to save and exit\n{0}".format("-"*40))
	
	try:
		#crawling function
		crawler.webcrawl(site)
	except KeyboardInterrupt:
		print("\nSaving links")
	#writing out links in html format
	if ("y" in raw_input("Would you like to save it into html page?\nY/N: ").lower()):
		file__format = "html"
		text = '<title>Sites Found</title>'
		for link in crawler.all_links():
			text += '</br ><a href="%s" target=_blanc>%s</a>\n' % (link, link)
	#writing out links in text format
	else:
		raw_input("\nThe file will be saved as Text")
		text = ""
		file__format = "txt"
		for link in crawler.all_links():
			text += "%s\n" % link
	#writing files according to their choosed format	
	try:
		file = open("Crawled_links.%s.tmp" % file__format, "w")
		file.write(text)
		file.flush()
		fsync(file.fileno())
		file.close()
	except TypeError:
		print("Failed to save")
	try:
		remove("Crawled_links.%s" % file__format)
	except:
		pass
	rename("Crawled_links.%s.tmp" % file__format, "Crawled_links.%s" % file__format)
	print("\n{0}\nSaved Sucessfully!!!!!!!!!\n{0}").format("-"*40)
	return 0

if __name__ == "__main__":
         main()
