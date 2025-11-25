import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

class YallaKoraMatches:
    """Scraper pour récupérer les matchs depuis Yallakora.com"""
    
    def __init__(self):
        self.base_url = "https://www.yallakora.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
    
    def get_today_matches(self):
        """Récupère les matchs du jour"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            return self.get_matches_by_date(today)
        except Exception as e:
            print(f"Erreur lors de la récupération des matchs Yallakora: {e}")
            return []
    
    def get_matches_by_date(self, date):
        """Récupère les matchs pour une date spécifique"""
        matches = []
        
        try:
            # Format de date pour Yallakora: MM/DD/YYYY
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%m/%d/%Y')
            
            # URL de l'API Yallakora pour les matchs
            url = f"{self.base_url}/match-center"
            params = {'date': formatted_date}
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                print(f"Erreur HTTP {response.status_code}")
                return matches
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Trouver toutes les sections de matchs
            match_items = soup.find_all('li', class_='item')
            
            if not match_items:
                match_items = soup.find_all('div', class_='matchCard')
            
            for item in match_items:
                try:
                    match = self._parse_match_item(item, date)
                    if match:
                        matches.append(match)
                except Exception as e:
                    print(f"Erreur lors du parsing d'un match: {e}")
                    continue
            
            print(f"Yallakora: {len(matches)} matchs trouvés pour {date}")
            
        except Exception as e:
            print(f"Erreur lors du scraping Yallakora: {e}")
        
        return matches
    
    def _parse_match_item(self, item, date):
        """Parse un élément de match et extrait les informations"""
        try:
            # Extraire les équipes
            home_team_elem = item.find('div', class_='teamA')
            away_team_elem = item.find('div', class_='teamB')
            
            if not home_team_elem or not away_team_elem:
                # Essayer une autre structure
                teams = item.find_all('p', class_='teamName')
                if len(teams) >= 2:
                    home_team = teams[0].get_text(strip=True)
                    away_team = teams[1].get_text(strip=True)
                else:
                    return None
            else:
                home_team = home_team_elem.find('p').get_text(strip=True) if home_team_elem.find('p') else ''
                away_team = away_team_elem.find('p').get_text(strip=True) if away_team_elem.find('p') else ''
            
            if not home_team or not away_team:
                return None
            
            # Extraire l'heure
            time_elem = item.find('span', class_='time')
            if not time_elem:
                time_elem = item.find('div', class_='matchTime')
            
            match_time = time_elem.get_text(strip=True) if time_elem else "TBD"
            
            # Extraire le score
            score_elem = item.find('div', class_='matchResult')
            if not score_elem:
                score_elem = item.find('span', class_='score')
            
            score = score_elem.get_text(strip=True) if score_elem else "-"
            
            # Extraire la compétition
            competition_elem = item.find('div', class_='tournament')
            if not competition_elem:
                competition_elem = item.find('h3', class_='leagueName')
            
            competition = competition_elem.get_text(strip=True) if competition_elem else "Unknown"
            
            # Déterminer le statut
            status = "Scheduled"
            if score and score != "-":
                if "'" in item.get_text():  # Si on trouve un ' cela indique généralement le temps de jeu
                    status = "Live"
                else:
                    status = "Finished"
            
            is_live = status == "Live"
            
            # Extraire les chaînes de diffusion
            channels = []
            channel_elems = item.find_all('div', class_='channel')
            for ch in channel_elems:
                channel_name = ch.get_text(strip=True)
                if channel_name:
                    channels.append(channel_name)
            
            return {
                'home_team': home_team,
                'away_team': away_team,
                'time': match_time,
                'date': date,
                'score': score,
                'competition': competition,
                'status': status,
                'is_live': is_live,
                'channels': channels,
                'source': 'Yallakora'
            }
            
        except Exception as e:
            print(f"Erreur _parse_match_item: {e}")
            return None
