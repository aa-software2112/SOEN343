from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='SOEN343')

@app.route('/example')
def showObject():
    # creating a dictionnary object on the fly
    dictionary = {"Title":"TIME", "Publisher":"Time (May 13 2008)", "Language":"English", "ISBN-10":1603200185}
    # rendering the template and setting the objToDisplay in the exampleBackendToFrontend.html to the dictionary
    return render_template('exampleBackendToFrontend.html', objToDisplay=dictionary)

if __name__ == "__main__":
    app.run()
