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

    # statistics page
    url(r'^totals_plot/', MV.TotalsPlot),
    url(r'^scores_plot/', MV.ScoresPlot),

    # data science page
    url(r'^data_history/', MV.DataHistory),
    url(r'^vote_plot/', MV.VotePlot),
    url(r'^analysis_logreg/', MV.AnalysisLogReg),

    # browsing pages
    url(r'^movies_watched/', MV.MoviesWatched),
    url(r'^movies_towatch/', MV.MoviesToWatch),
]

urlpatterns = [
   url(r'^api/movies/', include((filmophile_url, 'movies'))),

   # base template goes last
   url(r'^', TemplateView.as_view(template_name="index.html")),
]

