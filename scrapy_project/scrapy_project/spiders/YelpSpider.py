import scrapy
import logging
import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_project.items import MyItem
from scrapy.mail import MailSender

class YelpSpider(scrapy.Spider):
    logger = logging.getLogger()

    name = "YelpSpider"
    allowed_domains = ["yelp.com"]
    count_item = 0
    ts = datetime.datetime.now().timestamp()
    site = 'https://www.yelp.com'

    def start_requests(self):
        url = self.site
        serch_category = self.category
        serch_address = self.address
        if serch_category is not None:
            if serch_address is not None:
                serch_address = serch_address.replace(" ", "+")
                url = url + '/search?find_desc=' + serch_category + '&find_loc=' + serch_address + '&ns=1'
                yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response):
        url = self.site
        for quote in response.css('li'):
            item_link = quote.css('div.businessNameWithNoVerifiedBadge__373c0__24q4s div span a::attr(href)').get()
            if item_link != None:
                url_all = url + str(item_link)
                yield scrapy.Request(url_all, callback=self.parse_item)

        next_page = response.css('div.pagination__373c0__1NjN5 a::attr(href)').getall()[-1]
        if next_page is not None:
            next_page = url + next_page
            yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response):
        card_all = response.css('div.stickySidebar--heightContext__373c0__133M8')

        address_all_span = card_all.css('address.lemon--address__373c0__2sPac span::text').getall()

        count_address_all_span = len(address_all_span)

        address_all_span_after = card_all.css('div.pseudoIsland__373c0__Fak5q div.lemon--div__373c0__1mboc.border-color--default__373c0__2oFDT p::text').getall()

        address_all = []
        for znch in address_all_span:
            address_all.append(znch)
        for znch in address_all_span_after:
            address_all.append(znch)

        item = MyItem()

        item['name_dir'] = str(self.ts) + '_' + str(self.count_item)

        name = card_all.css('h1::text').get()
        item['name'] = name

        item['address_all'] = ' '.join(address_all)
        item['address_all_span'] = ' '.join(address_all_span)

        country = ''
        sity = ''
        index = ''
        index_temp = []
        for i in range(1, count_address_all_span):
            index_temp = address_all_span[i].split(" ")
            if index_temp[0].isdigit():
                index = index_temp[0]
                zapobij = True
                for y in range(1, len(index_temp)):
                    if zapobij:
                        sity = index_temp[y]
                        zapobij = False
                    else:
                        sity = sity + " " + index_temp[y]
                if i == count_address_all_span - 1:
                    country = 'None'
                elif i < count_address_all_span - 1:
                    country = address_all_span[count_address_all_span - 1]
                    if not country:
                        country = 'None'
            else:
                try:
                    str_ind = address_all_span[i].split(",")
                    str_ind_two = str_ind[1].strip().split(" ")
                    if str_ind_two[1].isdigit():
                        index = str_ind_two[1]
                        sity = str_ind[0]
                        if i == count_address_all_span - 1:
                            country = 'None'
                        elif i < count_address_all_span - 1:
                            country = address_all_span[count_address_all_span - 1]
                            if not country:
                                country = 'None'
                except:
                    continue
        
        item['country'] = country
        item['index'] = index
        item['sity'] = sity

        countreview = card_all.css('p.text__373c0__2pB8f.text-color--mid__373c0__3G312.text-align--left__373c0__2pnx_.text-size--large__373c0__1568g::text').get()
        if countreview is not None:
            item['countreview'] = countreview.split(" ")[0]
        else:
            item['countreview'] = '0'
        
        web_tel = card_all.css('div.island__373c0__3fs6U.u-padding-t1.u-padding-r1.u-padding-b1.u-padding-l1.border--top__373c0__19Owr.border--right__373c0__22AHO.border--bottom__373c0__uPbXS.border--left__373c0__1SjJs div.lemon--div__373c0__1mboc.arrange__373c0__UHqhV.gutter-12__373c0__3kguh.vertical-align-middle__373c0__2TQsQ.border-color--default__373c0__2oFDT p::text').getall()
        web_tel_count = len(web_tel)
        if web_tel_count == 1:
            if web_tel[0] == 'Business website':
                item['website'] = card_all.css('div.island__373c0__3fs6U.u-padding-t1.u-padding-r1.u-padding-b1.u-padding-l1.border--top__373c0__19Owr.border--right__373c0__22AHO.border--bottom__373c0__uPbXS.border--left__373c0__1SjJs div.lemon--div__373c0__1mboc.arrange__373c0__UHqhV.gutter-12__373c0__3kguh.vertical-align-middle__373c0__2TQsQ.border-color--default__373c0__2oFDT a::text').get()
                item['phone'] = 'None'
            elif web_tel[0] == 'Phone number':
                item['website'] = 'None'
        elif web_tel_count == 2:
            if web_tel[0] == 'Business website':
                item['website'] = card_all.css('div.island__373c0__3fs6U.u-padding-t1.u-padding-r1.u-padding-b1.u-padding-l1.border--top__373c0__19Owr.border--right__373c0__22AHO.border--bottom__373c0__uPbXS.border--left__373c0__1SjJs div.lemon--div__373c0__1mboc.arrange__373c0__UHqhV.gutter-12__373c0__3kguh.vertical-align-middle__373c0__2TQsQ.border-color--default__373c0__2oFDT a::text').get()
                item['phone'] = 'None'
            elif web_tel[0] == 'Phone number':
                item['website'] = 'None'
                phone = web_tel[1]
                item['phone'] = phone
        elif web_tel_count == 3:
            if web_tel[0] == 'Business website':
                item['website'] = card_all.css('div.island__373c0__3fs6U.u-padding-t1.u-padding-r1.u-padding-b1.u-padding-l1.border--top__373c0__19Owr.border--right__373c0__22AHO.border--bottom__373c0__uPbXS.border--left__373c0__1SjJs div.lemon--div__373c0__1mboc.arrange__373c0__UHqhV.gutter-12__373c0__3kguh.vertical-align-middle__373c0__2TQsQ.border-color--default__373c0__2oFDT a::text').get()
                if web_tel[1] == 'Phone number':
                    phone = web_tel[2]
                    item['phone'] = phone
        elif web_tel_count == 0:
            item['website'] = 'None'
            item['phone'] = 'None'
        
        schedule = card_all.css('tr p::text').getall()
        item['schedule'] = ' '.join(schedule)
        array_attib = []
        for val in card_all.css('div.arrange__373c0__UHqhV.gutter-12__373c0__3kguh.layout-wrap__373c0__34d4b.layout-2-units__373c0__3CiAk ::text').getall() :
            if val != "\xa0" :
                array_attib.append(val) 
        item['array_attib'] = ' '.join(array_attib)
        category =""
        for ittem_cat in card_all.css('span.text__373c0__2pB8f.text-color--normal__373c0__K_MKN.text-align--left__373c0__2pnx_.text-size--large__373c0__1568g a::text').getall():
            if category == "":
                category = ittem_cat
            else:
                category = category + ", " + ittem_cat
        item['category'] = category

        rannge = card_all.css('div.i-stars__373c0__3UQrn::attr(aria-label)').get()
        if rannge is not None:
            item['rannge'] = rannge.strip().split(" ")[0]
        else:
            item['rannge'] = "0"
        
        img_urls = response.css('div.scrollContainer__373c0__2h-gG img::attr(src)').getall()
        if img_urls:
            item['image_urls'] = img_urls
        else:
            img_urls = response.css('div.scrollContainer__373c0__1Y9If img::attr(src)').getall()
            item['image_urls'] = img_urls
        
        self.count_item += 1

        yield item











