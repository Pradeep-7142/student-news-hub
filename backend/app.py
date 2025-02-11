
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import psycopg2
import re
from datetime import datetime
import random
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import hashlib
import jwt
import secrets

app = Flask(__name__)
CORS(app)

# Configuration
GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"
NEWS_API_KEY = "YOUR_API_KEY"
NEWS_API_URL = "https://newsapi.org/v2/everything"
QUERY = "education OR university OR college OR scholarships"
LANGUAGE = "en"
JWT_SECRET = secrets.token_hex(32)

# Database Configuration
DB_CONFIG = {
    "dbname": "news_portal",
    "user": "your_user",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}

def init_db():
    """Initialize database tables."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Create news table
        create_news_table = '''
        CREATE TABLE IF NOT EXISTS news_articles (
            id SERIAL PRIMARY KEY,
            title TEXT UNIQUE,
            content TEXT,
            description TEXT,
            category TEXT,
            source TEXT,
            author TEXT,
            publish_date TIMESTAMP,
            url TEXT UNIQUE,
            image TEXT
        );
        '''
        
        # Create users table
        create_users_table = '''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT,
            name TEXT,
            google_id TEXT UNIQUE,
            college TEXT,
            location TEXT,
            branch TEXT,
            goal TEXT,
            year_of_study TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        
        cursor.execute(create_news_table)
        cursor.execute(create_users_table)
        conn.commit()
        
    except Exception as e:
        print(f"Database initialization error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def hash_password(password):
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_jwt_token(user_id):
    """Generate JWT token for user authentication."""
    return jwt.encode(
        {'user_id': user_id, 'exp': datetime.utcnow().timestamp() + 86400},
        JWT_SECRET,
        algorithm='HS256'
    )

def save_to_postgres(articles):
    """Save unique news articles to PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        insert_query = '''
        INSERT INTO news_articles (title, content, description, category, source, author, publish_date, url, image)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (url) DO NOTHING;
        '''
        
        for article in articles:
            cursor.execute(insert_query, (
                article["title"],
                article["content"],
                article["description"],
                article["category"],
                article["source"],
                article["author"],
                article["publish_date"],
                article["url"],
                article["image"]
            ))
        
        conn.commit()
        print(f"Successfully processed {len(articles)} articles.")
    except Exception as e:
        print(f"Error saving to postgres: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_random_articles(count=6):
    """Get random articles from database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT title, content, description, category, source, author, 
                   publish_date, url, image 
            FROM news_articles 
            ORDER BY RANDOM() 
            LIMIT %s;
        ''', (count,))
        
        columns = ['title', 'content', 'description', 'category', 'source', 
                  'author', 'publish_date', 'url', 'image']
        articles = []
        
        for row in cursor.fetchall():
            article = dict(zip(columns, row))
            articles.append(article)
        
        return articles
    except Exception as e:
        print(f"Error fetching random articles: {e}")
        return get_fallback_news()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check if email exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (data['email'],))
        if cursor.fetchone():
            return jsonify({"error": "Email already exists"}), 400
        
        # Hash password and insert user
        password_hash = hash_password(data['password'])
        
        insert_query = '''
        INSERT INTO users (email, password_hash, name, college, location, branch, goal, year_of_study)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        '''
        
        cursor.execute(insert_query, (
            data['email'],
            password_hash,
            data['name'],
            data['college'],
            data['location'],
            data['branch'],
            data['goal'],
            data['yearOfStudy']
        ))
        
        user_id = cursor.fetchone()[0]
        conn.commit()
        
        # Generate JWT token
        token = generate_jwt_token(user_id)
        
        return jsonify({
            "success": True,
            "token": token,
            "message": "User registered successfully"
        })
        
    except Exception as e:
        print(f"Signup error: {e}")
        return jsonify({"error": "Registration failed"}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, password_hash FROM users WHERE email = %s",
            (data['email'],)
        )
        
        result = cursor.fetchone()
        if not result:
            return jsonify({"error": "User not found"}), 404
        
        user_id, stored_hash = result
        
        if hash_password(data['password']) != stored_hash:
            return jsonify({"error": "Invalid password"}), 401
        
        token = generate_jwt_token(user_id)
        
        return jsonify({
            "success": True,
            "token": token,
            "message": "Login successful"
        })
        
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({"error": "Login failed"}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/api/auth/google', methods=['POST'])
def google_auth():
    try:
        token = request.json.get('token')
        
        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            token, google_requests.Request(), GOOGLE_CLIENT_ID)
        
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        
        # Get user info from token
        google_id = idinfo['sub']
        email = idinfo['email']
        name = idinfo.get('name', '')
        
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute(
            "SELECT id FROM users WHERE google_id = %s OR email = %s",
            (google_id, email)
        )
        result = cursor.fetchone()
        
        if result:
            user_id = result[0]
            # Update existing user
            cursor.execute(
                "UPDATE users SET google_id = %s, name = %s WHERE id = %s",
                (google_id, name, user_id)
            )
        else:
            # Create new user
            cursor.execute(
                "INSERT INTO users (email, name, google_id) VALUES (%s, %s, %s) RETURNING id",
                (email, name, google_id)
            )
            user_id = cursor.fetchone()[0]
        
        conn.commit()
        
        # Generate JWT token
        token = generate_jwt_token(user_id)
        
        return jsonify({
            "success": True,
            "token": token,
            "message": "Google authentication successful"
        })
        
    except ValueError as e:
        print(f"Token verification error: {e}")
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        print(f"Google auth error: {e}")
        return jsonify({"error": "Authentication failed"}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/api/news', methods=['GET'])
def get_news():
    try:
        # Fetch and save all articles first
        if NEWS_API_KEY and NEWS_API_KEY != "YOUR_API_KEY":
            params = {
                "q": QUERY,
                "language": LANGUAGE,
                "apiKey": NEWS_API_KEY
            }
            response = requests.get(NEWS_API_URL, params=params)
            response.raise_for_status()
            
            raw_articles = response.json().get("articles", [])
            processed_articles = []
            
            for article in raw_articles:
                processed_articles.append({
                    "title": article.get("title", ""),
                    "content": article.get("content", ""),
                    "description": article.get("description", ""),
                    "category": "Education",  # You might want to add category detection logic
                    "source": article.get("source", {}).get("name", ""),
                    "author": article.get("author", ""),
                    "publish_date": article.get("publishedAt", datetime.utcnow().isoformat()),
                    "url": article.get("url", ""),
                    "image": article.get("urlToImage", "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=400&h=300&fit=crop")
                })
            
            # Save all articles to database
            save_to_postgres(processed_articles)
        
        # Get random articles from database
        articles = get_random_articles(6)
        return jsonify(articles)
        
    except Exception as e:
        print(f"Error in get_news: {e}")
        return jsonify(get_fallback_news())

# Initialize database when starting the app
init_db()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
