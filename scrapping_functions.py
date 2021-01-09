import re
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
from datetime import datetime
import numpy as np
import pandas as pd
from parse import search
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Scrapper:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.browser = webdriver.Chrome(executable_path = driver_path)
        self.user = ""
        self.pwd = ""

    def get_influencers_world(self):
        """
        Retrieving top 49 World Influencers from Wikipedia
        ---------
        Input : local path to Chrome WebDriver
        ---------
        Outputs : 
            df : DataFrame with influencers' related infos
            df['Links to profile'].tolist() : list of the accounts' links
        """
        from selenium import webdriver
        import time
        browser = self.browser
        user = self.user
        pwd = self.pwd
        driver_path =self.driver_path

        url = "https://fr.m.wikipedia.org/wiki/Liste_des_comptes_Instagram_les_plus_suivis"
        browser.get(url)
        time.sleep(1)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        browser.quit()

        insta_acc_links_int=[]
        names_int=[]
        activity = []
        country=[]
        brand = []

        base = 'https://www.instagram.com/'

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        }

        s = requests.Session()
        s.headers.update(headers)
        r = s.get(url,allow_redirects= False)

        soup_int = BeautifulSoup(r.text, 'html.parser')
        inst_in = soup_int.find('table',attrs={'class':"wikitable sortable"})
        table = inst_in.find_all('tr')[2:]
        del table[2]
        for infl in table:

            info = infl.find_all('td')

            pseudo = info[0].text[1:]
            insta_acc_links_int.append(base + pseudo[:-1] + '/')

            nom_util = info[1].find('a').text
            names_int.append(nom_util)

            act = info[3].text
            activity.append(act[:-1])

            pays = info[4].find_all('a')[-1].text
            country.append(pays)

            marque = info[-1].text
            brand.append(marque[:-1])
        from pandas import DataFrame
        Influencers = {'Links to profile': insta_acc_links_int,
                    'Name': names_int,
                    'Activity': activity,
                    'Country': country,
                    'Brand': brand      
                    }
        df = pd.DataFrame(Influencers, columns=['Links to profile','Name','Activity','Country','Brand'])
        return df,  df['Links to profile'].tolist()

    def connection_instagram(self, instagram_account_link, user_name, password):
        """
        Connecting to instagram and passing connection messages
        ---------
        Input : 
            driver_path : local path to Chrome WebDriver
            instagram_account_link : the link to an instagram account
            user_name : user name of the account used to scrape
            password : password of the account used to scrape
        ---------
        Outputs : None
        """
        browser = self.browser
        user = self.user
        pwd = self.pwd
        browser.get(instagram_account_link)
        cookies_click = browser.find_element_by_xpath("//button[text()='Accepter']")
        cookies_click.click()
        time.sleep(2)
        try:
            login_click = browser.find_element_by_xpath("//button[text()='Se connecter']")
            login_click.click()
            time.sleep(2)
        except: 
            time.sleep(2)

        username_input = browser.find_element_by_css_selector("input[name='username']")
        password_input = browser.find_element_by_css_selector("input[name='password']")

        time.sleep(2)
        username_input.send_keys(user_name)
        time.sleep(1)
        password_input.send_keys(password)

        login_button = browser.find_element_by_xpath("//button[@type='submit']")
        time.sleep(2)
        login_button.click()

        time.sleep(2)

        pass_click = browser.find_element_by_xpath("//button[text()='Plus tard']")
        pass_click.click()
        time.sleep(1)
        return browser

    def get_influencer_posts(self,browser, account_link, pause_time):
        """
        Get links of an influencer's posts and general information about the account
        ---------
        Input : 
            account_link : link to the influencer's account
            pause_time : time (in seconds) to wait for loading when scrolling down the account page
        ---------
        Outputs : 
            df : DataFrame containing the infos (posts links and account general infos)
        """
        browser = browser
        user = self.user
        pwd = self.pwd
        driver_path = self.driver_path

        lien_pub = []
        liens=[]
        noms=[]
        activité = []
        pays=[]
        marques = []
        biographys = []
        nb_posts= []
        followers = []
        followings =[]
        verif_st = []
        publis =[]
        
        time.sleep(6)
        
        browser.get(account_link)

        last_height = browser.execute_script("return document.body.scrollHeight")
        while True:

            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


            time.sleep(pause_time)

            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            body = soup.find('body').find('div').find('section').find('main').find('div').find('article').find('div').find('div')
            pubs = body.find_all('div')
            base = 'https://www.instagram.com'
            for pub in pubs : 
                pub_1 = pub.find_all('a')
                for p in pub_1:
                    p = p['href']
                    publis.append(base + p)
        publis_2 = list(np.unique(publis))
        print(account_link)
        print(len(publis_2))
        time.sleep(10)
        browser.get(account_link)

        try:
            biography_1 = browser.find_element_by_xpath('html/body/div/section/main/div/header/section/div[2]/h1').text
        except:
            biography_1 = ""
        try:
            biography_2 = browser.find_element_by_xpath('html/body/div/section/main/div/header/section/div[2]/span').text
        except:
            biography_2 =""
        biography = biography_1 + biography_2
        print(biography)

        number_of_posts = browser.find_element_by_xpath('html/body/div/section/main/div/header/section/ul/li/span').text
        print(number_of_posts)

        number_of_followers = browser.find_element_by_xpath('html/body/div/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title')
        print(number_of_followers)

        try : 
            number_of_followings = browser.find_element_by_xpath('html/body/div/section/main/div/header/section/ul/li[3]/a/span').text
        except : 
            number_of_followings = 0
        print(number_of_followings)

        is_verified = browser.find_element_by_xpath('html/body/div/section/main/div/header/section/div/div/span').text
        print(is_verified)

        time.sleep(2)
        for pub in publis_2:
            lien_pub.append(pub)
            liens.append(insta_acc_links_int[i])
            noms.append(names_int[i])
            activité.append(activity[i])
            pays.append(country[i])
            marques.append(brand[i])

            biographys.append(biography)
            nb_posts.append(number_of_posts)
            followers.append(number_of_followers)
            followings.append(number_of_followings)
            verif_st.append(is_verified)

        from pandas import DataFrame

        Influencers = {'Links to profile': liens,
                    'Links to publication' : lien_pub,
                        'Name Account/Influencer': noms,
                        'Professional Activity': activité,
                        'Nationality': pays,
                        'Brand': marques,
                        'Account description':  biographys,
                        'Number of posts':  nb_posts,
                        'Number of followers':  followers,
                        'Number of followings':  followings,
                        'Verified Status': verif_st,        
                        }
        df = DataFrame(Influencers, columns= ['Links to profile','Links to publication' , 'Name Account/Influencer','Professional Activity',
                                                'Nationality','Brand','Account description','Number of posts','Number of followers',
                                                'Number of followings','Verified Status'])

        return df

    def get_pub_infos(self, pub_list, driver_path, instagram_account_link, user_name, password): 
        """
        Retrieving informations for each posts of a list of publications
        ---------
        Input : 
            pub_list : List of publications' links
            driver_path : local path to Chrome WebDriver
            instagram_account_link : the link to an instagram account
            user_name : user name of the account used to scrape
            password : password of the account used to scrape
        ---------
        Outputs : 
            df : DataFrame of the collected informations for each post
        """
        browser = self.browser
        user = self.user
        pwd = self.pwd
        
        connection_instagram(driver_path, instagram_account_link, user_name, password)

        caption = []
        number_of_com = []
        number_of_lik = []
        dates = []
        typ = []
        l = []

        for pub in pub_list: 
            try:
                browser.get(pub)
            except:
                browser.quit()
                connection_instagram(driver_path, instagram_account_link, user_name, password)
                browser.get(pub)
            
            try:
                date = browser.find_element_by_xpath('/html/body/div/section/main/div/div/article/div[3]/div[2]/a/time').get_attribute('datetime')
            except:
                time.sleep(10)
                try : 
                    browser.get(pub)
                    date = browser.find_element_by_xpath('/html/body/div/section/main/div/div/article/div[3]/div[2]/a/time').get_attribute('datetime')
                except : 
                    browser.quit()
                    connection_instagram(driver_path, instagram_account_link, user_name, password)
                    browser.get(pub)
                    date = browser.find_element_by_xpath('/html/body/div/section/main/div/div/article/div[3]/div[2]/a/time').get_attribute('datetime')
            
            try:
                try:
                    nb_likes = browser.find_element_by_xpath('html/body/div/section/main/div/div/article/div[3]/section[2]/div/div/button/span').text
                    typ.append("Photo")

                except: 
                    nb_likes= browser.find_element_by_xpath('html/body/div/section/main/div/div/article/div[3]/section[2]/div/span/span').text
                    typ.append("Video")
            except:
                time.sleep(6)
                try : 
                    browser.get(pub)
                    try:
                        nb_likes = browser.find_element_by_xpath('html/body/div/section/main/div/div/article/div[3]/section[2]/div/div/button/span').text
                        typ.append("Photo")
                    except: 
                        nb_likes= browser.find_element_by_xpath('html/body/div/section/main/div/div/article/div[3]/section[2]/div/span/span').text
                        typ.append("Video")
                except : 
                    browser.quit()
                    connection_instagram(driver_path, instagram_account_link, user_name, password)
                    browser.get(pub)
                    try:
                        nb_likes = browser.find_element_by_xpath('html/body/div/section/main/div/div/article/div[3]/section[2]/div/div/button/span').text
                        typ.append("Photo")

                    except: 
                        nb_likes= browser.find_element_by_xpath('html/body/div/section/main/div/div/article/div[3]/section[2]/div/span/span').text
                        typ.append("Video")
            try:
                cap = browser.find_element_by_xpath('html/body/div/section/main/div/div/article/div[3]/div/ul/div/li/div/div/div[2]/span').text
            except:
                cap = "No caption"

            try:
                c_1 = browser.find_element_by_xpath("//*[contains(text(),'edge_media_to_parent_comment')]")
                c = c_1.get_attribute('text')
                co = search(':{"count":{nb},"page_info":',c)
                nb_co = int(co['nb'])
            except:
                nb_co = "No comment"
            
            l.append(pub)
            caption.append(cap)
            number_of_com.append(nb_co)
            number_of_lik.append(nb_likes)
            dates.append(date)

        from pandas import DataFrame

        Influencers = {'Links to publication' : l,
                    'Post description': caption,
                    'Post number of comments': number_of_com,
                    'Post number of likes' : number_of_lik,
                    'Posting date': dates,
                    'Media Type': typ          
                    }

        df = DataFrame(Influencers, columns= ['Links to publication',
                                        'Post description','Post number of comments','Post number of likes',
                                            'Posting date','Media Type'])
        return df

    
