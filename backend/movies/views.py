"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
GAME-RULES VIEWS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from rest_framework.decorators import api_view
from rest_framework.response import Response

import app_proj.utility as UT
import movies.models.models as MM


@api_view(["GET"])
def DataHistory(request):
   result_dx = MM.Reporter.GetDataHistory()
   return Response(result_dx)

