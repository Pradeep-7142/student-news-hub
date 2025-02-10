
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import psycopg2
import re
from datetime import datetime
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# --- Flask App Setup ---
app = Flask(__name__)
CORS(app)

# --- Configuration ---
GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"  # Replace with your actual client ID
NEWS_API_KEY = "YOUR_API_KEY"  # Replace with your actual API key
NEWS_API_URL = "https://newsapi.org/v2/everything"
QUERY = "education OR university OR college OR scholarships"
LANGUAGE = "en"

# PostgreSQL Database Configuration
DB_CONFIG = {
    "dbname": "news_portal",
    "user": "your_user",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}

def preprocess_text(text):
    """Clean and preprocess text for storage."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

# --- Save to PostgreSQL ---
def save_to_postgres(data):
    """Save news articles to PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS training_data (
            id SERIAL PRIMARY KEY,
            title TEXT,
            content TEXT,
            description TEXT,
            category TEXT,
            source TEXT,
            author TEXT,
            publish_date TIMESTAMP,
            url TEXT
        );
        '''
        cursor.execute(create_table_query)
        
        insert_query = '''
        INSERT INTO training_data (title, content, description, category, source, author, publish_date, url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        '''
        
        for article in data:
            cursor.execute(insert_query, (
                article["title"], article["content"], article["description"],
                article["category"], article["source"], article["author"],
                article["publish_date"], article["url"]
            ))
        
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Successfully inserted {len(data)} articles.")
    except Exception as e:
        print(f"Error saving to postgres: {e}")

def get_fallback_news():
    """Return fallback news data when API is not available."""
    return [
        {
            "title": "Latest Developments in Educational Technology",
            "content": "New advancements in AI-powered learning platforms...",
            "description": "How AI is transforming education",
            "category": "Technology",
            "source": "Education Weekly",
            "author": "John Doe",
            "publish_date": datetime.utcnow().isoformat(),
            "url": "https://example.com/edu-tech",
            "image": "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=400&h=300&fit=crop"
        },
        {
            "title": "Scholarship Opportunities for STEM Students",
            "content": "New scholarships available for computer science majors...",
            "description": "Financial aid for tech students",
            "category": "Scholarships",
            "source": "University Times",
            "author": "Jane Smith",
            "publish_date": datetime.utcnow().isoformat(),
            "url": "https://example.com/scholarships",
            "image": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=400&h=300&fit=crop"
        },
        {
            "title": "Campus Mental Health Initiatives",
            "content": "Universities implementing new wellness programs...",
            "description": "Supporting student wellbeing",
            "category": "Health",
            "source": "Campus News",
            "author": "Mike Johnson",
            "publish_date": datetime.utcnow().isoformat(),
            "url": "https://example.com/mental-health",
            "image": "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=400&h=300&fit=crop"
        }
    ]

def fetch_news():
    """Fetch news articles from API."""
    if not NEWS_API_KEY or NEWS_API_KEY == "YOUR_API_KEY":
        print("No API key configured, using fallback data")
        return get_fallback_news()

    params = {
        "q": QUERY,
        "language": LANGUAGE,
        "apiKey": NEWS_API_KEY
    }
    try:
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        print(f"Fetched {len(articles)} articles from API.")
        return articles
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return get_fallback_news()

# --- Flask API Endpoint ---
@app.route('/api/news', methods=['GET'])
def get_news():
    try:
        raw_articles = fetch_news()
        processed_articles = []
        
        for article in raw_articles[:6]:  # Limiting to 6 articles
            processed_articles.append({
                "title": preprocess_text(article.get("title", "")),
                "content": preprocess_text(article.get("content", "")),
                "description": preprocess_text(article.get("description", "")),
                "category": "Education",
                "source": article.get("source", {}).get("name", ""),
                "author": article.get("author", ""),
                "publish_date": article.get("publishedAt", datetime.utcnow().isoformat()),
                "url": article.get("url", ""),
                "image": article.get("urlToImage", "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=400&h=300&fit=crop")
            })
        
        try:
            save_to_postgres(processed_articles)
        except Exception as e:
            print(f"Error saving to database: {e}")
        
        return jsonify(processed_articles)
    except Exception as e:
        print(f"Error in get_news: {e}")
        fallback_data = get_fallback_news()
        return jsonify(fallback_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
