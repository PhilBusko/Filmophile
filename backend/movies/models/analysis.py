"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
MOVIE ANALYSIS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os, re
import pandas as PD
import numpy as NP

import app_proj.utility as UT
import app_proj.settings as ST
import movies.models.models as MD

FEATURE_PATH = 'movies/data/clean_feature.csv'


class FeatureEngineer(object):


    @staticmethod
    def GetFullDataframe():
        master_ls = MD.MasterMovie.objects.values()
        master_df = PD.DataFrame(master_ls).drop(columns=['id', 'OriginalTitle', 'Poster', 'Synopsis', 'Indeces'])
        master_df['Year'] = master_df['Year'].astype('int')
        master_df['RunTime'] = master_df['RunTime'].astype('Int64')
        master_df['Budget'] = master_df['Budget'].astype('Int64')
        master_df['Gross'] = master_df['Gross'].astype('Int64')
        master_df['VotesImdb'] = master_df['VotesImdb'].astype('Int64')
        return master_df


    @staticmethod
    def GetTypeDataframes(master_df):
        identity_df = master_df[['Movie_ID', 'Title']].copy()
        numeric_df = master_df[['Year', 'RunTime', 'Budget', 'Gross', 'ScoreImdb', 'VotesImdb']].copy()
        onehot_df = master_df[['Rating', 'Companies', 'Country', 'Language', 'Crew', 'Cast']].copy()
        multihot_df = master_df[['Genres']].copy()
        del master_df
        return (identity_df, numeric_df, onehot_df, multihot_df)


    @staticmethod
    def GetSingularMaximums():
        # ok to match total obs because will pca later

        total_obs = MD.UserVotes.objects.all().count()
        total_obs -= 220                        # subtract for country, language, genres, etc
        max_companies = int(total_obs / 2)
        max_crew = int(total_obs / 4)
        max_cast = int(total_obs / 4)
        return max_companies, max_crew, max_cast

    @staticmethod
    def SingularColumn(onehot_df, column, keep_max):

        # get the most frequent values of the column's lists

        full_ls = []
        for idx, row in onehot_df.iterrows():
            entry = row[column]
            if entry is None or entry == 'nan':
                continue
            
            full_ls += entry.split(', ')

        counts = PD.Series(full_ls).value_counts()

        keep_ls = []
        number_items = 0
        for val, cnt in counts.items():
            keep_ls.append(val.strip())
            number_items += 1
            if number_items > keep_max:
                break

        #print(keep_ls)

        # keep only the highest frequency entry found, if any

        def get_keep_only(entries):
            for kp in keep_ls:
                if entries is not None and kp in entries:
                    return kp
            return 'Other'

        onehot_df[column + '_sng'] = onehot_df[column].apply(get_keep_only)
        onehot_df = onehot_df.drop(columns=[column])

        return onehot_df


    @staticmethod
    def MultiHotEncode(multihot_df, column):

        import sklearn.preprocessing as PP
        mlb = PP.MultiLabelBinarizer()

        array_column = column + '_ls'
        multihot_df[array_column] = multihot_df[column].apply(lambda x: x.split(', ') if x else ['None'])
        array_out = mlb.fit_transform( multihot_df[array_column] )

        df_out = PD.DataFrame(data=array_out, columns=mlb.classes_)
        multihot_df = PD.merge(multihot_df, df_out, left_index=True, right_index=True)
        multihot_df = multihot_df.drop(columns=[column, array_column])

        return multihot_df        


    @staticmethod
    def OutputCSV(feature_df):
        save_path = os.path.join(ST.BASE_DIR, FEATURE_PATH)
        feature_df.to_csv(save_path, index=False)


    @staticmethod
    def RunFeatures():

        # this is the same call sequence as in the development notebook

        master_df = FeatureEngineer.GetFullDataframe()

        identity_df, numeric_df, onehot_df, multihot_df = FeatureEngineer.GetTypeDataframes(master_df)
        del master_df

        onehot_df = FeatureEngineer.SingularColumn(onehot_df, 'Companies')
        onehot_df = FeatureEngineer.SingularColumn(onehot_df, 'Crew')
        onehot_df = FeatureEngineer.SingularColumn(onehot_df, 'Cast')
        onehot_dummy_df = PD.get_dummies(onehot_df, columns=['Rating', 'Country', 'Language', 'Companies_sng',
            'Crew_sng', 'Cast_sng'], drop_first=True, dummy_na=False)

        multihot_dummy_df = FeatureEngineer.MultiHotEncode(multihot_df, 'Genres')

        feature_df = PD.concat([identity_df, numeric_df, onehot_dummy_df, multihot_dummy_df], axis=1)

        FeatureEngineer.OutputCSV(feature_df)

