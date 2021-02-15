import scrapy

class LawyersSpider(scrapy.Spider):
    name = 'lawyers'
    allowed_domains = ['www.floridabar.org']
    start_urls = ['https://www.floridabar.org/directories/find-mbr/?lName=&sdx=N&fName=*&eligible=N&deceased=N&firm=&locValue=&locType=C&pracAreas=&lawSchool=&services=&langs=&certValue=&pageNumber=54&pageSize=10']

    def parse(self, response):
        for profile in response.xpath("//ul[@class='profiles-compact']/li"):
            yield {
                'bar_number':profile.xpath(".//p[@class='profile-bar-number']/span/text()").get(),
                'attorney_name':profile.xpath(".//p[@class='profile-name']/a/text()").get(),
                'eligible':profile.xpath(".//div[@class='eligibility eligibility-eligible']/text()").get(),
                'not eligible':profile.xpath(".//div[@class='eligibility eligibility-ineligible-neutral']/text()").get(),
                'photo':profile.xpath(".//div[@class='profile-image']/a/img/@src").get(),
                'mailing_address':profile.xpath(".//div[@class='profile-contact']/p[1]/text()").extract(),
                'phone_1':profile.xpath(".//div[@class='profile-contact']/p[2]/a[1]/text()").get(),
                'phone_2':profile.xpath(".//div[@class='profile-contact']/p[2]/a[2]/text()").get(),
                'email':profile.xpath(".//div[@class='profile-contact']/p[2]/a[3]").get(),
                'url':profile.xpath(".//p[@class='profile-name']/a/@href").get()
            }

        next_page = response.xpath("//a[@title='next page']/@href").get()

        if next_page: 
        # We can let the web scraper to retreive and store a certain number of search results here. 
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)