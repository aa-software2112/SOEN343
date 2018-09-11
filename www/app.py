from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
	course = 'SOEN343'
	books = [
		{
			'author':'randomly generated author ' + str(random.randint(0,100)) + '',
			'title': 'randomly generated book title ' + str(random.randint(0,100)) + ''

		},
		{
			'author':'randomly generated author ' + str(random.randint(0,100)) + '',
			'title': 'randomly generated book title ' + str(random.randint(0,100)) + ''
		},
		{
			'author':'randomly generated author ' + str(random.randint(0,100)) + '',
			'title': 'randomly generated book title ' + str(random.randint(0,100)) + ''
		}
	]

	return render_template('index.html', course='SOEN343', books=books)

@app.route('/example')
def showObject():
    # creating a dictionnary object on the fly
    dictionary = {"Title":"TIME", "Publisher":"Time (May 13 2008)", "Language":"English", "ISBN-10":1603200185}
    # rendering the template and setting the objToDisplay in the exampleBackendToFrontend.html to the dictionary
    return render_template('exampleBackendToFrontend.html', objToDisplay=dictionary)

if __name__ == "__main__":
    app.run()
