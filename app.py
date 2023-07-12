from flask import Flask, request, render_template, jsonify, send_file, redirect, url_for
from scraper import scrape_all

app = Flask(__name__)

@app.route('/')
def home():
    if request.args.get('embed'):
        return redirect(url_for('embed'))
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def do_scrape():
    urls = request.json.get('urls', [])
    data = scrape_all(urls)
    return jsonify(data)

@app.route('/download')
def download():
    return send_file('scraped_data.csv', as_attachment=True)

@app.route('/embed')
def embed():
    return render_template('embed.html')

if __name__ == '__main__':
    app.run(debug=True)
