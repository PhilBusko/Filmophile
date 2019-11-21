"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
WHAT'S ON NETFLIX SCRAPER
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
import sys
import time as TM
import selenium.webdriver as SN
import selenium.webdriver.common.keys as KY
import selenium.webdriver.support as SS

MOVIES_URL = 'https://www.whats-on-netflix.com/library/movies/'


class WhatsOnScraper(object):

    def __init__(self):

        this_path = os.path.abspath(os.path.dirname(__file__))
        if sys.platform == 'darwin': # mac
            driver_path = os.path.join(this_path, 'static/geckodriver_mac')
        else:
            driver_path = os.path.join(this_path, 'static/geckodriver')
        self.driver = SN.Firefox(executable_path=driver_path)
        print(self.driver)


    def setup_scrape(self):

        # virtual display is necessary on live server

        import socket
        host = socket.gethostname()

        if host.startswith('prod'):
            from pyvirtualdisplay import Display
            display = Display(visible=0, size=(1920, 1080))
            display.start()

        # go to page 

        self.driver.get(MOVIES_URL)
        self.driver.maximize_window() 
        TM.sleep(3)

        # stupid popover can appear

        try:
            popover_lm = self.driver.find_element_by_id('onesignal-popover-container')
            button_lm = popover_lm.find_element_by_id('onesignal-popover-cancel-button')
            button_lm.click()
        except:
            pass

        # set number of results

        body_lm = self.driver.find_element_by_css_selector('body')
        body_lm.send_keys(KY.Keys.PAGE_DOWN)

        select_lm = self.driver.find_element_by_name('netflixlist_length')
        select = SS.select.Select(select_lm)

        option_lm_ls = [p for p in select_lm.find_elements_by_tag_name('option')]
        max_option = max([ int(p.get_attribute('value')) for p in option_lm_ls ])
        select.select_by_value(str(max_option))
        

    def scrape_page(self):

       # first for each tr, expose the next tr, which has the actual data 

        tbody_lm = self.driver.find_element_by_xpath('//*[@id="netflixlist"]/tbody')
        row_lm_ls = tbody_lm.find_elements_by_tag_name('tr')

        for row in row_lm_ls:
            expand_lm = row.find_element_by_css_selector('td.details-control.sorting_1')
            expand_lm.click()
            TM.sleep(0.1)

        # second, iterate through expanded table and get data
        # get only the first tr, the expanded rows have 8 more tr's

        movie_ls = []
        row_lm_ls = self.driver.find_elements_by_xpath('//*[@id="netflixlist"]/tbody/tr')

        for idx in range(0, len(row_lm_ls), 2):
            top_row = row_lm_ls[idx]
            bottom_row = row_lm_ls[idx+1]

            #print(top_row.get_attribute('innerHTML'))

            title_tx = top_row.find_elements_by_tag_name('td')[2].text
            year_tx = top_row.find_elements_by_tag_name('td')[3].text
            link_href = bottom_row.find_element_by_tag_name('a').get_attribute('href')
            netflix_tx = link_href.split('/')[-1]

            new_dx = {
                'title': title_tx,
                'year': year_tx,
                'netflix_id': netflix_tx,
            }
            movie_ls.append(new_dx)

        return movie_ls


    def next_page(self):

        next_link = self.driver.find_element_by_id('netflixlist_next')
        classes_tx = next_link.get_attribute('class')

        if 'disabled' not in classes_tx:
            next_link.click()
            TM.sleep(1)
            return True

        return False


    def close(self):
        TM.sleep(5)
        self.driver.quit()
    
