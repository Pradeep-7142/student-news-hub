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
GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"  # You'll replace this with your actual client ID
NEWS_API_KEY = "YOUR_API_KEY"
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

@app.route('/api/auth/google', methods=['POST'])
def google_auth():
    try:
        token = request.json.get('token')
        
        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            token, google_requests.Request(), GOOGLE_CLIENT_ID)

        # Get user info from the token
        user_data = {
            'email': idinfo['email'],
            'name': idinfo.get('name', ''),
            'picture': idinfo.get('picture', '')
        }

        # Connect to database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Create users table if it doesn't exist
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            name TEXT,
            college TEXT,
            location TEXT,
            branch TEXT,
            goal TEXT,
            year_of_study TEXT,
            picture TEXT,
            auth_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        cursor.execute(create_table_query)

        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (user_data['email'],))
        existing_user = cursor.fetchone()

        if not existing_user:
            # Insert new user
            insert_query = '''
            INSERT INTO users (email, name, picture, auth_type)
            VALUES (%s, %s, %s, 'google')
            RETURNING id;
            '''
            cursor.execute(insert_query, (
                user_data['email'],
                user_data['name'],
                user_data['picture']
            ))
            user_id = cursor.fetchone()[0]
        else:
            user_id = existing_user[0]

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            'success': True,
            'user': user_data,
            'userId': user_id
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

def fetch_news():
    """Fetch news articles from API."""
    params = {
        "q": QUERY,
        "language": LANGUAGE,
        "apiKey": NEWS_API_KEY
    }
    try:
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        print(f"Fetched {len(articles)} articles.")
        return articles
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

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
        
        # Save fetched articles to PostgreSQL
        if processed_articles:
            save_to_postgres(processed_articles)
        
        return jsonify(processed_articles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
