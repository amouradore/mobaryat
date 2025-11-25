from flask import Flask, render_template, jsonify, request, Response, stream_with_context
import os
import sys
import json
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

# Ajouter le dossier parent au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importer les modules nécessaires
from scrapers.kooora_scraper import KooraMatches
from scrapers.yallakora_scraper import YallaKoraScraper
from scrapers.filgoal_scraper import FilgoalScraper
from scrapers.channels_mapping import get_channels_for_competition

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

# Cache simple en mémoire
cache = {}
CACHE_DURATION = timedelta(hours=2)

# Initialiser les scrapers
kooora = KooraMatches()
yallakora = YallaKoraScraper()
filgoal = FilgoalScraper()

def parse_m3u(filename, category):
    """Parse un fichier M3U et retourne la liste des chaînes"""
    channels = []
    current_name = None
    
    filepath = os.path.join(os.path.dirname(__file__), '..', filename)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#EXTINF'):
                    parts = line.split(',', 1)
                    if len(parts) > 1:
                        current_name = parts[1].strip()
                elif line.startswith('http') and current_name:
                    channels.append({
                        'name': current_name,
                        'url': line,
                        'category': category,
                        'logo': f'/static/logos/{category}.png'
                    })
                    current_name = None
    except Exception as e:
        print(f"Erreur lors de la lecture de {filename}: {e}")
    
    return channels

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/channels')
def channels_page():
    return render_template('channels.html')

@app.route('/api/channels')
def get_channels():
    channels = []
    m3u_files = [
        'bein.m3u', 'dazn.m3u', 'espn.m3u', 'elevendazn.m3u',
        'generalsports.m3u', 'mbc.m3u', 'premierleague.m3u',
        'roshnleague.m3u', 'SeriaA.m3u', 'sky_channels.m3u'
    ]
    
    for m3u_file in m3u_files:
        category = m3u_file.replace('.m3u', '').replace('_channels', '')
        channels_list = parse_m3u(m3u_file, category)
        channels.extend(channels_list)
    
    return jsonify(channels)

@app.route('/api/matches/today')
def get_today_matches():
    cache_key = f"matches_{datetime.now().strftime('%Y-%m-%d')}"
    
    if cache_key in cache:
        cached_data, cached_time = cache[cache_key]
        if datetime.now() - cached_time < CACHE_DURATION:
            return jsonify(cached_data)
    
    matches = []
    
    try:
        kooora_matches = kooora.get_today_matches()
        matches.extend(kooora_matches)
    except:
        pass
    
    try:
        yallakora_matches = yallakora.get_today_matches()
        matches.extend(yallakora_matches)
    except:
        pass
    
    try:
        filgoal_matches = filgoal.get_today_matches()
        matches.extend(filgoal_matches)
    except:
        pass
    
    for match in matches:
        if not match.get('channels'):
            comp = match.get('competition', '')
            match['channels'] = get_channels_for_competition(comp)
    
    cache[cache_key] = (matches, datetime.now())
    return jsonify(matches)

@app.route('/proxy/stream')
def proxy_stream():
    stream_url = request.args.get('url')
    
    if not stream_url:
        return jsonify({'error': 'URL manquante'}), 400
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Referer': stream_url
        }
        
        response = requests.get(stream_url, headers=headers, stream=True, timeout=10)
        content_type = response.headers.get('Content-Type', 'application/vnd.apple.mpegurl')
        
        if 'mpegurl' in content_type or stream_url.endswith('.m3u8'):
            m3u8_content = response.text
            
            import re
            from urllib.parse import urljoin
            
            base_url = '/'.join(stream_url.split('/')[:-1]) + '/'
            
            def replace_url(match):
                url = match.group(0)
                if url.startswith('http'):
                    return f"/proxy/stream?url={url}"
                else:
                    absolute_url = urljoin(base_url, url)
                    return f"/proxy/stream?url={absolute_url}"
            
            m3u8_content = re.sub(r'https?://[^\s]+|[^\s]+\.ts|[^\s]+\.m3u8', replace_url, m3u8_content)
            
            return Response(m3u8_content, mimetype='application/vnd.apple.mpegurl')
        
        def generate():
            try:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        yield chunk
            except:
                pass
        
        return Response(stream_with_context(generate()), 
                       mimetype=content_type,
                       headers={
                           'Access-Control-Allow-Origin': '*',
                           'Cache-Control': 'no-cache'
                       })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Export pour Vercel
app = app
