"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DATA MANAGER
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import os, csv, re, json
import pandas as PD
import numpy as NP
import django.db as DB

import app_proj.utility as UT
import movies.models.tables as TB


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DATABASE EDITOR 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class Editor(object):


    @staticmethod
    def DeleteTable(table_name):
        if table_name == 'MasterMovie' or table_name == 'All':
            TB.MasterMovie.objects.all().delete()
        if table_name == 'MovieDB_Load' or table_name == 'All':
            TB.MovieDB_Load.objects.all().delete()
        if table_name == 'Reelgood_Load' or table_name == 'All':
            TB.Reelgood_Load.objects.all().delete()
        if table_name == 'IMDB_Load' or table_name == 'All':
            TB.IMDB_Load.objects.all().delete()


    @staticmethod
    def InsertDictToTable(data_ls, table):
        # data_obj_ls = [MovieDB_Load(**r) for r in data_ls]
        # MovieDB_Load.objects.bulk_create(data_obj_ls)
        data_obj_ls = eval(f"[{table}(**r) for r in data_ls]")
        exec(f"{table}.objects.bulk_create(data_obj_ls, ignore_conflicts=True)")

        # for debugging input data
        # bulk insert is faster

        # for dt in data_ls:
        #     try:
        #         new_mv = IMDB_Load(**dt)
        #         new_mv.save()
        #     except Exception as ex:
        #         print(ex)
        #         print(dt)
        #         print('')
        #         continue


    @staticmethod
    def ToDBColumns(header_ls):
        new_ls = []
        for hdr in header_ls:
            new_col = hdr.replace('_', ' ').title().replace(' ', '')
            new_ls.append(new_col)
        return new_ls


    @staticmethod
    def CSVtoDict(file_path):
        
        if not os.path.isfile(file_path):
            raise Exception(f"CSV file not found: {file_path}")
        
        fhandle = open(file_path, 'r')
        reader = csv.reader(fhandle)
        header_ls = next(reader)            
        header_ls = Editor.ToDBColumns(header_ls)
        data_ls = []

        for row in reader:
            new_dx = {}
            for idx, col in enumerate(header_ls):
                try:
                    new_dx[col] = row[idx] if row[idx] else None
                except Exception as ex:
                    print(ex)
                    print(f'title: {row[0]} error-col: {col}')
                    print('')
                    break
            data_ls.append(new_dx)
  
        fhandle.close()
        return data_ls


    @staticmethod
    def RunMasterMovies():

        # apparently django ORM can only join tables if there is a foreign key relation
        # but these 3 tables are from disparate sources, the relation comes from outside of them
        # so use pandas to join, though it will be expensive to create copies of all 3 tables
        # pandas is better than sql because this join requires tokenizing the titles

        # create and join dataframes
        # joining imdb on id is better than on the token, though the token in 100% for tmdb and reelgood

        moviedb_df = PD.DataFrame(list(MovieDB_Load.objects.values()))
        reelgood_df = PD.DataFrame(list(Reelgood_Load.objects.values()))
        imdb_df = PD.DataFrame(list(IMDB_Load.objects.values()))

        def GetJoinToken(row):
            title = row['Title']
            year = row['Year']
            token = re.sub(r'[#,:"/=&¡!?\-\.\'\(\)\s]', '', title).lower()
            token = token[:12] if len(token) > 12 else token
            token = f'{token}_{year}'
            return token

        moviedb_df['join_token'] = moviedb_df.apply(GetJoinToken, axis=1)
        reelgood_df['join_token'] = reelgood_df.apply(GetJoinToken, axis=1)
        #return moviedb_df[['Title', 'Year', 'join_token']]

        moviedb_df.columns = [f'{c}_tmdb' for c in moviedb_df.columns]
        reelgood_df.columns = [f'{c}_rlgd' for c in reelgood_df.columns]
        imdb_df.columns = [f'{c}_imdb' for c in imdb_df.columns]

        merge_df = PD.merge(moviedb_df, reelgood_df, how='left', left_on='join_token_tmdb', right_on='join_token_rlgd')
        merge_df = PD.merge(merge_df, imdb_df, how='left', left_on='ImdbId_tmdb', right_on='ImdbId_imdb')
        merge_df = merge_df.drop(columns=['id_tmdb', 'Collection_tmdb', 'ImdbId_tmdb', 'join_token_tmdb',
                    'id_rlgd', 'Tags_rlgd', 'join_token_rlgd', 'id_imdb', 'GrossUs_imdb'])
        #return merge_df

        master_ls = []
        for idx, row in merge_df.iterrows():
            master_dx = Editor.GetMasterMovie(row)
            master_ls.append(master_dx)

        return master_ls


    @staticmethod
    def GetMasterMovie(row):
        
        def best_rating(row):
            rlgd_raw = row['Rating_rlgd']
            imdb_raw = row['Rating_imdb']
            rlgd = 0
            imdb = 0

            if rlgd_raw in ['18+ (R)', '16+']: rlgd = 4
            if rlgd_raw == '13+ (PG-13)': rlgd = 3
            if rlgd_raw == '7+ (PG)': rlgd = 2
            if rlgd_raw == 'All (G)': rlgd = 1
            
            if imdb_raw in ['R', 'TV-MA']: imdb = 4
            if imdb_raw in ['PG-13', 'PG', 'TV-14', 'TV-PG', 'GP']: imdb = 3
            if imdb_raw in ['TV-Y7']: imdb = 2
            if imdb_raw in ['G', 'TV-G']: imdb = 1
            if imdb_raw in ['Not Rated', 'Unrated', 'Approved', 'Passed']: imdb = 0

            final = max([rlgd, imdb])

            if final == 4: return 'R'
            if final == 3: return 'PG-13'
            if final == 2: return 'PG'
            if final == 1: return 'G'
            return None

        def best_companies(row):
            tmdb = row['Companies_tmdb']
            imdb = row['Companies_imdb']

            companies = None
            if tmdb and type(tmdb)==str: companies = tmdb
            elif imdb and type(imdb)==str: companies = imdb

            # 'The' in company name is problematic for analysis - remove them all

            if companies is None or type(companies)==float:
                return None

            companies = re.sub(r', The$', '', companies)
            companies = companies.replace(', The ', ', ').replace('The ', ' ')
            companies = companies.replace(', Ltd.', '').replace(', Inc.', '')
            companies = companies.replace('Asylum', 'The Asylum')

            companies = companies.replace('Lions Gate Films', 'Lionsgate')
            companies = companies.replace('Star Cinema – ABS-CBN Film Productions', 'ABS-CBN Films')
            companies = companies.replace('HBO Films', 'HBO').replace('HBO', 'HBO Films')
            companies = companies.replace('BBC Films', 'BBC').replace('BBC', 'BBC Films')
            companies = re.sub(r'\([^)]*\)', '', companies).strip()

            return companies

        def best_country(row):
            # this one is tied between IMDB and TMDB
            tmdb = row['Country_tmdb']
            rlgd = row['Country_rlgd']
            imdb = row['Country_imdb']

            if imdb: return imdb
            if tmdb: return tmdb
            return None

        def best_runtime(row):
            tmdb_raw = row['RunTime_tmdb']
            rlgd_raw = row['Duration_rlgd']
            imdb_raw = row['Duration_imdb']

            try: tmdb = int(tmdb_raw)
            except: tmdb = 0

            try: rlgd = int(rlgd_raw)
            except: rlgd = 0

            try: imdb = int(imdb_raw)
            except: imdb = 0
            
            rt_max = max([tmdb, rlgd, imdb])
            if rt_max: return rt_max
            return None

        def best_crew(row):
            tmdb = row['Crew_tmdb'] 
            imdb1 = row['Directors_imdb'] 
            imdb2 = row['Writers_imdb'] 

            crew_full_ls = tmdb.split(', ') if type(tmdb)==str else []
            crew_full_ls += imdb1.split(', ') if type(imdb1)==str else []
            crew_full_ls += imdb2.split(', ') if type(imdb2)==str else []
            
            series = PD.Series(crew_full_ls)
            counts = series.value_counts()
            crew_ls = []
            for idx, val in counts.items():
                if val >= 2:
                    crew_ls.append(idx)
            return ', '.join(crew_ls) if len(crew_ls) >= 1 else None

        def best_cast(row):
            tmdb = row['Cast_tmdb']
            imdb = row['Actors_imdb']

            if tmdb and imdb == '':
                return tmdb
            if tmdb == '' and imdb:
                return imdb

            cast_full_ls = tmdb.split(', ') if type(tmdb)==str else []
            cast_full_ls += imdb.split(', ') if type(imdb)==str else []
            series = PD.Series(cast_full_ls)
            counts = series.value_counts()
            cast_ls = []
            for idx, val in counts.items():
                if val >= 2:
                    cast_ls.append(idx)
            return ', '.join(cast_ls) if len(cast_ls) >= 1 else None

        def best_poster(row):
            # poster seem very similar from both sources, they are tall
            tmdb = row['Poster_tmdb'] or ''
            rlgd = row['Poster_rlgd'] or ''

            if tmdb: return tmdb
            if rlgd: return rlgd
            return None

        def best_genres(row):
            tmdb = row['Genres_tmdb']
            rlgd = row['Genres_rlgd']
            imdb = row['Genres_imdb']

            if type(tmdb)==float or tmdb is None: tmdb = ''
            if type(rlgd)==float or rlgd is None: rlgd = ''
            if type(imdb)==float or imdb is None: imdb = ''
            
            tmdb = tmdb.replace('Science Fiction', 'Sci-Fi')
            rlgd = rlgd.replace('Action & Adventure', 'Action, Adventure').replace('Science-Fiction', 'Sci-Fi').replace('Musical', 'Music')
            imdb = imdb.replace('Musical', 'Music')

            genre_full_ls = tmdb.split(', ') + rlgd.split(', ') + imdb.split(', ') 
            series = PD.Series(genre_full_ls)
            counts = series.value_counts()
            genre_ls = []
            for idx, val in counts.items():
                if val >= 2:
                    genre_ls.append(idx)
            return ', '.join(genre_ls) if len(genre_ls) >= 1 else None

        def best_synopsis(row):
            tmdb = row['Synopsis_tmdb'] 
            rlgd = row['Synopsis_rlgd'] 
            imdb = row['Synopsis_imdb'] 
            return rlgd

        def best_budget(row):
            tmdb_raw = row['Budget_tmdb'] 
            imdb_raw = row['Budget_imdb'] 

            try: tmdb = int(tmdb_raw)
            except: tmdb = 0

            try: imdb = int(imdb_raw)
            except: imdb = 0

            money_max = max([tmdb, imdb])
            if money_max: return money_max
            return None

        def best_gross(row):
            tmdb_raw = row['Gross_tmdb'] 
            imdb_raw = row['GrossWorldwide_imdb'] 

            try: tmdb = int(tmdb_raw)
            except: tmdb = 0

            try: imdb = int(imdb_raw)
            except: imdb = 0

            money_max = max([tmdb, imdb])
            if money_max: return money_max
            return None

        def aggregate_scores(row):
            # the number of votes on TMDb is 2 orders of magnitude less than IMDB
            # so just keep IMDB scores and votes
            pass

        def aggregate_indeces(row):
            index_dx = json.loads(row['Services_rlgd'])
            imdb_id = row['ImdbId_imdb']
            index_dx['imdb'] = imdb_id
            return json.dumps(index_dx)
            
        master_dx = {
            'Movie_ID': row['TmdbId_tmdb'],
            'Title': row['Title_tmdb'],
            'OriginalTitle': row['OriginalTitle_tmdb'],
            'Year': row['Year_tmdb'],
            'Rating': best_rating(row),
            'Companies': best_companies(row),
            'Country': best_country(row),
            'Language': row['Language_tmdb'],
            'RunTime': best_runtime(row),
            'Crew': best_crew(row),
            'Cast': best_cast(row),
            'Poster': best_poster(row),
            'Genres': best_genres(row),
            'Synopsis': best_synopsis(row),
            'Budget': best_budget(row),
            'Gross': best_gross(row),
            'ScoreImdb': float(row['Score_imdb']) if NP.isnan(row['Score_imdb'])==False else None,
            'VotesImdb': int(row['Votes_imdb']) if NP.isnan(row['Votes_imdb'])==False else None,
            'Indeces': aggregate_indeces(row),
        }

        return master_dx


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DATABASE REPORTER 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class Reporter(object):

    # BROWSE PAGES

    @staticmethod
    def GetTableCounts():


        dict([(name, cls) for name, cls in TB.__dict__.items() if isinstance(cls, type)])



        history_ls = []
        tmdb_total = TB.MovieDB_Load.objects.count()
        imdb_total = TB.IMDB_Load.objects.count()
        reelgood_total = TB.Reelgood_Load.objects.count() 
        master_total = TB.MasterMovie.objects.count()

        new_dx = {
            'Feature': 'Title',
            'TMDB': tmdb_total,
            'IMDB': imdb_total,
            'Reelgood': reelgood_total,
            'Union-All': master_total,
        }
        history_ls.append(new_dx)

        new_dx = {
            'Feature': 'Year',
            'TMDB': tmdb_total,
            'IMDB': imdb_total,
            'Reelgood': reelgood_total,
            'Union-All': master_total,

        }
        history_ls.append(new_dx)

        new_dx = {
            'Feature': 'Rating',
            'TMDB': 0,
            'IMDB': TB.IMDB_Load.objects.filter(Rating__isnull=False).
                    exclude(Rating__in=['Not Rated', 'Unrated', 'Approved', 'Passed']).count(),
            'Reelgood': TB.Reelgood_Load.objects.filter(Rating__isnull=False).count(),
            'Union-All': TB.MasterMovie.objects.filter(Rating__isnull=False).count(),
        }
        history_ls.append(new_dx)



        # normalize the values, done here to simplify the above code

        for row in history_ls:
            row['TMDB'] = round(row['TMDB'] / tmdb_total * 100, 1)
            row['IMDB'] = round(row['IMDB'] / imdb_total * 100, 1)
            row['Reelgood'] = round(row['Reelgood'] / reelgood_total * 100, 1)
            row['Union-All'] = round(row['Union-All'] / master_total * 100, 1)

        return history_ls
