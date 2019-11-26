"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
IMDB SCRAPER
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
import sys
import re
import time as TM
import selenium.webdriver as SN
import selenium.webdriver.common.keys as KY

MOVIE_BASE = 'https://www.imdb.com/title/'
IMDB_HOME = 'https://www.imdb.com/'
MOVIE_RX = r'([\w\s\d#,:"/=&¡!?\-\.\']+)\s\(([\d]{4})\)(?:\s\(TV Movie\))*(?:\s\(Video\))*$'


class ImdbScraper(object):


    def __init__(self):

        self.driver = None

        this_path = os.path.abspath(os.path.dirname(__file__))
        this_parent = os.path.dirname(this_path)
        if sys.platform == 'darwin': # mac
            driver_path = os.path.join(this_parent, 'static/geckodriver_mac')
        else:
            driver_path = os.path.join(this_parent, 'static/geckodriver')

        # disable javascript to save time (can check on about:config)

        profile = SN.FirefoxProfile()
        profile.DEFAULT_PREFERENCES['frozen']['javascript.enabled'] = False
        profile.set_preference('app.update.auto', False)
        profile.set_preference('app.update.enabled', False)
        profile.update_preferences()

        self.driver = SN.Firefox(executable_path=driver_path, firefox_profile=profile)
        print(self.driver)


    def open_imdb(self):

        # virtual display is necessary on live server

        import socket
        host = socket.gethostname()

        if host.startswith('prod'):
            from pyvirtualdisplay import Display
            display = Display(visible=0, size=(1920, 1080))
            display.start()

        # enter search criteria and go

        self.driver.get(IMDB_HOME)
        self.driver.maximize_window() 
        TM.sleep(0.3)
        #print(self.driver.current_url)


    # option 1: get movie by id
    def get_movie_by_id(self, imdb_id):

        movie_url = f'{MOVIE_BASE}{imdb_id}'
        self.driver.get(movie_url)
        TM.sleep(0.2)

        return self.get_movie_data()


    # option 2: search for movie by title-year
    def search_any(self, search_tx):

        input_lm = self.driver.find_element_by_id('suggestion-search')
        input_lm.clear()
        TM.sleep(0.1)
        input_lm.send_keys(search_tx)
        TM.sleep(0.1)
        input_lm.send_keys(KY.Keys.ENTER)
        TM.sleep(1)
        #print(self.driver.current_url)


    # option 2 continued
    def map_to_imdb(self, title_streaming):

        mapping_dx = {
            '187': 'One Eight Seven',
            '15-Aug': '15 August',
            '27, el club de los malditos': '27: The Cursed Club', 
            'ABCD 2': 'Any Body Can Dance 2',
            'Alexis Viera: A Story of Surviving': 'Alexis Viera, una historia de superación', 
            'Anarkali of Aarah': 'Anaarkali of Aarah', 
            'Asoka': 'Ashoka the Great',
            'Balto 2: Wolf Quest': 'Balto: Wolf Quest',
            'Balto 3: Wings of Change': 'Balto III: Wings of Change', 
            'Blinky Bill the Movie ': 'Blinky Bill', 
            '': '', 
            '': '', 
            '': '', 
            '': '', 
            '': '', 
            '': '', 
        }

        for key, val in mapping_dx.items():
            if title_streaming == key:
                return val

        return None


    # option 2 continued
    def goto_movie_result(self, title, year):

        # get all search results
        # the order of Titles, Names, Companies result types can change with each search

        titles_section_lm = self.driver.find_element_by_xpath('//*[h3/text()="Titles"]')
        tbody_lm = titles_section_lm.find_element_by_tag_name('tbody')
        row_lm_ls = tbody_lm.find_elements_by_tag_name('tr')

        # loop through each Title result looking for the best match

        def clean_title(title):
            if title:
                title = title.lower()
                title = re.sub(r'[#,:"/=&¡!?\-\.\'\(\)]', '', title)
                return title.strip()
            return None

        for row in row_lm_ls:

            # clean the streaming and imdb data for comparison

            movie_tx = clean_title(title)
            movie_imdb_tx = clean_title(self.map_to_imdb(title))
            year = str(year).strip()

            row_title = None
            row_year = None
            row_aka = None
            result_tx = row.find_element_by_class_name('result_text').text
            result_ls = result_tx.split('\n')

            dedoop = result_ls[0].replace('(I) ', '').replace('(II) ', '').replace('(III) ', '').replace('(IV) ', '')
            #print(dedoop)
            matches = re.match(MOVIE_RX, dedoop)
            if matches:
                row_title = clean_title(matches.group(1))
                row_year = matches.group(2).strip()

            if len(result_ls) > 1:
                row_aka = result_ls[1].replace('aka', '')
                row_aka = clean_title(row_aka)

            # print('')
            # print(movie_tx)
            # print(movie_imdb_tx)
            # print(year)
            # print(row_title)
            # print(row_aka)
            # print(row_year)

            # compare the data, sometimes year can be off by 1 (like a dec release)

            if not row_year:
                continue

            if not (year == row_year or year == str(int(row_year)+1) or year == str(int(row_year)-1)):
                continue

            if movie_tx == row_title or movie_tx == row_aka or movie_imdb_tx == row_title:
                link_lm = row.find_element_by_tag_name('a')
                link_lm.click()
                TM.sleep(0.5)
                return True

        return False


    # both options use this to get the data
    def get_movie_data(self):

        # assumes that the browser is already on movie page

        imdb_id = self.driver.current_url.split('/')[-2]

        # title block

        title_imdb = None
        title_original = None
        year = None

        title_lm = self.driver.find_element_by_class_name('title_wrapper')
        h1_tx = title_lm.find_element_by_tag_name('h1').text

        matches = re.match(MOVIE_RX, h1_tx)
        if matches:
            title_imdb = matches.group(1)
            year = matches.group(2)
        else:
            raise Exception(f'get_movie_data(): title error: {imdb_id}')

        try:
            original_tx = title_lm.find_element_by_class_name('originalTitle').text
            title_original = re.sub(r'\([^)]*\)', '', original_tx).strip()
        except:
            pass
        
        # title subtext block

        rating = None
        duration = None
        genres = None

        subtext_tx = title_lm.find_element_by_class_name('subtext').text
        subtext_ls = subtext_tx.split('|')

        if len(subtext_ls) == 4:
            rating = subtext_ls[0].strip()
            duration_raw = subtext_ls[1].strip()
            genres = subtext_ls[2].strip()

        if len(subtext_ls) == 3:
            duration_raw = subtext_ls[0].strip()
            genres = subtext_ls[1].strip()

        if len(subtext_ls) == 2:
            genres = subtext_ls[0].strip()

        try:
            matches = re.match(r'(?:(\d)h\s)*([\d]+)min', duration_raw)
            hrs = matches.groups()[0]
            mins = matches.groups()[1]
            if hrs:
                duration = int(hrs) * 60 + int(mins)
            else:
                duration = int(mins)
        except:
            pass

        # score block

        score = None
        votes = None

        try:
            score_block_lm = self.driver.find_element_by_class_name('imdbRating')
            score = score_block_lm.find_element_by_class_name('ratingValue').find_element_by_tag_name('strong').text
            votes = score_block_lm.find_element_by_tag_name('a').text.replace(',', '')
        except:
            pass

        # synopsis & credits

        synopsis = None
        directors = None
        writers = None
        actors = None

        summary_lm = self.driver.find_element_by_class_name('plot_summary')
        synopsis = summary_lm.find_element_by_class_name('summary_text').text
        synopsis = synopsis.replace('... See full summary »', '').replace('Add a Plot »', '')
        credit_lm_ls = summary_lm.find_elements_by_class_name('credit_summary_item')

        for crd in credit_lm_ls:
            try:
                credit_type = crd.find_element_by_tag_name('h4').text.strip()
            except: 
                continue

            if credit_type in ['Director:', 'Directors:']:
                directors = crd.text.replace('Director:', '').replace('Directors:', '')
                directors = directors.split('|')[0]
                directors = re.sub(r'\([^)]*\)', '', directors).strip()
            elif credit_type in ['Writer:', 'Writers:']:
                writers = crd.text.replace('Writer:', '').replace('Writers:', '')
                writers = writers.split('|')[0]
                writers = re.sub(r'\([^)]*\)', '', writers).strip()
            elif credit_type == 'Stars:':
                actors = crd.text.replace('Stars:', '')
                actors = actors.split('|')[0].strip()

        # country, box office, company

        country = None
        language = None
        budget = None
        gross_us = None
        gross_worldwide = None
        companies = None

        details_lm = self.driver.find_element_by_id('titleDetails')
        blocks_lm_ls = details_lm.find_elements_by_class_name('txt-block')

        for blk in blocks_lm_ls:
            try:
                block_type = blk.find_element_by_tag_name('h4').text.strip()
            except: 
                continue

            if block_type == 'Country:':
                country = blk.find_elements_by_tag_name('a')[0].text
            elif block_type == 'Language:':
                language = blk.find_elements_by_tag_name('a')[0].text
            elif block_type == 'Budget:':
                budget = blk.text
            elif block_type == 'Gross USA:':
                gross_us = blk.text
            elif block_type == 'Cumulative Worldwide Gross:':
                gross_worldwide = blk.text
            elif block_type == 'Production Co:':
                links = blk.find_elements_by_tag_name('a')[0:2]
                companies = ', '.join([k.text for k in links])
                companies = companies.replace(', See more', '')

        if budget:
            budget = budget.replace('Budget:', '').replace('$', '').replace(',', '')
            budget = re.sub(r'\([^)]*\)', '', budget).strip()
        if gross_us:
            gross_us = gross_us.replace('Gross USA:', '').replace('$', '').replace(',', '').strip()
        if gross_worldwide:
            gross_worldwide = gross_worldwide.replace('Cumulative Worldwide Gross:', '').replace('$', '').replace(',', '').strip()

        # compile all data and return 

        movie_dx = {
            'imdb_id': imdb_id,
            'title': title_imdb,
            'original_title': title_original,
            'year': year, 
            'rating': rating,
            'companies': companies,
            'country': country,
            'language': language, 
            'duration': duration,
            'directors': directors,
            'writers': writers,
            'actors': actors, 
            'genres': genres, 
            'synopsis': synopsis, 
            'budget': budget, 
            'gross_us': gross_us,
            'gross_worldwide': gross_worldwide, 
            'score': score,
            'votes': votes, 
        }
        return movie_dx
    

    def close(self):
        TM.sleep(1)
        self.driver.quit()

