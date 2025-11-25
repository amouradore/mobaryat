from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import json
import os
from scrapers.kooora_scraper import KooraMatches
from scrapers.yallakora_scraper import YallaKoraMatches
from scrapers.filgoal_scraper import FilgoalMatches
from scrapers.api_football import APIFootballMatches
from scrapers.channels_mapping import add_channels_to_matches

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['JSON_AS_ASCII'] = False

# Initialize scrapers
kooora = KooraMatches()
yallakora = YallaKoraMatches()
filgoal = FilgoalMatches()
api_football = APIFootballMatches()

@app.route('/')
def index():
    """Page d'accueil avec lecteur de flux et matchs du jour"""
    return render_template('index.html')

@app.route('/channels')
def channels():
    """Page des chaînes disponibles"""
    return render_template('channels.html')

@app.route('/api/matches/today')
def get_today_matches():
    """Récupère les matchs du jour depuis plusieurs sources"""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Essayer de récupérer depuis le cache d'abord
        cache_file = f'cache/matches_{today}.json'
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                return jsonify(json.load(f))
        
        # Scraper les matchs depuis différentes sources
        matches = []
        
        # Source 1: Kooora
        try:
            kooora_matches = kooora.get_today_matches()
            matches.extend(kooora_matches)
        except Exception as e:
            print(f"Erreur Kooora: {e}")
        
        # Source 2: Yallakora
        try:
            yallakora_matches = yallakora.get_today_matches()
            matches.extend(yallakora_matches)
        except Exception as e:
            print(f"Erreur Yallakora: {e}")
        
        # Source 3: Filgoal
        try:
            filgoal_matches = filgoal.get_today_matches()
            matches.extend(filgoal_matches)
        except Exception as e:
            print(f"Erreur Filgoal: {e}")
        
        # Source 4: API-Football (si disponible)
        try:
            api_matches = api_football.get_today_matches()
            matches.extend(api_matches)
        except Exception as e:
            print(f"Erreur API-Football: {e}")
        
        # Dédupliquer les matchs
        unique_matches = deduplicate_matches(matches)
        
        # Ajouter les chaînes de diffusion basées sur la compétition
        unique_matches = add_channels_to_matches(unique_matches)
        
        # Sauvegarder dans le cache
        os.makedirs('cache', exist_ok=True)
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(unique_matches, f, ensure_ascii=False, indent=2)
        
        return jsonify(unique_matches)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/matches/date/<date>')
def get_matches_by_date(date):
    """Récupère les matchs pour une date spécifique (YYYY-MM-DD)"""
    try:
        cache_file = f'cache/matches_{date}.json'
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                return jsonify(json.load(f))
        
        matches = []
        
        try:
            kooora_matches = kooora.get_matches_by_date(date)
            matches.extend(kooora_matches)
        except Exception as e:
            print(f"Erreur Kooora: {e}")
        
        try:
            yallakora_matches = yallakora.get_matches_by_date(date)
            matches.extend(yallakora_matches)
        except Exception as e:
            print(f"Erreur Yallakora: {e}")
        
        try:
            filgoal_matches = filgoal.get_matches_by_date(date)
            matches.extend(filgoal_matches)
        except Exception as e:
            print(f"Erreur Filgoal: {e}")
        
        unique_matches = deduplicate_matches(matches)
        
        # Ajouter les chaînes de diffusion
        unique_matches = add_channels_to_matches(unique_matches)
        
        os.makedirs('cache', exist_ok=True)
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(unique_matches, f, ensure_ascii=False, indent=2)
        
        return jsonify(unique_matches)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/channels')
def get_channels():
    """Récupère la liste des chaînes disponibles"""
    channels = []
    m3u_files = [
        'bein.m3u', 'dazn.m3u', 'espn.m3u', 'elevendazn.m3u',
        'generalsports.m3u', 'mbc.m3u', 'premierleague.m3u',
        'roshnleague.m3u', 'SeriaA.m3u', 'sky_channels.m3u'
    ]
    
    for m3u_file in m3u_files:
        if os.path.exists(m3u_file):
            category = m3u_file.replace('.m3u', '').replace('_channels', '')
            channels_list = parse_m3u(m3u_file, category)
            channels.extend(channels_list)
    
    return jsonify(channels)

@app.route('/proxy/stream')
def proxy_stream():
    """Proxy pour les flux IPTV - contourne les restrictions CORS et serveur"""
    from flask import Response, stream_with_context
    import requests
    
    # Récupérer l'URL du flux depuis les paramètres
    stream_url = request.args.get('url')
    
    if not stream_url:
        return jsonify({'error': 'URL manquante'}), 400
    
    try:
        # Headers pour se faire passer pour un client IPTV standard
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': stream_url
        }
        
        # Faire la requête au serveur IPTV
        response = requests.get(stream_url, headers=headers, stream=True, timeout=10)
        
        # Déterminer le type de contenu
        content_type = response.headers.get('Content-Type', 'application/vnd.apple.mpegurl')
        
        # Si c'est un fichier m3u8, on doit modifier les URLs internes
        if 'mpegurl' in content_type or stream_url.endswith('.m3u8'):
            # Lire le contenu du m3u8
            m3u8_content = response.text
            
            # Modifier les URLs relatives en URLs absolues via notre proxy
            import re
            from urllib.parse import urljoin, urlparse
            
            base_url = '/'.join(stream_url.split('/')[:-1]) + '/'
            
            def replace_url(match):
                url = match.group(0)
                # Si c'est déjà une URL complète, la proxifier
                if url.startswith('http'):
                    return f"/proxy/stream?url={url}"
                # Si c'est une URL relative, la convertir en absolue puis proxifier
                else:
                    absolute_url = urljoin(base_url, url)
                    return f"/proxy/stream?url={absolute_url}"
            
            # Remplacer les URLs dans le m3u8
            m3u8_content = re.sub(r'https?://[^\s]+|[^\s]+\.ts|[^\s]+\.m3u8', replace_url, m3u8_content)
            
            return Response(m3u8_content, mimetype='application/vnd.apple.mpegurl')
        
        # Pour les segments TS ou autre contenu, streamer directement
        def generate():
            try:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        yield chunk
            except Exception as e:
                print(f"Erreur streaming: {e}")
        
        return Response(stream_with_context(generate()), 
                       mimetype=content_type,
                       headers={
                           'Access-Control-Allow-Origin': '*',
                           'Access-Control-Allow-Methods': 'GET, OPTIONS',
                           'Access-Control-Allow-Headers': 'Content-Type',
                           'Cache-Control': 'no-cache'
                       })
    
    except Exception as e:
        print(f"Erreur proxy: {e}")
        return jsonify({'error': str(e)}), 500

def parse_m3u(file_path, category):
    """Parse un fichier M3U et retourne la liste des chaînes"""
    channels = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith('#EXTINF'):
                # Extraire le nom de la chaîne
                channel_name = line.split(',', 1)[1] if ',' in line else 'Unknown'
                
                # La ligne suivante devrait contenir l'URL
                if i + 1 < len(lines):
                    url = lines[i + 1].strip()
                    if url and not url.startswith('#'):
                        channels.append({
                            'name': channel_name.strip(),
                            'url': url,
                            'category': category,
                            'logo': f'/static/logos/{category}.png'
                        })
                i += 2
            else:
                i += 1
    except Exception as e:
        print(f"Erreur lors du parsing de {file_path}: {e}")
    
    return channels

def deduplicate_matches(matches):
    """Déduplique les matchs basés sur l'équipe à domicile, l'équipe à l'extérieur et l'heure"""
    seen = set()
    unique = []
    
    for match in matches:
        key = (match.get('home_team'), match.get('away_team'), match.get('time'))
        if key not in seen:
            seen.add(key)
            unique.append(match)
    
    # Trier par heure
    unique.sort(key=lambda x: x.get('time', ''))
    
    return unique

if __name__ == '__main__':
    # Créer les dossiers nécessaires
    os.makedirs('cache', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/logos', exist_ok=True)
    os.makedirs('scrapers', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
