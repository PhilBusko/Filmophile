"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
BACKEND URLS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from django.conf.urls import url, include
from django.views.generic import TemplateView

#import game_rules.views as GV

# use this link for api list
# http://127.0.0.1:8000/api/game_rules

"""
gamerules_url = [
   url(r'^table_summary/', GV.TableSummary),
   url(r'^load_db/', GV.LoadGameRules),

   url(r'^rulebooks_path/', GV.RuleBooksPath),
   url(r'^create_rulebooks/', GV.CreateRuleBooks),
   url(r'^test_html/', GV.TestPDF),
]
"""

urlpatterns = [
   #url(r'^api/game_rules/', include((gamerules_url, 'game_rules'))),

   # base template goes last
   url(r'^', TemplateView.as_view(template_name="index.html")),
]

