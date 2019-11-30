"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
BACKEND URLS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from django.conf.urls import url, include
from django.views.generic import TemplateView

import movies.views as MV

filmophile_url = [
    url(r'^data_history/', MV.DataHistory),
    url(r'^vote_plot/', MV.VotePlot),
]

urlpatterns = [
   url(r'^api/movies/', include((filmophile_url, 'movies'))),

   # base template goes last
   url(r'^', TemplateView.as_view(template_name="index.html")),
]

