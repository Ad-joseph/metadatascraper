from flask import Flask, request, render_template, jsonify
from scraper import scrape

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def do_scrape():
    urls = request.json.get('urls', [])
    data = [scrape(url) for url in urls]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
