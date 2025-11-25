import requests
from datetime import datetime
import os

class APIFootballMatches:
    """
    Scraper utilisant l'API API-Football (api-football.com)
    Note: Nécessite une clé API (gratuit jusqu'à 100 requêtes/jour)
    """
    
    def __init__(self):
        self.base_url = "https://v3.football.api-sports.io"
        # Vous pouvez obtenir une clé API gratuite sur https://www.api-football.com/
        self.api_key = os.getenv('API_FOOTBALL_KEY', '')  # Mettre votre clé API ici
        self.headers = {
            'x-rapidapi-host': 'v3.football.api-sports.io',
            'x-rapidapi-key': self.api_key
        }
    
    def get_today_matches(self):
        """Récupère les matchs du jour"""
        if not self.api_key:
            print("API_FOOTBALL_KEY non configurée, utiliser les scrapers alternatifs")
            return []
        
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            return self.get_matches_by_date(today)
        except Exception as e:
            print(f"Erreur lors de la récupération des matchs API-Football: {e}")
            return []
    
    def get_matches_by_date(self, date):
        """Récupère les matchs pour une date spécifique"""
        if not self.api_key:
            return []
        
        matches = []
        
        try:
            url = f"{self.base_url}/fixtures"
            params = {
                'date': date,
                'timezone': 'Africa/Cairo'  # Ajuster selon votre fuseau horaire
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code != 200:
                print(f"Erreur HTTP {response.status_code}")
                return matches
            
            data = response.json()
            
            if data.get('response'):
                for fixture in data['response']:
                    match = self._parse_fixture(fixture, date)
                    if match:
                        matches.append(match)
            
            print(f"API-Football: {len(matches)} matchs trouvés pour {date}")
            
        except Exception as e:
            print(f"Erreur lors de l'appel API-Football: {e}")
        
        return matches
    
    def _parse_fixture(self, fixture, date):
        """Parse un fixture de l'API et extrait les informations"""
        try:
            fixture_data = fixture.get('fixture', {})
            teams = fixture.get('teams', {})
            goals = fixture.get('goals', {})
            league = fixture.get('league', {})
            
            home_team = teams.get('home', {}).get('name', 'Unknown')
            away_team = teams.get('away', {}).get('name', 'Unknown')
            
            # Extraire l'heure
            timestamp = fixture_data.get('timestamp')
            if timestamp:
                dt = datetime.fromtimestamp(timestamp)
                match_time = dt.strftime('%H:%M')
            else:
                match_time = "TBD"
            
            # Score
            home_goals = goals.get('home')
            away_goals = goals.get('away')
            
            if home_goals is not None and away_goals is not None:
                score = f"{home_goals} - {away_goals}"
            else:
                score = "-"
            
            # Statut
            status_short = fixture_data.get('status', {}).get('short', 'NS')
            status_map = {
                'NS': 'Scheduled',
                'LIVE': 'Live',
                '1H': 'Live',
                'HT': 'Half Time',
                '2H': 'Live',
                'ET': 'Extra Time',
                'P': 'Penalties',
                'FT': 'Finished',
                'AET': 'Finished',
                'PEN': 'Finished',
                'PST': 'Postponed',
                'CANC': 'Cancelled',
                'ABD': 'Abandoned',
                'TBD': 'To Be Defined'
            }
            
            status = status_map.get(status_short, 'Scheduled')
            is_live = status_short in ['LIVE', '1H', '2H', 'ET', 'P', 'HT']
            
            competition = league.get('name', 'Unknown')
            competition_logo = league.get('logo', '')
            
            return {
                'home_team': home_team,
                'away_team': away_team,
                'time': match_time,
                'date': date,
                'score': score,
                'competition': competition,
                'competition_logo': competition_logo,
                'status': status,
                'is_live': is_live,
                'fixture_id': fixture_data.get('id'),
                'source': 'API-Football'
            }
            
        except Exception as e:
            print(f"Erreur _parse_fixture: {e}")
            return None
    
    def get_live_matches(self):
        """Récupère uniquement les matchs en direct"""
        if not self.api_key:
            return []
        
        matches = []
        
        try:
            url = f"{self.base_url}/fixtures"
            params = {'live': 'all'}
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('response'):
                    for fixture in data['response']:
                        match = self._parse_fixture(fixture, datetime.now().strftime('%Y-%m-%d'))
                        if match:
                            matches.append(match)
            
        except Exception as e:
            print(f"Erreur lors de la récupération des matchs live: {e}")
        
        return matches
