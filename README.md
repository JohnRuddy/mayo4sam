# Mayo4Sam

A Flask-based web application that aggregates Mayo GAA football news from various RSS feeds across the web into a single, convenient location with modern UI and social sharing features.

## Overview

Mayo4Sam is a personal project designed to collect, filter, and display the latest Mayo GAA football stories from multiple Irish sports news sources. The application automatically fetches content from RSS feeds every 30 minutes, applies intelligent filtering, and presents the news in a clean, responsive interface with Mayo GAA colors.

## Features

- **RSS Feed Aggregation**: Automatically collects news from 16+ Irish sports news sources
- **Global Content Filtering**: Filters stories based on configurable keywords (currently set to "Mayo")
- **Intelligent Caching**: Configurable caching system (default: 30 minutes) to improve performance
- **Advanced Search**: Filter stories by date range and keyword search
- **Responsive Design**: Bootstrap-based UI that works on all devices with Mayo GAA color scheme
- **Image Support**: Displays story thumbnails with lazy loading for better performance
- **Social Sharing**: Share stories directly to Facebook, LinkedIn, WhatsApp, X (Twitter)
- **Friendly Time Display**: Shows relative time (e.g., "2 hours ago", "3 days ago")
- **Feed Management**: About page with detailed information about all monitored feeds
- **Performance Optimized**: DNS prefetch, resource preloading, and lazy loading for faster page loads
- **Google Analytics Support**: Optional Google Analytics integration via configuration file
- **Referrer Tracking**: All outbound links tagged with referrer information

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Fonts**: Google Fonts (Inter) for modern typography
- **Icons**: Font Awesome for social media and UI icons
- **Data Processing**: pandas, feedparser
- **Deployment**: Python 3.11+

## Project Structure

```
mayo4sam/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── routes/
│   │   └── __init__.py          # Main routes and business logic
│   ├── static/
│   │   └── images/
│   │       └── placeholder.png  # Default image for stories
│   └── templates/
│       ├── base.html            # Base template with navigation and Mayo GAA styling
│       ├── index.html           # Home page with news feed and social sharing
│       ├── about.html           # About page with feed information and social links
│       └── cache_config.txt     # Cache duration configuration
├── global_filter.txt            # Global keyword filter
├── google_analytics.txt         # Google Analytics tracking ID (optional)
├── rss_feeds.txt               # List of RSS feed URLs
├── requirements.txt            # Python dependencies
├── run.py                      # Application entry point
└── README.md                   # This file
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd mayo4sam
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python run.py
   ```

5. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

## Configuration

### RSS Feeds
Edit [`rss_feeds.txt`](rss_feeds.txt) to add or remove RSS feed URLs. Each URL should be on a separate line.

### Global Filter
Modify [`global_filter.txt`](global_filter.txt) to change the keyword filter. Stories must contain this keyword in their title or description to be displayed.

### Cache Duration
Update [`app/templates/cache_config.txt`](app/templates/cache_config.txt) to change the cache duration in minutes (default: 30 minutes).

### Google Analytics (Optional)
Add your Google Analytics tracking ID to [`google_analytics.txt`](google_analytics.txt) to enable tracking. Leave the file empty to disable analytics.

## Current RSS Sources

The application monitors the following Irish sports news sources:

- Hogan Stand
- Irish Examiner GAA
- Breaking News GAA
- The42.ie GAA
- SportsJoe GAA
- GAA Zone
- Don't Foul
- GAA.ie Official
- Irish Mirror GAA
- Balls.ie GAA
- Dublin GAA
- Mayo GAA Blog
- Independent.ie GAA
- Sky Sports GAA
- RTÉ Sport GAA
- Irish News GAA

## Usage

### Home Page
- Browse the latest Mayo GAA football news with Mayo county colors (red/green gradient)
- Filter stories by date range using the date picker
- Search for specific keywords in story titles or content
- Click on story titles to read the full article on the source website (opens in new tab)
- Share stories directly to social media platforms
- View story count and publication times

### About Page
- View detailed information about all monitored RSS feeds
- See feed statistics including total entries and last update times
- Access direct links to source websites
- Connect with the developer on LinkedIn and GitHub

### Social Features
- Share individual stories to Facebook, LinkedIn, WhatsApp, and X (Twitter)
- All outbound links include referrer tracking
- Modern social media icons with hover effects

## API Routes

- `GET /` - Home page with filtered news stories
- `GET /about` - About page with feed information

## Performance Features

- **DNS Prefetch**: Resolves external domain lookups early
- **Resource Preloading**: Critical CSS and fonts load first
- **Lazy Loading**: Images load only when needed
- **Responsive Images**: Optimized image loading with proper sizing
- **Minified Assets**: Bootstrap and Font Awesome loaded from CDN
- **Caching**: Intelligent caching system reduces server load

## Development

### Key Components

- **[`app/routes/__init__.py`](app/routes/__init__.py)**: Main application logic including feed fetching, caching, and filtering
- **[`app/templates/index.html`](app/templates/index.html)**: Home page template with story display, filtering, and social sharing
- **[`app/templates/base.html`](app/templates/base.html)**: Base template with navigation, Mayo GAA styling, and Google Analytics
- **[`app/templates/about.html`](app/templates/about.html)**: About page template with feed information and social links

### Custom Template Filters

- `friendly_time`: Converts datetime objects to human-readable relative time
- `get_domain`: Extracts domain name from URLs for display
- `striptags`: Removes HTML tags from story descriptions
- `urlencode`: Encodes URLs for social sharing

### Design Features

- **Mayo GAA Colors**: Red and green diagonal gradient branding
- **Inter Font**: Modern Google Font for improved readability
- **Card-based Layout**: Clean, consistent design across all pages
- **Hover Effects**: Subtle animations for better user experience
- **Mobile Responsive**: Works perfectly on all screen sizes

## Contributing

This is a personal project, but suggestions and improvements are welcome. Please feel free to open issues or submit pull requests.

## License

This project is for personal use and educational purposes.

## Acknowledgments

- Built with Flask and Bootstrap for a responsive, modern web experiencel
- Font Awesome for social media icons
- Google Fonts for modern typography

## Contact

If you enjoy this project, feel free to connect:
- **LinkedIn**: [John Pruddy](https://www.linkedin.com/in/johnpruddy/)
- **GitHub**: [JohnRuddy](https://github.com/JohnRuddy)