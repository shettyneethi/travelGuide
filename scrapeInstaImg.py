# # import scrapy
# import os
# import urllib, json
# import urllib.request
# # from selenium import webdriver
# # from selenium.webdriver.support import expected_conditions as EC
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
import pymongo


# # options = webdriver.ChromeOptions() 
# # options.add_argument("start-maximized")
# # options.add_argument('disable-infobars')
# # driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver.exe"))

# for start_url in start_urls:
#     with urllib.request.urlopen(start_url) as url:
#         data = json.loads(url.read().decode())
#         print(data[])

# # class TripAdvisorSpider(scrapy.Spider):
# #     name = "blog"
    
# #     start_urls = []
# #     for l in places:
# #         start_urls.append("https://www.instagram.com/explore/tags/"+l['NAME'].replace(" ","")+"/?__a=1")
    
    
#!/usr/bin/python
# -- coding: utf-8 --
import requests
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json


class Insta_Image_Links_Scraper:

    def getProfilPic(self,loc):
        url = "https://www.instagram.com/explore/tags/"
        
        l = loc.split(" ")
        flag = False

        while(flag==False and len(l)>0):
            tag = "".join(l)
            url = "https://www.instagram.com/explore/tags/"+tag+"/"
            try:

                html = urllib.request.urlopen(url, context=self.ctx).read()
                flag = True
            except:
                l.pop()
        print("url=====",url)
        if(flag == False):
            return ""

        soup = BeautifulSoup(html, 'html.parser')
        script = soup.find('script', text=lambda t: \
                           t.startswith('window._sharedData'))
        page_json = script.text.split(' = ', 1)[1].rstrip(';')
        data = json.loads(page_json)
        profile_pic_url = data['entry_data']['TagPage'][0]['graphql']['hashtag']['profile_pic_url']

        return profile_pic_url
        # for post in data['entry_data']['TagPage'][0]['graphql'
        #         ]['hashtag']['edge_hashtag_to_media']['edges']:
        #     image_src = post['node']['thumbnail_resources'][1]['src']
        #     hs = open(hashtag + '.txt', 'a')
        #     hs.write(image_src + '\n')
        #     hs.close()

    def main(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["DATASET"]
        reviewsCol = mydb["REVIEWS"]

        places = reviewsCol.find({},{"NAME":1})

        for l in places:
            
            profile_pic_url = self.getProfilPic(l['NAME'])
            print(profile_pic_url)
            reviewsCol.update({"NAME": l['NAME']}, {"$set": {"PROFILE_PIC_URL": profile_pic_url}})
            print(reviewsCol.find({"NAME": l['NAME']},{"PROFILE_PIC_URL":1}))

obj = Insta_Image_Links_Scraper()
obj.main()
# #     def parse(self, response):
# #         print("&&&&&&&&&&&&&&&&&&&&&*************************",response.request.url)
# #         print(response.xpath(".//pre/descendant::text()").extract())
#         # data = {}
#         # place_name = str(response.xpath(".//h1[@id='HEADING']/descendant::text()").extract()[0].strip())
#         # data["NAME"] = place_name
#         # print "####################################################################################NAME", place_name
#         # total_rating = response.css("span[class*='ui_bubble_rating']::attr(alt)").extract()[0].strip().split(" ")[0]
#         # data["OVERALL_RATING"] = float(total_rating.strip())
#         # print "#####################################################################################OVERALL_RATING",total_rating
#         # # total_reviews = response.xpath(".//span[@class='reviews_header_count']").extract()[0].strip()
#         # # total_reviews = ''.join(i for i in total_reviews if i.isdigit())
        

#         # try:
#         #     data["LOCATION"] =response.xpath(".//span[@class='locality']/descendant::text()").extract()[0].strip().split(",")[0]
#         # except:
#         #     data["LOCATION"] = place_name

#         # print "++++++++++++++++"+data["LOCATION"]
#         # try:
#         #     last_page = int(response.xpath("//div[@class='unified ui_pagination ']//a[@class='pageNum last taLnk ']/descendant::text()").extract()[0].strip())
#         # except:
#         #     last_page = None
#         # all_reviews = []

#         # url = response.request.url
#         # allPageURL = [url]
        

#         # total_pages = 0
#         # if(last_page is not None):
#         #     total_pages = last_page
#         # cur_page = 1
#         # step = len(response.css("div[class='review-container']::attr(data-reviewid)").extract())
#         # start = step

#         # while(total_pages>=cur_page+1):
#         #     # print(total_pages,cur_page+1)
#         #     mod_place_name = place_name.replace(' ','_')
#         #     new_url = url.split(mod_place_name)
#         #     new_url = new_url[0] + 'or'+str(start)+'-'+ mod_place_name+ new_url[1]
#         #     allPageURL.append(str(new_url))
#         #     start += step
#         #     cur_page +=1


#         # # #commenT THIS MODIFIED

#         # # print self.parseReviewsInPage(response,url)


#         # for link in allPageURL:
#         #     all_reviews += self.parseReviewsInPage(response,link)

#         # data["REVIEW_COUNT"] = len(all_reviews)
#         # data["REVIEWS"] = all_reviews
#         # x = mycol.insert_one(data)
# # driver.close()
#         