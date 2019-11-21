"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
IMDB SCRAPER
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
import sys
import re
import time as TM
import selenium.webdriver as SN
import selenium.webdriver.common.keys as KY

IMDB_HOME = 'https://www.imdb.com/'
MOVIE_RX = r'([\w\s\d#,:"/=&¡!?\-\.\']+)\s\(([\d]{4})\)(?:\s\(TV Movie\))*(?:\s\(Video\))*$'


class ImdbScraper(object):

    def __init__(self):

        self.driver = None

        this_path = os.path.abspath(os.path.dirname(__file__))
        if sys.platform == 'darwin': # mac
            driver_path = os.path.join(this_path, 'static/geckodriver_mac')
        else:
            driver_path = os.path.join(this_path, 'static/geckodriver')

        self.driver = SN.Firefox(executable_path=driver_path)
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
        TM.sleep(0.1)
        #print(self.driver.current_url)


    def search_any(self, search_tx):

        input_lm = self.driver.find_element_by_id('navbar-query')
        input_lm.clear()
        TM.sleep(0.1)
        input_lm.send_keys(search_tx)
        TM.sleep(0.1)
        input_lm.send_keys(KY.Keys.ENTER)
        TM.sleep(2)
        #print(self.driver.current_url)


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


    def find_movie_result(self, title, year):

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

            print('')
            print(movie_tx)
            print(movie_imdb_tx)
            print(year)
            print(row_title)
            print(row_aka)
            print(row_year)

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


    def get_movie_data(self, title_stream):

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
            print(f'Title not found: {imdb_id}')
            return {}

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
        director = None
        writer = None
        actors = None

        summary_lm = self.driver.find_element_by_class_name('plot_summary')
        synopsis = summary_lm.find_element_by_class_name('summary_text').text.replace('... See full summary »', '')
        credit_lm_ls = summary_lm.find_elements_by_class_name('credit_summary_item')

        for crd in credit_lm_ls:
            try:
                credit_type = crd.find_element_by_tag_name('h4').text.strip()
            except: 
                continue

            if credit_type in ['Director:', 'Directors:']:
                director = crd.find_elements_by_tag_name('a')[0].text
            elif credit_type in ['Writer:', 'Writers:']:
                writer = crd.find_elements_by_tag_name('a')[0].text
            elif credit_type == 'Stars:':
                actors = crd.text

        if director:
            director = director.replace('Director:', '').replace('Directors:', '').split(',')[0]
            director = re.sub(r'\([^)]*\)', '', director).strip()
        if writer: 
            writer = writer.replace('Writer:', '').replace('Writers:', '').split(',')[0]
            writer = re.sub(r'\([^)]*\)', '', writer).strip()
        if actors:
            actors = actors.replace('Stars:', '').split('|')[0].strip()

        # country, box office, company

        country = None
        language = None
        budget = None
        gross_us = None
        gross_worldwide = None
        company = None

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
                company = blk.find_elements_by_tag_name('a')[0].text

        if budget:
            budget = budget.replace('Budget:', '').replace('$', '').replace(',', '')
            budget = re.sub(r'\([^)]*\)', '', budget).strip()
        if gross_us:
            gross_us = gross_us.replace('Gross USA:', '').replace('$', '').replace(',', '').strip()
        if gross_worldwide:
            gross_worldwide = gross_worldwide.replace('Cumulative Worldwide Gross:', '').replace('$', '').replace(',', '').strip()

        # compile all data and return 

        movie_dx = {
            'title_imdb': title_imdb,
            'title_original': title_original,
            'title_stream': title_stream,        
            'year': year, 
            'imdb_id': imdb_id,
            'score': score,
            'votes': votes, 
            'rating': rating,
            'duration': duration,
            'genres': genres, 
            'synopsis': synopsis, 
            'director': director,
            'writer': writer,
            'actors': actors, 
            'country': country,
            'language': language, 
            'budget': budget, 
            'gross_us': gross_us,
            'gross_worldwide': gross_worldwide, 
            'company': company,
        }
        return movie_dx


    def close(self):
        TM.sleep(1)
        self.driver.quit()
    
