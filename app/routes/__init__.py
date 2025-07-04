import openai
openai.api_key = "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"

from flask import Blueprint, render_template, request, redirect, url_for, flash
import feedparser
import pandas as pd
from datetime import datetime, timedelta
import os
from urllib.parse import urlparse

main = Blueprint('main', __name__)

# Global cache variables
cached_feeds = None
cache_timestamp = None

def get_cache_duration():
    """Get cache duration in minutes from config file"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'cache_config.txt')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                duration = int(f.read().strip())
                return duration
        except (ValueError, IOError):
            return 30  # Default to 30 minutes
    return 30  # Default to 30 minutes

def is_cache_valid():
    """Check if cache is still valid"""
    global cache_timestamp
    if cache_timestamp is None:
        return False
    
    cache_duration = get_cache_duration()
    expiry_time = cache_timestamp + timedelta(minutes=cache_duration)
    return datetime.now() < expiry_time

def get_global_filter():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'global_filter.txt')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            pattern = f.read().strip().lower()
            return pattern if pattern else None
    return None

def fetch_feeds_from_sources():
    """Fetch feeds from RSS sources (used for caching)"""
    feeds_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'rss_feeds.txt')
    with open(feeds_file, 'r') as f:
        feed_urls = [line.strip() for line in f if line.strip()]
    
    global_filter = get_global_filter()
    stories = []
    
    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.get('title', 'No Title')
            description = entry.get('description', '')
            
            # Apply global filter
            if global_filter and (global_filter not in title.lower() and global_filter not in description.lower()):
                continue
                
            try:
                published_parsed = getattr(entry, 'published_parsed', None) or getattr(entry, 'updated_parsed', None)
                published_dt = datetime(*published_parsed[:6]) if published_parsed else None
            except Exception:
                published_dt = None

            # Extract image URL
            image_url = None
            if 'media_content' in entry and entry.media_content:
                image_url = entry.media_content[0].get('url')
            elif 'media_thumbnail' in entry and entry.media_thumbnail:
                image_url = entry.media_thumbnail[0].get('url')
            elif 'enclosures' in entry and entry.enclosures:
                image_url = entry.enclosures[0].get('href')

            stories.append({
                'title': title,
                'description': description,
                'link': entry.get('link', ''),
                'published': published_dt,
                'image_url': image_url
            })
    
    if not stories:
        df = pd.DataFrame(columns=['title', 'description', 'link', 'published', 'image_url'])
    else:
        df = pd.DataFrame(stories)
    
    if 'published' in df.columns:
        df = df[df['published'].notnull()]
        df = df.sort_values(by='published', ascending=False, na_position='last')
    
    return df

def get_feeds():
    """Get feeds with caching"""
    global cached_feeds, cache_timestamp
    
    if not is_cache_valid():
        print(f"Cache expired or invalid. Fetching fresh data...")
        cached_feeds = fetch_feeds_from_sources()
        cache_timestamp = datetime.now()
        print(f"Cache refreshed at {cache_timestamp}")
    else:
        print(f"Using cached data from {cache_timestamp}")
    
    return cached_feeds

def get_google_analytics_id():
    """Read Google Analytics ID from file if it exists and is not empty."""
    try:
        with open('google_analytics.txt', 'r') as f:
            ga_id = f.read().strip()
            return ga_id if ga_id else None
    except FileNotFoundError:
        return None
    except Exception:
        return None

@main.route("/", methods=["GET"])
def home():
    df = get_feeds()
    today = datetime.now().date()
    five_days_ago = today - timedelta(days=5)

    min_date = df['published'].min().strftime("%Y-%m-%d") if not df.empty else ''
    max_date = df['published'].max().strftime("%Y-%m-%d") if not df.empty else ''

    start_date = request.values.get('start_date') or five_days_ago.strftime("%Y-%m-%d")
    end_date = request.values.get('end_date') or today.strftime("%Y-%m-%d")
    keyword = request.values.get('keyword', '').strip().lower()

    if start_date:
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            df = df[df['published'] >= start_dt]
        except Exception:
            pass
    if end_date:
        try:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
            df = df[df['published'] < end_dt]
        except Exception:
            pass
    if keyword:
        df = df[df['title'].str.lower().str.contains(keyword) | df['description'].str.lower().str.contains(keyword)]

    stories = df.to_dict(orient='records')
    return render_template(
        "index.html",
        stories=stories,
        start_date=start_date,
        end_date=end_date,
        min_date=min_date,
        max_date=max_date,
        keyword=keyword,
        ga_id=get_google_analytics_id()
    )

def get_domain(url):
    try:
        return urlparse(url).netloc
    except Exception:
        return url

main.add_app_template_filter(get_domain, 'get_domain')

from datetime import datetime

def friendly_time(dt):
    if not dt:
        return "No date"
    now = datetime.now()
    diff = now - dt
    minutes = int(diff.total_seconds() // 60)
    days = diff.days
    if diff.total_seconds() < 3600:
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif days < 20:
        return f"{days} day{'s' if days != 1 else ''} ago"
    else:
        months = days // 30
        if months < 1:
            months = 1
        return f"{months} month{'s' if months != 1 else ''} ago"

main.add_app_template_filter(friendly_time, 'friendly_time')

@main.route("/about")
def about():
    feeds = []
    
    try:
        with open('rss_feeds.txt', 'r') as f:
            feed_urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        feed_urls = []
    
    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            # Use feed URL if title is not available
            title = feed.feed.get('title', url)
            
            feed_info = {
                'url': url,
                'title': title,
                'link': feed.feed.get('link', url),
                'entries_count': len(feed.entries),
                'last_updated': feed.feed.get('updated', 'Not available')
            }
            feeds.append(feed_info)
        except Exception as e:
            # If parsing fails, still show the URL
            feed_info = {
                'url': url,
                'title': url,
                'link': url,
                'entries_count': 0,
                'last_updated': 'Error loading feed'
            }
            feeds.append(feed_info)
    
    return render_template(
        'about.html',
        feeds=feeds,
        ga_id=get_google_analytics_id()
    )