from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from copy import deepcopy
import os.path
from diodberg.core.types import Panel
from diodberg.util.utils import readfile

# TODO: Limit global state in this application.
# TODO: Move d3.js to local installation

class AppState(object):
    """ Maintains some in-memory state for the application.
    """ 
    
    __slots__ = {'__panels'}
    
    def __init__(self):
        self.__panels = dict()

    def __get_panels(self): 
        return self.__panels
    def __set_panels(self, val): 
        self.__panels = val
    def __del_panels(self): 
        del self.__panels

    panels = property(__get_panels, __set_panels, __del_panels, "Route name/ID.")

    def __repr__(self):
        return "AppState"

app = Flask(__name__)
state = AppState()


def is_valid_filename(filename):
    """ Is this a valid local filename?
    """ 
    return path.exists(filename)


@app.route('/', methods=['GET', 'POST'])
def main_page(name = None):
    if request.method == 'GET':
        return render_template('main.html', name = "Get")
    elif request.method == 'POST' and "read" in request.form:
        filename = request.form["filename"]
        if is_valid_filename(filename):
            app.logger.debug("Reading filename: " + filename)
            print filename
            state.panels = deepcopy(readfile(filename))
            return render_template('main.html', name = "Post")
    return render_template('main.html', name = "Else")

@app.route('/debug')
def debug():
    return "Debug page: more right along."

@app.route('/log')
def logging():
    return "Log page: more right along."

def main():
    app.debug = True
    app.run(host = '0.0.0.0')

if __name__ == '__main__':
    main()
