"""
Configuration de l'application Mobaryat
"""

import os
from datetime import timedelta

class Config:
    """Configuration de base"""
    
    # Clé secrète Flask (à changer en production!)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuration de l'application
    APP_NAME = 'Mobaryat'
    APP_VERSION = '1.0.0'
    
    # Configuration Flask
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING = False
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False
    
    # Configuration du serveur
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Configuration du cache
    CACHE_DIR = 'cache'
    CACHE_TIMEOUT = timedelta(minutes=5)  # Les données de matchs sont mises en cache 5 minutes
    
    # Configuration des scrapers
    SCRAPERS_ENABLED = {
        'kooora': True,
        'yallakora': True,
        'filgoal': True,
        'api_football': os.environ.get('API_FOOTBALL_KEY') is not None
    }
    
    # API Keys
    API_FOOTBALL_KEY = os.environ.get('API_FOOTBALL_KEY', '')
    
    # User-Agent pour les scrapers
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    # Timeout pour les requêtes HTTP
    REQUEST_TIMEOUT = 10
    
    # Nombre de workers pour le rafraîchissement automatique
    AUTO_REFRESH_INTERVAL = 120  # secondes
    
    # Configuration des logs
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = 'app.log'
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
    LOG_BACKUP_COUNT = 3
    
    # Configuration M3U
    M3U_FILES = [
        'bein.m3u',
        'dazn.m3u',
        'espn.m3u',
        'generalsports.m3u',
        'mbc.m3u',
        'premierleague.m3u',
        'roshnleague.m3u',
        'SeriaA.m3u'
    ]
    
    # Catégories de chaînes avec icônes
    CHANNEL_CATEGORIES = {
        'bein': {
            'name': 'beIN Sports',
            'icon': 'fa-futbol',
            'color': '#9b1d20'
        },
        'dazn': {
            'name': 'DAZN',
            'icon': 'fa-video',
            'color': '#f8d000'
        },
        'espn': {
            'name': 'ESPN',
            'icon': 'fa-basketball-ball',
            'color': '#cc0000'
        },
        'premierleague': {
            'name': 'Premier League',
            'icon': 'fa-trophy',
            'color': '#3d195b'
        },
        'roshnleague': {
            'name': 'Roshn League',
            'icon': 'fa-medal',
            'color': '#00843d'
        },
        'SeriaA': {
            'name': 'Serie A',
            'icon': 'fa-flag',
            'color': '#024494'
        },
        'generalsports': {
            'name': 'Sports Généraux',
            'icon': 'fa-running',
            'color': '#ff6600'
        },
        'mbc': {
            'name': 'MBC',
            'icon': 'fa-film',
            'color': '#1a73e8'
        }
    }

class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False
    TESTING = False
    
    # En production, la clé secrète doit être définie via variable d'environnement
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY doit être définie en production!")

class TestingConfig(Config):
    """Configuration pour les tests"""
    DEBUG = True
    TESTING = True
    CACHE_TIMEOUT = timedelta(seconds=1)

# Dictionnaire de configuration
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(env=None):
    """Récupère la configuration selon l'environnement"""
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
