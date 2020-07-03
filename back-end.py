from flask import Flask, render_template, request
from querySearch import search
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def search_box():
    if request.method == 'POST':
        query = request.form['searchTerm']
        response = search(query)
        hits = response['hits']['hits']
        numResults = len(hits)
        return render_template('index.html', hits=hits, numResults=numResults)
    if request.method == 'GET':
        return render_template('index.html', init='True')


if __name__ == "__main__":
    app.run(debug=True)
