"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
NETFLIX SCRAPER
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
import sys
import time as TM
import selenium.webdriver as SN
import selenium.webdriver.common.keys as KY

# when something errors : what is best to return ?
# for notebook print is enough
# for webserver ?

class NetflixScraper(object):

    def __init__(self):

        self.username = 'phil.busko@gmail.com'
        self.password = 'netfl1x'
        self.driver = None

        this_path = os.path.abspath(os.path.dirname(__file__))
        if sys.platform == 'darwin': # mac
            driver_path = os.path.join(this_path, 'static/geckodriver_mac')
        else:
            driver_path = os.path.join(this_path, 'static/geckodriver')
        self.driver = SN.Firefox(executable_path=driver_path)
        print(self.driver)


    def log_in(self):

        # virtual display is necessary on live server

        import socket
        host = socket.gethostname()

        if host.startswith('prod'):
            from pyvirtualdisplay import Display
            display = Display(visible=0, size=(1920, 1080))
            display.start()

        # enter credentials and log in

        url = 'https://www.netflix.com/login'
        self.driver.get(url)
        self.driver.maximize_window() 
        TM.sleep(0.1)
        print(self.driver.current_url)

        username_lm = self.driver.find_element_by_id('id_userLoginId')
        password_lm = self.driver.find_element_by_id('id_password')
        submit_lm = self.driver.find_element_by_css_selector('button.btn.login-button.btn-submit.btn-small')

        username_lm.send_keys(self.username)
        password_lm.send_keys(self.password)
        TM.sleep(1)
        submit_lm.send_keys(KY.Keys.ENTER)
        
        TM.sleep(3)
        print(self.driver.current_url)


    def choose_profile(self):
        TM.sleep(1)
        # clicking on the <a profile-link> doesn't work, but the inner div does
        link_lm_ls = self.driver.find_elements_by_class_name('profile-icon')
        first_profile = link_lm_ls[0]
        first_profile.click()


    def enter_search(self, search_term):

        # show the input box

        TM.sleep(3)
        show_search_lm = self.driver.find_element_by_class_name('searchTab')
        show_search_lm.click()

        # type into it and auto search

        search_lm = self.driver.find_element_by_xpath('//*[@class="searchInput"]/input')
        search_lm.send_keys(search_term)


    def get_search_movies():

        pass

    def close(self):
        TM.sleep(10)
        self.driver.quit()
    
