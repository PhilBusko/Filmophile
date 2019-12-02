"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
THE MOVIE DB SCRAPER
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
import sys
import time as TM
import re
import tmdbsimple as MB


class MovieDBHelper(object):


    def __init__(self):
        MB.API_KEY = 'f000577cd45312936e5b58384faa5569'


    def discover_movies(self, year):
        
        movie_ls = []

        date_start = f'{year}-01-01'
        date_end = f'{year}-04-30'
        movie_ls += self.discover_by_period(date_start, date_end)
        
        date_start = f'{year}-05-01'
        date_end = f'{year}-08-31'
        movie_ls += self.discover_by_period(date_start, date_end)
        
        date_start = f'{year}-09-01'
        date_end = f'{year}-12-31'
        movie_ls += self.discover_by_period(date_start, date_end)
        
        return movie_ls


    def discover_by_period(self, date_start, date_end):

        discover = MB.Discover()
        pagination = discover.movie(release_date_gte=date_start, release_date_lte=date_end,
                                    include_adult=False, include_video=False)
        TM.sleep(0.5)

        total_pages = int(pagination['total_pages'])
        total_results = pagination['total_results']
        print(f'results for {date_start} to {date_end}: {total_results} ({total_pages} pages)')

        movie_ls = []

        for pg in range(1, total_pages+1):
            if pg % 20 == 0:
                print(f'page: {pg}')

            results_dx = discover.movie(page=pg,
                                    release_date_gte=date_start, release_date_lte=date_end,
                                    include_adult=False, include_video=False)
            TM.sleep(0.3)
            movies = results_dx['results']

            for mov in movies:
                mov_id = mov['id']
                movie_dx = self.get_movie_by_id(mov_id)
                movie_ls.append(movie_dx)

        return movie_ls


    def get_movie_id(self, title, year):

        # search for movie and inspect results
        # the year helps greatly to resolve ties

        search = MB.Search()
        search_results = search.movie(query=title, primary_release_year=year)
        TM.sleep(0.3)

        # for id 3083, 6223 it seems just taking 1st resolves multiple results
        # but id 11787 has the 2nd result be the true result 
        # so must look for true result  

        if search_results['total_results'] == 0:
            raise Exception(f'No movie found: {title} ({year}).')

        movie_found = None
        
        results = search_results['results']
        title_token = re.sub(r'[#,:"/=&¡!?\-\.\'\(\)]', '', title).lower()
        for res in results:
            found_token = re.sub(r'[#,:"/=&¡!?\-\.\'\(\)]', '', res['title']).lower()
            if title_token == found_token:
                movie_found = res
                break

        if not movie_found:
            raise Exception(f'Movie not in results: {title} ({year}).')

        return movie_found['id']


    def get_movie_by_id(self, tmdb_id):

        movie = MB.Movies(tmdb_id)
        movie_info = movie.info()
        TM.sleep(0.3)
        #return movie_info

        try:
            collection = movie_info['belongs_to_collection']['name']
        except:
            collection = None

        budget = movie_info['budget']
        genres = [g['name'] for g in movie_info['genres']] 
        tmdb_id = movie_info['id']
        imdb_id = movie_info['imdb_id']

        try:
            language = self.convert_iso6391(movie_info['original_language'])
        except:
            lang = movie_info['original_language']
            print(f'language error: {lang} | id: {tmdb_id}')
            language = None

        original_title = movie_info['original_title']
        synopsis = movie_info['overview']
        poster = movie_info['poster_path']

        companies = None
        try:
            companies = movie_info['production_companies'][0]['name']
            if len(movie_info['production_companies']) >= 2:
                companies += ', ' + movie_info['production_companies'][1]['name']
        except: 
            pass

        country = None
        try:
            country = movie_info['production_countries'][0]['name']
        except: 
            pass

        year = movie_info['release_date'][:4]
        gross = movie_info['revenue']
        runtime = movie_info['runtime']
        title = movie_info['title']
        tmdb_score = movie_info['vote_average']
        tmdb_votes = movie_info['vote_count']

        cast = None
        cast_ls = movie.credits()['cast']
        if len(cast_ls) > 0:
            cast = cast_ls[0]['name']
        if len(cast_ls) > 1:
            cast += ', ' + cast_ls[1]['name']
        if len(cast_ls) > 2:
            cast += ', ' + cast_ls[2]['name']

        crew_long_ls = movie.credits()['crew']
        crew_ls = []

        for crw in crew_long_ls:
            if crw['job'] == 'Director':
                crew_ls.append(crw['name'])

        for crw in crew_long_ls:
            if (crw['job'] in ['Producer', 'Director', 'Writer', 'Executive Producer'] and 
                crw['name'] not in crew_ls and len(crew_ls) < 3):
                crew_ls.append(crw['name'])

        # return the movie data

        movie_dx = {
            'title': title,
            'original_title': original_title,
            'year': year,
            #'rating': None,
            'companies': companies,
            'country': country,
            'language': language,
            'run_time': runtime,
            'crew': ', '.join(crew_ls),
            'cast': cast,
            'poster': poster,
            
            'genres': ', '.join(genres),
            'collection': collection,
            'synopsis': synopsis,
            'budget': budget if budget else None,
            'gross': gross if gross else None,
            'score': tmdb_score,
            'votes': tmdb_votes,
            
            'tmdb_id': tmdb_id,
            'imdb_id': imdb_id,
        }

        return movie_dx


    def convert_iso6391(self, code):

        table = [('ab', 'Abkhaz'),
            ('aa', 'Afar'),
            ('af', 'Afrikaans'),
            ('ak', 'Akan'),
            ('sq', 'Albanian'),
            ('am', 'Amharic'),
            ('ar', 'Arabic'),
            ('an', 'Aragonese'),
            ('hy', 'Armenian'),
            ('as', 'Assamese'),
            ('av', 'Avaric'),
            ('ae', 'Avestan'),
            ('ay', 'Aymara'),
            ('az', 'Azerbaijani'),
            ('bm', 'Bambara'),
            ('ba', 'Bashkir'),
            ('eu', 'Basque'),
            ('be', 'Belarusian'),
            ('bn', 'Bengali'),
            ('bh', 'Bihari'),
            ('bi', 'Bislama'),
            ('bs', 'Bosnian'),
            ('br', 'Breton'),
            ('bg', 'Bulgarian'),
            ('my', 'Burmese'),
            ('ca', 'Catalan; Valencian'),
            ('ch', 'Chamorro'),
            ('ce', 'Chechen'),
            ('ny', 'Chichewa; Chewa; Nyanja'),
            ('zh', 'Chinese'),
            ('cn', 'Chinese'),      # Guangzhou dialect
            ('cv', 'Chuvash'),
            ('kw', 'Cornish'),
            ('co', 'Corsican'),
            ('cr', 'Cree'),
            ('hr', 'Croatian'),
            ('cs', 'Czech'),
            ('da', 'Danish'),
            ('dv', 'Divehi; Maldivian;'),
            ('nl', 'Dutch'),
            ('dz', 'Dzongkha'),
            ('en', 'English'),
            ('eo', 'Esperanto'),
            ('et', 'Estonian'),
            ('ee', 'Ewe'),
            ('fo', 'Faroese'),
            ('fj', 'Fijian'),
            ('fi', 'Finnish'),
            ('fr', 'French'),
            ('ff', 'Fula'),
            ('gl', 'Galician'),
            ('ka', 'Georgian'),
            ('de', 'German'),
            ('el', 'Greek, Modern'),
            ('gn', 'Guaraní'),
            ('gu', 'Gujarati'),
            ('ht', 'Haitian'),
            ('ha', 'Hausa'),
            ('he', 'Hebrew (modern)'),
            ('hz', 'Herero'),
            ('hi', 'Hindi'),
            ('ho', 'Hiri Motu'),
            ('hu', 'Hungarian'),
            ('ia', 'Interlingua'),
            ('id', 'Indonesian'),
            ('ie', 'Interlingue'),
            ('ga', 'Irish'),
            ('ig', 'Igbo'),
            ('ik', 'Inupiaq'),
            ('io', 'Ido'),
            ('is', 'Icelandic'),
            ('it', 'Italian'),
            ('iu', 'Inuktitut'),
            ('ja', 'Japanese'),
            ('jv', 'Javanese'),
            ('kl', 'Kalaallisut'),
            ('kn', 'Kannada'),
            ('kr', 'Kanuri'),
            ('ks', 'Kashmiri'),
            ('kk', 'Kazakh'),
            ('km', 'Khmer'),
            ('ki', 'Kikuyu, Gikuyu'),
            ('rw', 'Kinyarwanda'),
            ('ky', 'Kirghiz, Kyrgyz'),
            ('kv', 'Komi'),
            ('kg', 'Kongo'),
            ('ko', 'Korean'),
            ('ku', 'Kurdish'),
            ('kj', 'Kwanyama, Kuanyama'),
            ('la', 'Latin'),
            ('lb', 'Luxembourgish'),
            ('lg', 'Luganda'),
            ('li', 'Limburgish'),
            ('ln', 'Lingala'),
            ('lo', 'Lao'),
            ('lt', 'Lithuanian'),
            ('lu', 'Luba-Katanga'),
            ('lv', 'Latvian'),
            ('gv', 'Manx'),
            ('mk', 'Macedonian'),
            ('mg', 'Malagasy'),
            ('ms', 'Malay'),
            ('ml', 'Malayalam'),
            ('mt', 'Maltese'),
            ('mi', 'Māori'),
            ('mr', 'Marathi (Marāṭhī)'),
            ('mh', 'Marshallese'),
            ('mn', 'Mongolian'),
            ('na', 'Nauru'),
            ('nv', 'Navajo, Navaho'),
            ('nb', 'Norwegian Bokmål'),
            ('nd', 'North Ndebele'),
            ('ne', 'Nepali'),
            ('ng', 'Ndonga'),
            ('nn', 'Norwegian Nynorsk'),
            ('no', 'Norwegian'),
            ('ii', 'Nuosu'),
            ('nr', 'South Ndebele'),
            ('oc', 'Occitan'),
            ('oj', 'Ojibwe, Ojibwa'),
            ('cu', 'Old Church Slavonic'),
            ('om', 'Oromo'),
            ('or', 'Oriya'),
            ('os', 'Ossetian, Ossetic'),
            ('pa', 'Panjabi, Punjabi'),
            ('pi', 'Pāli'),
            ('fa', 'Persian'),
            ('pl', 'Polish'),
            ('ps', 'Pashto, Pushto'),
            ('pt', 'Portuguese'),
            ('qu', 'Quechua'),
            ('rm', 'Romansh'),
            ('rn', 'Kirundi'),
            ('ro', 'Romanian, Moldavan'),
            ('ru', 'Russian'),
            ('sa', 'Sanskrit (Saṁskṛta)'),
            ('sc', 'Sardinian'),
            ('sd', 'Sindhi'),
            ('se', 'Northern Sami'),
            ('sm', 'Samoan'),
            ('sg', 'Sango'),
            ('sr', 'Serbian'),
            ('gd', 'Scottish Gaelic'),
            ('sn', 'Shona'),
            ('si', 'Sinhala, Sinhalese'),
            ('sk', 'Slovak'),
            ('sl', 'Slovene'),
            ('so', 'Somali'),
            ('st', 'Southern Sotho'),
            ('es', 'Spanish; Castilian'),
            ('su', 'Sundanese'),
            ('sw', 'Swahili'),
            ('ss', 'Swati'),
            ('sv', 'Swedish'),
            ('ta', 'Tamil'),
            ('te', 'Telugu'),
            ('tg', 'Tajik'),
            ('th', 'Thai'),
            ('ti', 'Tigrinya'),
            ('bo', 'Tibetan'),
            ('tk', 'Turkmen'),
            ('tl', 'Tagalog'),
            ('tn', 'Tswana'),
            ('to', 'Tonga'),
            ('tr', 'Turkish'),
            ('ts', 'Tsonga'),
            ('tt', 'Tatar'),
            ('tw', 'Twi'),
            ('ty', 'Tahitian'),
            ('ug', 'Uighur, Uyghur'),
            ('uk', 'Ukrainian'),
            ('ur', 'Urdu'),
            ('uz', 'Uzbek'),
            ('ve', 'Venda'),
            ('vi', 'Vietnamese'),
            ('vo', 'Volapük'),
            ('wa', 'Walloon'),
            ('cy', 'Welsh'),
            ('wo', 'Wolof'),
            ('fy', 'Western Frisian'),
            ('xh', 'Xhosa'),
            ('yi', 'Yiddish'),
            ('yo', 'Yoruba'),
            ('za', 'Zhuang, Chuang'),
            ('zu', 'Zulu'),]

        for tpl in table:
            if tpl[0] == code:
                return tpl[1]

        raise Exception(f'Language code not found: {code}')


    @staticmethod
    def GetPosterThumbUrl():
        base_url = 'http://image.tmdb.org/t/p/'
        thumb_url = f'{base_url}w154'
        return thumb_url

