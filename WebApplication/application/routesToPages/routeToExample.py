from flask import render_template
from application import app
import random 

@app.route('/example')
def showObject():
    # creating a dictionnary object on the fly
    dictionary = {"Title":"TIME", "Publisher":"Time (May 13 2008)", "Language":"English", "ISBN-10":1603200185}
    # rendering the template and setting the objToDisplay in the exampleBackendToFrontend.html to the dictionary
    return render_template('exampleBackendToFrontend.html', objToDisplay=dictionary)

	
