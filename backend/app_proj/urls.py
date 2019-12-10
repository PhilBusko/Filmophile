"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
BACKEND URLS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from django.conf.urls import url, include
from django.views.generic import TemplateView

import movies.views as MV

filmophile_url = [
    # general data
    url(r'^genres/', MV.Genres),
    url(r'^recom_levels/', MV.RecomLevels),

    # browsing pages
    url(r'^movies_watched/', MV.MoviesWatched),
    url(r'^movies_towatch/', MV.MoviesToWatch),

    # exploration page
    url(r'^years_plot/', MV.YearPlot),
    url(r'^countries_plot/', MV.CountriesPlot),
    url(r'^genres_plot/', MV.GenresPlot),
    url(r'^genresmovie_plot/', MV.GenresMoviePlot),
    url(r'^roi_plot/', MV.RoiPlot),
    url(r'^scoreprofit_plot/', MV.ScoreProfitPlot),
    url(r'^totals_plot/', MV.TotalsPlot),
    url(r'^scores_plot/', MV.ScoresPlot),

    # data science page
    url(r'^data_history/', MV.DataHistory),
    url(r'^vote_plot/', MV.VotePlot),
    url(r'^restricted_classifiers/', MV.RestrictedClassifiers),
]

urlpatterns = [
   url(r'^api/movies/', include((filmophile_url, 'movies'))),

   # base template goes last
   url(r'^', TemplateView.as_view(template_name="index.html")),
]

