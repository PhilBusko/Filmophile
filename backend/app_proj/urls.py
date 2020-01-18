"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
BACKEND URLS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from django.conf.urls import url, include
from django.views.generic import TemplateView
import movies.views as MV
import recommend.views as RV


movie_url = [
    # exploration page
    url(r'^years_plot/', MV.YearPlot),
    url(r'^countries_plot/', MV.CountriesPlot),
    url(r'^genres_plot/', MV.GenresPlot),
    url(r'^genresmovie_plot/', MV.GenresMoviePlot),
    url(r'^roi_plot/', MV.RoiPlot),
    url(r'^scoreprofit_plot/', MV.ScoreProfitPlot),
    url(r'^totals_plot/', MV.TotalsPlot),
    url(r'^scores_plot/', MV.ScoresPlot),

    # admin page
    url(r'^table_counts/', MV.TableCounts),
    url(r'^delete_tables/', MV.DeleteTables),
    url(r'^load_csvs/', MV.LoadCsvs),
    url(r'^master_movies/', MV.MasterMovies),
    url(r'^extract_moviedb/', MV.ExtractMovieDb),
    url(r'^extract_reelgood/', MV.ExtractReelgood),
    url(r'^extract_imdb/', MV.ExtractImdb),
]

recommend_url = [
    # browsing pages
    url(r'^genres/', RV.Genres),
    url(r'^recom_levels/', RV.RecomLevels),
    url(r'^movies_watched/', RV.MoviesWatched),
    url(r'^movies_towatch/', RV.MoviesToWatch),

    # data science page
    url(r'^data_history/', RV.DataHistory),
    url(r'^score_plot/', RV.ScorePlot),
    url(r'^restricted_classifiers/', RV.RestrictedClassifiers),

    # admin page
    url(r'^table_counts/', RV.TableCounts),
    url(r'^delete_tables/', RV.DeleteTables),
    url(r'^synthetic_scores/', RV.SyntheticScores),
    url(r'^features_file/', RV.FeaturesFile),
    url(r'^train_predict/', RV.TrainPredict),
]

urlpatterns = [
   url(r'^api/movies/', include((movie_url, 'movies'))),
   url(r'^api/recommend/', include((recommend_url, 'recommend'))),

   # base template goes last
   url(r'^', TemplateView.as_view(template_name="index.html")),
]

