import scrapy
import logging


class LawyersSpider(scrapy.Spider):
    name = 'lawyers'
    allowed_domains = ['www.floridabar.org']
    start_urls = ['https://www.floridabar.org/directories/find-mbr/?lName=&sdx=N&fName=*&eligible=N&deceased=N&firm=&locValue=&locType=C&pracAreas=&lawSchool=&services=&langs=&certValue=&pageNumber=1&pageSize=10']

    def parse(self, response):
        for profile in response.xpath("//ul[@class='profiles-compact']/li"):
            bar_number = profile.xpath(".//p[@class='profile-bar-number']/span/text()").get()
            attorney_name = profile.xpath(".//p[@class='profile-name']/a/text()").get()
            eligible = 'eligible' if profile.xpath(".//div[@class='eligibility eligibility-eligible']/text()").get() else 'not eligible'
            # not_eligible = profile.xpath(".//div[@class='eligibility eligibility-ineligible-neutral']/text()").get()
            photo = profile.xpath(".//div[@class='profile-image']/a/img/@src").get()
            mailing_address = profile.xpath(".//div[@class='profile-contact']/p[1]/text()").extract()
            phone_1 = profile.xpath(".//div[@class='profile-contact']/p[2]/a[1]/text()").get()
            phone_2 = profile.xpath(".//div[@class='profile-contact']/p[2]/a[2]/text()").get()
            email = profile.xpath(".//div[@class='profile-contact']/p[2]/a[3]").get()
            url = profile.xpath(".//p[@class='profile-name']/a/@href").get()
            yield response.follow(url=url, callback=self.parse_lawyers, meta={'bar_number':bar_number, 'attorney_name':attorney_name, 'eligible':eligible, 'photo':photo, 'mailing_address':mailing_address, 'phone_1':phone_1, 'phone_2':phone_2, 'email':email, 'url':url})
        
#        next_page = response.xpath("//a[@title='next page']/@href").get()
        # We can let the web scraper to retreive and store a certain number of search results here. 
 #       next_page = response.urljoin(next_page)
 #       yield scrapy.Request(url=next_page, callback=self.parse)       

    def parse_lawyers(self, response):
        bar_number = response.request.meta['bar_number']
        attorney_name = response.request.meta['attorney_name']
        standing = 'yes' if response.xpath("//div[@class='member-status status-good']") else 'no'
        yield {
            'attorney_name': attorney_name, 
            'bar_number':bar_number,
            'in good standing?': standing,
            'section 1':response.xpath("//div[@class='container-fluid']/div[2]")
        }
