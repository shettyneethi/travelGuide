import scrapy
import os
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pymongo


options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_argument('disable-infobars')
driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver.exe"))
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["DATASET"]
mycol = mydb["REVIEWS"]


class TripAdvisorSpider(scrapy.Spider):
    name = "blog"
    start_urls = ['https://www.tripadvisor.com/AttractionProductReview-g33388-d13000536-Rocky_Mountain_National_Park_Tour-Denver_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g60776-d117416-Reviews-Colorado_National_Monument-Fruita_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33388-d3038683-Reviews-History_Colorado_Center-Denver_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g671305-d2156150-Reviews-Colorado_Provencal-Rustrel_Vaucluse_Provence_Alpes_Cote_d_Azur.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33388-d1418676-Reviews-Colorado_Convention_Center-Denver_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33388-d128648-Reviews-Colorado_State_Capitol-Denver_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33379-d263293-Reviews-Cripple_Creek_Victor_Narrow_Gauge_Railroad-Cripple_Creek_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g29135-d1117911-Reviews-Cumbres_Toltec_Scenic_Railroad-Antonito_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33440-d263359-Reviews-Georgetown_Loop_Historic_Railroad-Georgetown_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g29129-d657079-Reviews-Rio_Grande_Scenic_Railroad-Alamosa_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33561-d534432-Reviews-Tiny_Town-Morrison_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33520-d534340-Reviews-Leadville_Colorado_Southern_Railroad-Leadville_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33397-d196341-Reviews-Durango_and_Silverton_Narrow_Gauge_Railroad_and_Museum-Durango_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33564-d1869603-Reviews-Carousel_of_Happiness-Nederland_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33537-d143457-Reviews-Cave_of_the_Winds_Mountain_Park-Manitou_Springs_El_Paso_County_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33344-d534497-Reviews-North_Pole_Santa_s_Workshop-Cascade_El_Paso_County_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33446-d116239-Reviews-Glenwood_Caverns_Adventure_Park-Glenwood_Springs_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33431-d2043754-Reviews-Colorado_Adventure_Park-Fraser_Grand_County_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g60945-d2172615-Reviews-Estes_Park_Ride_A_Kart_Cascade_Creek_Mini_Golf-Estes_Park_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g143048-d3592530-Reviews-Emerald_Lake_Trail-Rocky_Mountain_National_Park_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33446-d258799-Reviews-Hanging_Lake_Trail-Glenwood_Springs_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g29141-d270464-Reviews-Maroon_Lake_Scenic_Trail-Aspen_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33581-d640977-Reviews-Yankee_Boy_Basin-Ouray_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33364-d104028-Reviews-Pikes_Peak-Colorado_Springs_El_Paso_County_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33537-d4302991-Reviews-Manitou_Springs_Incline-Manitou_Springs_El_Paso_County_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g29141-d270467-Reviews-Rio_Grande_Trail-Aspen_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33584-d2335211-Reviews-Piedra_River_Trail-Pagosa_Springs_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33667-d212353-Reviews-Bear_Creek_Falls-Telluride_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33524-d560020-Reviews-Roxborough_State_Park-Littleton_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33327-d3547960-Reviews-McCullough_Gulch-Breckenridge_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33485-d1856914-Reviews-St_Mary_s_Glacier-Idaho_Springs_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33657-d3510009-Reviews-Yampa_River_Core_Trail-Steamboat_Springs_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g60900-d144953-Reviews-Petroglyph_Point_Hike-Mesa_Verde_National_Park_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33423-d2264599-Reviews-Horsetooth_Mountain_Open_Space-Fort_Collins_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33581-d2229735-Reviews-Perimeter_Trail-Ouray_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33676-d219595-Reviews-Booth_Falls_Trail-Vail_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g143048-d107762-Reviews-Bear_Lake_Trailhead-Rocky_Mountain_National_Park_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33397-d280000-Reviews-Animas_River_Trail-Durango_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33530-d3460375-Reviews-Devil_s_Backbone_Nature_Trail-Loveland_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33340-d2282167-Reviews-Tunnel_Drive-Canon_City_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33364-d7280427-Reviews-Seven_Bridges_Trail-Colorado_Springs_El_Paso_County_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g29141-d211568-Reviews-Crater_Lake_Trail-Aspen_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33581-d3156084-Reviews-Lower_Cascade_Trail_and_Falls-Ouray_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g143048-d3198432-Reviews-Adams_Falls_Trail-Rocky_Mountain_National_Park_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33364-d534483-Reviews-Palmer_Park-Colorado_Springs_El_Paso_County_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33620-d3320720-Reviews-Last_Dollar_Road-Ridgway_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33324-d7953113-Reviews-Mount_Sanitas_Trail-Boulder_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33450-d622951-Reviews-Canyon_View_Park-Grand_Junction_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33646-d212549-Reviews-Ice_Lakes_Trail-Silverton_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g143014-d145009-Reviews-Black_Canyon_of_the_Gunnison_National_Park-Black_Canyon_Of_The_Gunnison_National_P.html',
                    'https://www.tripadvisor.com/Attraction_Review-g33397-d214559-Reviews-San_Juan_National_Forest-Durango_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g60841-d9800243-Reviews-Great_Sand_Dunes_National_Park-Mosca_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g60740-d145438-Reviews-Gunnison_National_Forest-Gunnison_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g60857-d102614-Reviews-Hovenweep_National_Monument-Cortez_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g60740-d143112-Reviews-Curecanti_National_Recreation_Area-Gunnison_Colorado.html',
                    'https://www.tripadvisor.com/Attraction_Review-g60804-d143125-Reviews-Florissant_Fossil_Beds_National_Monument-Florissant_Colorado.html']
    
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
        total_reviews = response.xpath(".//span[@class='reviews_header_count']").extract()[0].strip()
        total_reviews = ''.join(i for i in total_reviews if i.isdigit())
        data["REVIEW_COUNT"] = int(total_reviews.strip())

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
        start = 5

        while(total_pages>=cur_page+1):
            # print(total_pages,cur_page+1)
            mod_place_name = place_name.replace(' ','_')
            new_url = url.split(mod_place_name)
            new_url = new_url[0] + 'or'+str(start)+'-'+ mod_place_name+ new_url[1]
            allPageURL.append(str(new_url))
            start += 5
            cur_page +=1


        # #commenT THIS MODIFIED

        # print self.parseReviewsInPage(response,url)


        for link in allPageURL:
            all_reviews += self.parseReviewsInPage(response,link)

        data["REVIEWS"] = all_reviews
        x = mycol.insert_one(data)
# driver.close()
        