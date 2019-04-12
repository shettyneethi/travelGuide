import pymongo
import requests
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
import time


class Insta_Image_Links_Scraper:

    def getProfilPic(self,loc):
        url = "https://www.instagram.com/explore/tags/"
        
        l = loc.split(" ")
        profile_pic_url =""

        while(len(l)>0):
            tag = "".join(l)
            url = "https://www.instagram.com/explore/tags/"+tag+"/"

            print("url=====",url)
            try:
                html = urllib.request.urlopen(url, context=self.ctx).read()
                soup = BeautifulSoup(html, 'html.parser')
                script = soup.find('script', text=lambda t: \
                           t.startswith('window._sharedData'))
                page_json = script.text.split(' = ', 1)[1].rstrip(';')
                data = json.loads(page_json)
                profile_pic_url = data['entry_data']['TagPage'][0]['graphql']['hashtag']['profile_pic_url']

                if profile_pic_url.split("/")[3]== "static":
                    l.pop()
                else:   
                    return profile_pic_url
            except:
                l.pop()
        
        return profile_pic_url

    def main(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["DATASET"]
        reviewsCol = mydb["REVIEWS"]

        places = reviewsCol.find({},{"NAME":1})

        # places = [{"NAME":"Rio Grande Trail"}]
        count = 0
        for i in range(places.count()):
            if(count%20==0):
                time.sleep(60)
            profile_pic_url = self.getProfilPic(places[i]['NAME'])
            print(profile_pic_url)
            reviewsCol.update({"NAME": places[i]['NAME']}, {"$set": {"PROFILE_PIC_URL": profile_pic_url}})
            print(reviewsCol.find({"NAME": places[i]['NAME']},{"PROFILE_PIC_URL":1}))
            count += 1



obj = Insta_Image_Links_Scraper()
obj.main()