"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
REELGOOD SCRAPER
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
import sys
import time as TM
import re
import json
import selenium.webdriver as SN
import selenium.webdriver.common.keys as KY
import selenium.webdriver.support as SS

LOGIN_URL = 'https://reelgood.com/login'
MOVIE_OFFSET_URL = 'https://reelgood.com/movies?filter-sort=4&offset='
MOVIE_BASE_URL = 'https://reelgood.com/movie/'


class ReelgoodScraper(object):

    def __init__(self):

        self.username = 'phil.busko@gmail.com'
        self.password = 'r33lgood'
        self.current_offset = 0

        # virtual display is necessary on live server

        import socket
        host = socket.gethostname()

        if host.startswith('prod'):

            if sys.platform == 'darwin':
                sys.path.append('/opt/X11/bin/xdpyinfo')

            from pyvirtualdisplay import Display
            display = Display(visible=0, size=(1920, 1080))
            display.start()

        # initialize the driver

        this_path = os.path.abspath(os.path.dirname(__file__))
        if sys.platform == 'darwin': # mac
            driver_path = os.path.join(this_path, 'static/geckodriver_mac')
        else:
            driver_path = os.path.join(this_path, 'static/geckodriver')
        self.driver = SN.Firefox(executable_path=driver_path)
        print(self.driver)


    def log_in(self):

        # go to form page and log in
        # good to login so services are in profile

        self.driver.get(LOGIN_URL)
        self.driver.maximize_window() 
        TM.sleep(1)

        username_lm = self.driver.find_element_by_name('email')
        password_lm = self.driver.find_element_by_name('password')
        submit_lm = self.driver.find_element_by_xpath('//*[text()="Log In"]')

        username_lm.send_keys(self.username)
        password_lm.send_keys(self.password)
        TM.sleep(0.5)
        submit_lm.send_keys(KY.Keys.ENTER)
        TM.sleep(1)
        print(self.driver.current_url)


    # returns false if the next page doesn't have any records
    def to_next_page(self):

        current_url = f'{MOVIE_OFFSET_URL}{self.current_offset}'
        self.driver.get(current_url)
        TM.sleep(2)

        # stupid popups

        try:
            cancel_lm = self.driver.find_element_by_xpath('//*[text()="GOT IT"]')
            cancel_lm.click()
        except:
            pass

        try:
            cancel_lm = self.driver.find_element_by_xpath('//*[text()="DONE"]')
            cancel_lm.click()
        except:
            pass

        try:
            table_lm = self.driver.find_element_by_xpath('//table[@class="css-1179hly"]')
            self.current_offset += 50
            return True
        except: 
            return False


    def get_movie_urls(self):

        url_ls = []
        tbody_lm = self.driver.find_element_by_xpath('//table[@class="css-1179hly"]/tbody')
        row_lm_ls = tbody_lm.find_elements_by_tag_name('tr')

        for row in row_lm_ls:
            cell_lm_ls = row.find_elements_by_tag_name('td')

            link = cell_lm_ls[1].find_element_by_tag_name('a').get_attribute('href')
            title = cell_lm_ls[1].find_element_by_tag_name('a').get_attribute('text')
            year = cell_lm_ls[3].text

            new_dx = {
                'title': title,
                'year': year,
                'reelgood_id': link.split('/')[-1], 
            }
            url_ls.append(new_dx)

        return url_ls


    def get_all_urls(self, limit_nt=None):

        urls_ls = []

        while self.to_next_page():
            urls_ls += self.get_movie_urls()

            if self.current_offset % 500 == 0:
                print(f'offset: {self.current_offset}')

            if limit_nt and self.current_offset >= limit_nt:
                return urls_ls

        return urls_ls


    def get_movie_data(self, reelgood_id):

        # seems driver will throw an error if a singular find_element_ is used but no result is found
        # but it won't throw an erro if the prular is sed and no result found

        # open the movie page

        current_url = f'{MOVIE_BASE_URL}{reelgood_id}'
        self.driver.get(current_url)
        TM.sleep(1)

        try:
            cancel_lm = self.driver.find_element_by_xpath('//*[text()="GOT IT"]')
            cancel_lm.click()
        except:
            pass

        try:
            cancel_lm = self.driver.find_element_by_xpath('//*[text()="DONE"]')
            cancel_lm.click()
        except:
            pass

        # poster 

        poster = None

        pblock_lm = self.driver.find_element_by_class_name('css-dvxtzn')
        poster = pblock_lm.find_element_by_tag_name('img').get_attribute('src')

        # data bar

        title = None
        imdb_score = None
        rt_score = None
        genres = None
        rating = None
        year = None
        duration = None
        tags = None
        country = None

        info_block_lm = self.driver.find_element_by_class_name('css-1jw3688')
        data_bar_lm = info_block_lm.find_element_by_class_name('css-1ss0qk')
        title = info_block_lm.find_element_by_tag_name('h1').text

        try:
            imdb_lm = self.driver.find_element_by_xpath('//*[@title="IMDb Rating"]')
            imdb_score = imdb_lm.find_element_by_class_name('css-xmin1q').text
        except:
            pass

        try:
            rt_lm = self.driver.find_element_by_xpath('//*[@title="Rotten Tomatoes Critic Rating"]')
            rt_score = rt_lm.find_element_by_class_name('css-xmin1q').text
        except:
            pass

        genre_lm_ls = self.driver.find_elements_by_xpath('//span/div/div/a[contains(@href, "/genre/")]')

        if not genre_lm_ls:
            genre_lm_ls = self.driver.find_elements_by_xpath('//span/a[contains(@href, "/genre/")]')

        if genre_lm_ls:
            genre_ls = []
            for gnr in genre_lm_ls:
                genre_ls.append(gnr.get_attribute('text'))
            genres = ', '.join(genre_ls)

        try:
            rating_lm = self.driver.find_element_by_xpath('//*[@title="Maturity rating"]')
            rating = rating_lm.text.replace('Rated:', '').strip()
        except:
            pass

        try:
            meta_lm = data_bar_lm.find_element_by_xpath('//meta[@itemprop="dateCreated"]')
            year = meta_lm.get_attribute('content')[:4]
        except:
            pass

        try:
            meta_lm = data_bar_lm.find_element_by_xpath('//meta[@itemprop="duration"]')
            duration = meta_lm.get_attribute('content')
            dura_rx = r'PT(?:(\d)H)*([\d]+)M'
            matches = re.match(dura_rx, duration)
            hrs = matches.groups()[0]
            mins = matches.groups()[1]
            if hrs:
                duration = int(hrs) * 60 + int(mins)
            else:
                duration = int(mins)
        except:
            pass

        tag_lm_ls = self.driver.find_elements_by_xpath('//span/div/div/a[contains(@href, "/list/")]')

        if not tag_lm_ls:
            tag_lm_ls = self.driver.find_elements_by_xpath('//span/a[contains(@href, "/list/")]')

        if tag_lm_ls:
            tag_ls = []
            for lnk in tag_lm_ls:
                tag_ls.append(lnk.get_attribute('text'))
            tags = ', '.join(tag_ls)

        try:
            country_lm = self.driver.find_element_by_xpath('//span[text()="Country:"]')
            link_lm_ls = country_lm.find_elements_by_tag_name('a')
            country = link_lm_ls[0].text
        except:
            pass

        # synopsis

        synopsis = None

        description_lm = self.driver.find_element_by_xpath('//p[@itemprop="description"]')
        synopsis_ls = description_lm.text.split('\n\n')
        synopsis = synopsis_ls[0]

        # services 

        services = {'reelgood': reelgood_id}

        service_block_lm = self.driver.find_element_by_css_selector('nav.css-1j9eqcs.e1udhou14')
        link_lm_ls = service_block_lm.find_elements_by_tag_name('a')

        for lnk in link_lm_ls:
            href = lnk.get_attribute('href')
            key = None

            if 'amazon' in href:
                key = 'amazon'
                value = href.split('/')[-1].split('?')[0]

            if 'netflix' in href:
                key = 'netflix'
                value = href.split('/')[-1]

            if 'hulu' in href:
                key = 'hulu'
                value = href.split('/')[-1]

            if key:
                services[key] = value

        # staff 

        # big issue with this where the staff grid doesn't fit on the screen, so selenium won't scrape it
        # 1. tried to get elements, move the grid, get more elements -  didn't work because first elements errored out
        # 2. tried to scrape the data, move the grid, scrape the next data - errored saying previous data wasn't available anymore ?
        # 3. tried pyvirtualdisplay - can't get it to work on mac
        # 4. tried to inject css to page to make whole grid fit - got styles to work on regular browser, 
        #    but on selenium was able to set styles with execute_script to execute js, and didn't work for unknown reason
        # 5. can try to get page with requests and scrape with beautifulsoup - don't want this
        # gave up on sraping crew, can get it from other sources

        # crew = None
        # cast = None
        # crew_ls = []
        # cast_ls = []

        # body = self.driver.find_element_by_tag_name('body')
        # body.send_keys(KY.Keys.PAGE_DOWN)
        # TM.sleep(0.1)

        # script = """
        #     var inner_grid_ls = document.getElementsByClassName("ReactVirtualized__Grid__innerScrollContainer");
        #     var staff_grid = inner_grid_ls[0];
        #     staff_grid.style.background = 'green';

        #     var children = staff_grid.children;
        #     for (var c = 0; c < children.length; c++) {
        #         var child = children[c];
        #         child.style.position = 'initial';
        #         child.style.left = (c *20).toString() + 'px';
        #     }
        # """
        # self.driver.execute_script(script)
        # TM.sleep(10)

        # try: 
        #     crew_header_lm = self.driver.find_element_by_xpath('//h2[text()="Cast & Crew"]')
        #     crew_block_lm = crew_header_lm.find_element_by_xpath('.//ancestor::div[starts-with(@class, "css-1v8x7dw")]')
        #     crew_grid_lm = crew_block_lm.find_element_by_class_name('ReactVirtualized__Grid__innerScrollContainer')
        #     forward_lm = crew_block_lm.find_element_by_xpath('.//span[@data-direction="forward"]')

        #     crew_link_lm_ls = crew_grid_lm.find_elements_by_tag_name('a')
        #     more_staff = True

        #     # the crew grid has to be scrolled into view to pick up the links that are off the page,
        #     # so some links end up being duplicated at the end 

        #     while more_staff:
                
        #         # get the current crew data
        #         print(len(crew_link_lm_ls))

        #         for lnk in crew_link_lm_ls:
        #             link_type = lnk.find_element_by_tag_name('h4').text
        #             print(link_type)
        #             staff_name = lnk.find_element_by_tag_name('h3').text

        #             if link_type in ['Director', 'Producer', 'Executive Producer', 'Writer'] and staff_name not in crew_ls:
        #                 crew_ls.append(staff_name)

        #             elif len(cast_ls) <= 2:
        #                 cast_ls.append(staff_name)

        #         # go to next grid view window

        #         try:
        #             forward_lm.click()
        #             TM.sleep(0.1)

        #             crew_header_lm = self.driver.find_element_by_xpath('//h2[text()="Cast & Crew"]')
        #             crew_block_lm = crew_header_lm.find_element_by_xpath('.//ancestor::div[starts-with(@class, "css-1v8x7dw")]')
        #             crew_grid_lm = crew_block_lm.find_element_by_class_name('ReactVirtualized__Grid__innerScrollContainer')
        #             forward_lm = crew_block_lm.find_element_by_xpath('.//span[@data-direction="forward"]')

        #             crew_link_lm_ls = crew_grid_lm.find_elements_by_tag_name('a')
        #             print('crew_ls refreshed')
        #         except: 
        #             more_staff = False

        # except Exception as ex:
        #     crew_link_lm_ls = []
        #     print(f'crew block error: {ex}')

        # crew = ', '.join(crew_ls)
        # cast = ', '.join(cast_ls)

        # assemble and ship 

        movie_dx = {
            'title': title,
            'year': year, 
            'duration': duration,
            'rating': rating,
            'country': country,
            #'crew': crew,
            #'cast': cast,
            'poster': poster,

            'genres': genres,
            'tags': tags,
            'imdb_score': imdb_score,
            'rt_score': rt_score,
            'synopsis': synopsis,

            'services': json.dumps(services),
        }
        return movie_dx


    def close(self):
        TM.sleep(5)
        self.driver.quit()
    
