from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_youtube(query):
    # Scrape YouTube search results for a query
    search_url = f"https://www.youtube.com/results?search_query={query}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    videos = soup.find_all('a', {'class': 'yt-simple-endpoint'})
    results = [{'title': video.get('title'), 'url': 'https://www.youtube.com' + video.get('href')} for video in videos if video.get('title')]
    return results

def scrape_amazon(query):
    # Scrape Amazon search results for a query
    search_url = f"https://www.amazon.com/s?k={query}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('div', {'class': 's-main-slot s-result-list s-search-results'})
    results = [{'title': item.get('data-asin'), 'url': 'https://www.amazon.com' + item.get('href')} for item in items if item.get('data-asin')]
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        youtube_results = scrape_youtube(query)
        amazon_results = scrape_amazon(query)
        return render_template('results.html', youtube_results=youtube_results, amazon_results=amazon_results)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
