from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_site(url, tag, class_name=None):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        if class_name:
            elements = soup.find_all(tag, class_=class_name)
        else:
            elements = soup.find_all(tag)

        return [el.get_text(strip=True) for el in elements]
    except Exception as e:
        return [f"Error: {str(e)}"]

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        url = request.form['url']
        tag = request.form['tag']
        class_name = request.form['class'] or None
        results = scrape_site(url, tag, class_name)
    return render_template('index.html', results=results)
1
if __name__ == '__main__':
    app.run(debug=True)
