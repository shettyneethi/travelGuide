import scrapy
import os
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pymongo


#to run this file: scrapy runspider myScrapy.py

options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_argument('disable-infobars')
driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver.exe"))
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["DATASET"]
mycol = mydb["REVIEWS"]


class TripAdvisorSpider(scrapy.Spider):
    name = "blog"
    state = "COLORADO"
    start_urls = ["https://www.tripadvisor.com/Attraction_Review-g33345-d2303415-Reviews-Rock_Park-Castle_Rock_Colorado.html"]
    def parseReviewsInPage(self,response,url):
        driver.get(url)
        # review_ids= response.css("div[class='review-container']::attr(data-reviewid)").extract()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'review-container')))
        review_ids =  []
        review_containers = driver.find_elements_by_class_name('review-container')

        for i in review_containers:
            review_ids.append(i.get_attribute('data-reviewid'))
        reviews =[]

        for i in review_ids:

            review_details = {}

            rId = "review_"+i.strip()
            print "********************************************REVIEWID:",rId
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, rId)))
            review = driver.find_element_by_id(rId) 
            # ratingDiv = 
            #review_details["RATING"] = int((review.find_element_by_css_selector('.rating.reviewItemInline')).find_element_by_xpath("//*[contains(@class, 'ui_bubble_rating')").get_attribute('class').split("_")[-1])/10
            
            try:
                dateEle = review.find_element_by_css_selector('.prw_rup.prw_reviews_stay_date_hsx')
                review_details["DATE"] = str(dateEle.text.split(":")[1]).strip()
            except:
                try:
                    temp = review.find_element_by_css_selector('.ratingDate.relativeDate').get_attribute('title').split(" ")
                    review_details["DATE"] = str(temp[0]+" "+temp[2])
                except:
                    temp = review.find_element_by_css_selector('.ratingDate').get_attribute('title').split(" ")
                    review_details["DATE"] = str(temp[0]+" "+temp[2])
            
            try:
                memberBadgingNoText = review.find_element_by_css_selector('.memberBadgingNoText')
                s = memberBadgingNoText.find_element_by_css_selector('.ui_icon.thumbs-up-fill')
                review_details["UPVOTES"] = int(memberBadgingNoText.find_elements_by_css_selector('.badgetext')[-1].text.strip())       
            except:
                review_details["UPVOTES"] = 0
            print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",rId
            review_details["SUMMARY"] = review.find_element_by_css_selector('.quote').text.strip().encode("utf-8")
            print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",review_details["SUMMARY"]

            try:
                full_review = WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.taLnk.ulBlueLinks'),'More'))
                # print "I AM HERE*************************"
                review.find_element_by_css_selector('.taLnk.ulBlueLinks').click()
                new_review = driver.find_element_by_id(rId)
                full_review = WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.taLnk.ulBlueLinks'),'Show less'))
            except:
                print "****************************************************************************NO show more for "+rId
            review_details["REVIEW_TEXT"] = driver.find_element_by_xpath("//div[@id='%s']//p[@class='partial_entry']"%rId).text.strip().encode("utf-8")

            reviews.append(review_details)

        return reviews

    def parse(self, response):
        
        data = {}
        place_name = str(response.xpath(".//h1[@id='HEADING']/descendant::text()").extract()[0].strip())
        data["NAME"] = place_name
        print "####################################################################################NAME", place_name
        total_rating = response.css("span[class*='ui_bubble_rating']::attr(alt)").extract()[0].strip().split(" ")[0]
        data["OVERALL_RATING"] = float(total_rating.strip())
        print "#####################################################################################OVERALL_RATING",total_rating
        # total_reviews = response.xpath(".//span[@class='reviews_header_count']").extract()[0].strip()
        # total_reviews = ''.join(i for i in total_reviews if i.isdigit())
        

        try:
            data["LOCATION"] =response.xpath(".//span[@class='locality']/descendant::text()").extract()[0].strip().split(",")[0]
        except:
            data["LOCATION"] = place_name

        print "++++++++++++++++"+data["LOCATION"]
        try:
            last_page = int(response.xpath("//div[@class='unified ui_pagination ']//a[@class='pageNum last taLnk ']/descendant::text()").extract()[0].strip())
        except:
            last_page = None
        all_reviews = []

        url = response.request.url
        allPageURL = [url]
        

        total_pages = 0
        if(last_page is not None):
            total_pages = last_page
        cur_page = 1
        step = len(response.css("div[class='review-container']::attr(data-reviewid)").extract())
        start = step

        while(total_pages>=cur_page+1):
            # print(total_pages,cur_page+1)
            mod_place_name = place_name.replace(' ','_')
            new_url = url.split(mod_place_name)
            new_url = new_url[0] + 'or'+str(start)+'-'+ mod_place_name+ new_url[1]
            allPageURL.append(str(new_url))
            start += step
            cur_page +=1


        # #commenT THIS MODIFIED

        # print self.parseReviewsInPage(response,url)


        for link in allPageURL:
            all_reviews += self.parseReviewsInPage(response,link)

        data["REVIEW_COUNT"] = len(all_reviews)
        data["REVIEWS"] = all_reviews
        data["STATE"] = state
        x = mycol.insert_one(data)
# driver.close()
        