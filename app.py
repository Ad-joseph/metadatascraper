from flask import Flask, request, render_template, jsonify, send_file
from scraper import scrape, save_to_csv

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def do_scrape():
    urls = request.json.get('urls', [])
    data = [scrape(url) for url in urls]
    save_to_csv(data)
    return jsonify(data)

@app.route('/download')
def download():
    return send_file('scraped_data.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
