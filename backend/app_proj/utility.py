"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
APP-PROJ UTILITY
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# os.path.join(UT.BASE_DIR, <file_name>) : <file_name> must not start with /
# BASE_DIR is /backend/


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
LOGGING
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import datetime
import logging
prog_lg = logging.getLogger('progress')
excp_lg = logging.getLogger('exception')
file_lg = logging.getLogger('filelogger')

class SimpleFmt(logging.Formatter):
    def format(self, record):
        msg = "\n" + "%s -> %s()" % (record.pathname[32:], record.funcName)
        msg += "\n" + super(SimpleFmt, self).format(record) + "\n"
        return msg

class CompleteFmt(logging.Formatter):
    def format(self, record):
        cDate = datetime.datetime.fromtimestamp(record.created)
        frmtDate = cDate.strftime("%Y-%m-%d %H:%M:%S")
        
        msg = "\n" + "%s @ %s" % (record.levelname, frmtDate)
        msg += "\n" + "%s : %s()" % (record.pathname[32:], record.funcName)
        msg += "\n" + super(CompleteFmt, self).format(record) + "\n"
        
        return msg

def ClearLog():
    open('logfile.log', 'w').close()


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
FILE SYSTEM
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os

def GetFileNames(baseDir):
    # baseDir must be an absolute path
    fileNames = []
    for (dirpath, dirnames, filenames) in os.walk(baseDir):
        fileNames.extend(filenames)
        break
    return fileNames

def MakeDir(p_newPath):
    if not os.path.exists(p_newPath):
        os.makedirs(p_newPath)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DATA HELPERS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def ConvertFigureToJson(figure):
    """
    Takes a plotly figure object and converts it to json for frontend.
    """
    import json
    from plotly.utils import PlotlyJSONEncoder

    redata = json.loads(json.dumps(figure.data, cls=PlotlyJSONEncoder))
    relayout = json.loads(json.dumps(figure.layout, cls=PlotlyJSONEncoder))
    fig_json=json.dumps({'data': redata,'layout': relayout})

    return fig_json

