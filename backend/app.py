from flask import Flask, jsonify
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

# You should replace this with your actual News API key
NEWS_API_KEY = "YOUR_API_KEY"
NEWS_API_URL = "https://newsapi.org/v2/everything"

@app.route('/api/news', methods=['GET'])
def get_news():
    try:
        # Get education-related news
        params = {
            'q': 'education OR university OR college',
            'language': 'en',
            'sortBy': 'publishedAt',
            'apiKey': NEWS_API_KEY
        }
        
        response = requests.get(NEWS_API_URL, params=params)
        news_data = response.json()
        
        # Format the response to match our frontend needs
        articles = news_data.get('articles', [])[:6]  # Get first 6 articles
        formatted_news = [
            {
                'title': article['title'],
                'image': article['urlToImage'] or 'https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=400&h=300&fit=crop',
                'category': 'Education'
            }
            for article in articles
        ]
        
        return jsonify(formatted_news)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)