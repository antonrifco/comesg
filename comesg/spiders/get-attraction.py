from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log
from comesg.items import ComesgItem

class AttractionSpider(CrawlSpider):
	name = "get-attraction"
	allowed_domains = ["comesingapore.com"]
	start_urls = [
		"http://comesingapore.com/travel-guide/category/285/attractions"
	]
	rules = ()

	def __init__(self, name=None, **kwargs):
		super(AttractionSpider, self).__init__(name, **kwargs)
		self.items_buffer = {}
		self.base_url = "http://comesingapore.com"
		from scrapy.conf import settings
		settings.overrides['DOWNLOAD_TIMEOUT'] = 360

	def parse(self, response):
		print "Start scrapping Attractions...."
		try:
			hxs = HtmlXPathSelector(response)
			links = hxs.select("//*[@id='content']//a[@style='color:black']/@href")
			
			if not links:
				return
				log.msg("No Data to scrap")

			for link in links:
				v_url = ''.join( link.extract() )
								
				if not v_url:
					continue
				else:
					_url = self.base_url + v_url
					yield Request( url= _url, callback=self.parse_details )
		except Exception as e:
			log.msg("Parsing failed for URL {%s}"%format(response.request.url))
			raise 

	def parse_details(self, response):
		print "Start scrapping Detailed Info...."
		try:
			hxs = HtmlXPathSelector(response)
			l_venue = ComesgItem()

			v_name = hxs.select("/html/body/div[@id='wrapper']/div[@id='page']/div[@id='page-bgtop']/div[@id='page-bgbtm']/div[@id='content']/div[3]/h1/text()").extract()
			if not v_name:
				v_name = hxs.select("/html/body/div[@id='wrapper']/div[@id='page']/div[@id='page-bgtop']/div[@id='page-bgbtm']/div[@id='content']/div[2]/h1/text()").extract()
			
			l_venue["name"] = v_name[0].strip()
			
			base = hxs.select("//*[@id='content']/div[7]")
			if base.extract()[0].strip() == "<div style=\"clear:both\"></div>":
				base = hxs.select("//*[@id='content']/div[8]")
			elif base.extract()[0].strip() == "<div style=\"padding-top:10px;margin-top:10px;border-top:1px dotted #DDD;\">\n  You must be logged in to add a tip\n  </div>":
				base = hxs.select("//*[@id='content']/div[6]")

			x_datas = base.select("div[1]/b").extract()
			v_datas = base.select("div[1]/text()").extract()
			i_d = 0;
			if x_datas:
				for x_data in x_datas:
					print "data is:" + x_data.strip()
					if x_data.strip() == "<b>Address:</b>":
					 	l_venue["address"] = v_datas[i_d].strip()
					if x_data.strip() == "<b>Contact:</b>":
					 	l_venue["contact"] = v_datas[i_d].strip()
					if x_data.strip() == "<b>Operating Hours:</b>":
					 	l_venue["hours"] = v_datas[i_d].strip()
					if x_data.strip() == "<b>Website:</b>":
					 	l_venue["website"] = (base.select("div[1]/a/@href").extract())[0].strip()

					i_d += 1
				
			v_photo = base.select("img/@src").extract()
			if v_photo:
				l_venue["photo"] = v_photo[0].strip()

			v_desc = base.select("div[3]/text()").extract()
			if v_desc:
				desc = ""
				for dsc in v_desc:
					desc += dsc
				l_venue["desc"] = desc.strip()

			v_video = hxs.select("//*[@id='content']/iframe/@src").extract()
			if v_video:
				l_venue["video"] = v_video[0].strip()


			yield l_venue
		except Exception as e:
			log.msg("Parsing failed for URL {%s}"%format(response.request.url))
			raise 
