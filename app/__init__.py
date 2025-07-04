from flask import Flask, Blueprint, render_template
import feedparser
import pandas as pd
from datetime import datetime
import os

main = Blueprint('main', __name__)

def get_feeds():
    feeds_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'rss_feeds.txt')
    with open(feeds_file, 'r') as f:
        feed_urls = [line.strip() for line in f if line.strip()]
    stories = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            # Try to parse date, fallback to None
            published = entry.get('published', entry.get('updated', None))
            try:
                published_parsed = entry.published_parsed if 'published_parsed' in entry else entry.updated_parsed
                published_dt = datetime(*published_parsed[:6]) if published_parsed else None
            except Exception:
                published_dt = None
            stories.append({
                'title': entry.get('title', 'No Title'),
                'description': entry.get('description', ''),
                'link': entry.get('link', ''),
                'published': published_dt
            })
    df = pd.DataFrame(stories)
    df = df.sort_values(by='published', ascending=False, na_position='last')
    return df.to_dict(orient='records')

@main.route("/")
def home():
    stories = get_feeds()
    return render_template("index.html", stories=stories)

@main.route("/about")
def about():
    """About page showing feed information"""
    feeds_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'rss_feeds.txt')
    feed_info = []
    
    with open(feeds_file, 'r') as f:
        feed_urls = [line.strip() for line in f if line.strip()]
    
    for url in sorted(feed_urls):  # Sort lexicographically
        try:
            feed = feedparser.parse(url)
            feed_data = {
                'url': url,
                'title': feed.feed.get('title', 'Unknown'),
                'description': feed.feed.get('description', 'No description available'),
                'link': feed.feed.get('link', ''),
                'language': feed.feed.get('language', 'Unknown'),
                'last_updated': feed.feed.get('updated', 'Unknown'),
                'generator': feed.feed.get('generator', 'Unknown'),
                'total_entries': len(feed.entries)
            }
            feed_info.append(feed_data)
        except Exception as e:
            feed_info.append({
                'url': url,
                'title': 'Error loading feed',
                'description': f'Error: {str(e)}',
                'link': '',
                'language': 'Unknown',
                'last_updated': 'Unknown',
                'generator': 'Unknown',
                'total_entries': 0
            })
    
    return render_template("about.html", feed_info=feed_info)

def create_app():
    app = Flask(__name__)

    from .routes import main
    app.register_blueprint(main)

    return app