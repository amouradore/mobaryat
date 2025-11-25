# 🕷️ Guide pour Ajouter de Nouveaux Scrapers

Ce guide explique comment créer de nouveaux scrapers pour récupérer des données de matchs depuis d'autres sites web.

## 📋 Structure d'un Scraper

Chaque scraper doit suivre la structure suivante:

```python
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class MonScraper:
    """Description du scraper"""
    
    def __init__(self):
        self.base_url = "https://exemple.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 ...',
            'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8'
        }
    
    def get_today_matches(self):
        """Récupère les matchs du jour"""
        today = datetime.now().strftime('%Y-%m-%d')
        return self.get_matches_by_date(today)
    
    def get_matches_by_date(self, date):
        """Récupère les matchs pour une date spécifique"""
        matches = []
        # Votre logique de scraping ici
        return matches
    
    def _parse_match_item(self, item, date):
        """Parse un élément de match"""
        return {
            'home_team': '',
            'away_team': '',
            'time': '',
            'date': date,
            'score': '-',
            'competition': '',
            'status': 'Scheduled',
            'is_live': False,
            'source': 'MonSite'
        }
```

## 🎯 Sites Recommandés pour le Scraping

### 1. Filgoal.com
```python
# scrapers/filgoal_scraper.py
class FilgoalMatches:
    def __init__(self):
        self.base_url = "https://www.filgoal.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'ar'
        }
```

**Sections à scraper:**
- Matchs du jour: `/matches`
- Matchs live: `/matches?date=today&status=live`
- Matchs par compétition

### 2. Flashscore.com
```python
# scrapers/flashscore_scraper.py
class FlashscoreMatches:
    def __init__(self):
        self.base_url = "https://www.flashscore.com"
        # Note: Flashscore utilise beaucoup de JavaScript
        # Utilisez Selenium ou Playwright
```

### 3. Livescore.com
```python
# scrapers/livescore_scraper.py
class LivescoreMatches:
    def __init__(self):
        self.base_url = "https://www.livescore.com"
        # API JSON disponible
```

### 4. ESPN.com
```python
# scrapers/espn_scraper.py
class ESPNMatches:
    def __init__(self):
        self.base_url = "https://www.espn.com/soccer"
        # Utilise des endpoints API
```

## 🛠️ Outils Utiles

### BeautifulSoup (Sites Simples)
```python
from bs4 import BeautifulSoup
import requests

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Trouver des éléments
matches = soup.find_all('div', class_='match-card')
team_name = soup.find('span', class_='team').get_text(strip=True)
```

### Selenium (Sites avec JavaScript)
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get(url)

# Attendre le chargement
driver.implicitly_wait(10)

# Extraire les données
matches = driver.find_elements(By.CLASS_NAME, 'match-card')
```

### Playwright (Moderne)
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    
    # Extraire les données
    matches = page.query_selector_all('.match-card')
```

### Requests avec JSON (APIs)
```python
import requests

response = requests.get(api_url, headers=headers)
data = response.json()

matches = data['matches']
```

## 📝 Format de Données Standard

Chaque match retourné doit avoir ce format:

```python
{
    'home_team': 'Équipe à domicile',        # Requis
    'away_team': 'Équipe à l\'extérieur',    # Requis
    'time': '20:00',                          # Requis (format HH:MM)
    'date': '2024-01-15',                     # Requis (format YYYY-MM-DD)
    'score': '2 - 1',                         # Optionnel (- si pas de score)
    'competition': 'La Liga',                 # Requis
    'status': 'Live',                         # Requis (Scheduled/Live/Finished/etc)
    'is_live': True,                          # Requis (Boolean)
    'channels': ['beIN 1', 'ESPN'],          # Optionnel
    'competition_logo': 'url',                # Optionnel
    'home_logo': 'url',                       # Optionnel
    'away_logo': 'url',                       # Optionnel
    'fixture_id': '12345',                    # Optionnel
    'source': 'NomDuSite'                    # Requis
}
```

## 🔧 Intégration dans l'Application

### Étape 1: Créer le fichier scraper
```bash
# Créer le fichier dans le dossier scrapers/
touch scrapers/nouveau_scraper.py
```

### Étape 2: Implémenter la classe
```python
# scrapers/nouveau_scraper.py
class NouveauScraper:
    # Votre code ici
    pass
```

### Étape 3: Importer dans app.py
```python
# Dans app.py
from scrapers.nouveau_scraper import NouveauScraper

# Initialiser
nouveau_scraper = NouveauScraper()

# Utiliser dans get_today_matches()
try:
    nouveau_matches = nouveau_scraper.get_today_matches()
    matches.extend(nouveau_matches)
except Exception as e:
    print(f"Erreur NouveauScraper: {e}")
```

## ⚠️ Bonnes Pratiques

### 1. Respecter les Sites
```python
# Ajouter un délai entre les requêtes
import time
time.sleep(1)  # Attendre 1 seconde

# Limiter le nombre de requêtes
max_retries = 3
```

### 2. Gérer les Erreurs
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Erreur: {e}")
    return []
```

### 3. User-Agent Réaliste
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ar,en-US;q=0.9',
    'Referer': 'https://www.google.com/'
}
```

### 4. Cache pour Performance
```python
import json
import os
from datetime import datetime

def get_cached_matches(date):
    cache_file = f'cache/matches_{date}.json'
    if os.path.exists(cache_file):
        # Vérifier si le cache est récent (< 5 minutes)
        file_time = os.path.getmtime(cache_file)
        if time.time() - file_time < 300:
            with open(cache_file, 'r') as f:
                return json.load(f)
    return None
```

### 5. Encoding UTF-8
```python
response = requests.get(url)
response.encoding = 'utf-8'  # Pour les sites arabes
content = response.text
```

## 🧪 Tester Votre Scraper

```python
# test_scraper.py
from scrapers.nouveau_scraper import NouveauScraper

scraper = NouveauScraper()
matches = scraper.get_today_matches()

print(f"Nombre de matchs: {len(matches)}")
for match in matches[:3]:  # Afficher les 3 premiers
    print(f"{match['home_team']} vs {match['away_team']} - {match['competition']}")
```

## 📚 Exemples Complets

### Exemple 1: Scraper Simple avec BeautifulSoup
```python
# scrapers/simple_scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class SimpleScraper:
    def __init__(self):
        self.base_url = "https://example-sports-site.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def get_today_matches(self):
        matches = []
        try:
            url = f"{self.base_url}/matches/today"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                match_cards = soup.find_all('div', class_='match-card')
                
                for card in match_cards:
                    home = card.find('div', class_='home-team').get_text(strip=True)
                    away = card.find('div', class_='away-team').get_text(strip=True)
                    time_elem = card.find('span', class_='time').get_text(strip=True)
                    
                    matches.append({
                        'home_team': home,
                        'away_team': away,
                        'time': time_elem,
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'score': '-',
                        'competition': 'Unknown',
                        'status': 'Scheduled',
                        'is_live': False,
                        'source': 'SimpleScraper'
                    })
        except Exception as e:
            print(f"Erreur SimpleScraper: {e}")
        
        return matches
```

### Exemple 2: Scraper avec API JSON
```python
# scrapers/api_scraper.py
import requests
from datetime import datetime

class APIScraper:
    def __init__(self):
        self.base_url = "https://api.example-sports.com/v1"
        self.api_key = "your_api_key"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def get_today_matches(self):
        matches = []
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            url = f"{self.base_url}/matches"
            params = {'date': today}
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for fixture in data.get('fixtures', []):
                    matches.append({
                        'home_team': fixture['home']['name'],
                        'away_team': fixture['away']['name'],
                        'time': fixture['time'],
                        'date': today,
                        'score': f"{fixture['score']['home']} - {fixture['score']['away']}",
                        'competition': fixture['league']['name'],
                        'status': fixture['status'],
                        'is_live': fixture['status'] == 'LIVE',
                        'source': 'APIScraper'
                    })
        except Exception as e:
            print(f"Erreur APIScraper: {e}")
        
        return matches
```

## 🔍 Déboguer un Scraper

### 1. Inspecter la Réponse HTML
```python
with open('debug.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
```

### 2. Logs Détaillés
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"URL: {url}")
logger.debug(f"Status: {response.status_code}")
logger.debug(f"Matchs trouvés: {len(matches)}")
```

### 3. Tester les Sélecteurs CSS
```python
# Dans votre navigateur (Console JavaScript):
document.querySelectorAll('.match-card')
```

## 📞 Besoin d'Aide?

Si vous rencontrez des problèmes:
1. Vérifiez les logs de la console
2. Inspectez la structure HTML du site cible
3. Testez votre scraper indépendamment
4. Utilisez les outils de développement du navigateur

## 🎉 Contribuer

Une fois votre scraper créé et testé:
1. Créez une Pull Request
2. Documentez votre scraper
3. Ajoutez des tests
4. Partagez avec la communauté!
