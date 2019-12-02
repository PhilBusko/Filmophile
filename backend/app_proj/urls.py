"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
BACKEND URLS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from django.conf.urls import url, include
from django.views.generic import TemplateView

import movies.views as MV

filmophile_url = [
    # general data
    url(r'^genres/', MV.Genres),

    # data science page
    url(r'^data_history/', MV.DataHistory),
    url(r'^vote_plot/', MV.VotePlot),
    url(r'^analysis_logreg/', MV.AnalysisLogReg),

    # browsing pages
    url(r'^movies_watched/', MV.MoviesWatched),

]

urlpatterns = [
   url(r'^api/movies/', include((filmophile_url, 'movies'))),

   # base template goes last
   url(r'^', TemplateView.as_view(template_name="index.html")),
]

