import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

class FilgoalMatches:
    """Scraper pour récupérer les matchs depuis Filgoal.com"""
    
    def __init__(self):
        self.base_url = "https://www.filgoal.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'https://www.google.com/'
        }
    
    def get_today_matches(self):
        """Récupère les matchs du jour"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            return self.get_matches_by_date(today)
        except Exception as e:
            print(f"Erreur lors de la récupération des matchs Filgoal: {e}")
            return []
    
    def get_matches_by_date(self, date):
        """Récupère les matchs pour une date spécifique"""
        matches = []
        
        try:
            # URL pour les matchs sur Filgoal
            url = f"{self.base_url}/matches"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                print(f"Erreur HTTP {response.status_code}")
                return matches
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Trouver toutes les sections de matchs
            # Filgoal utilise généralement des divs avec classe 'match_card' ou similaire
            match_items = soup.find_all('div', class_='mc-block')
            
            if not match_items:
                match_items = soup.find_all('li', class_='match-card')
            
            if not match_items:
                match_items = soup.find_all('div', attrs={'data-match-id': True})
            
            for item in match_items:
                try:
                    match = self._parse_match_item(item, date)
                    if match:
                        matches.append(match)
                except Exception as e:
                    print(f"Erreur lors du parsing d'un match: {e}")
                    continue
            
            print(f"Filgoal: {len(matches)} matchs trouvés pour {date}")
            
        except Exception as e:
            print(f"Erreur lors du scraping Filgoal: {e}")
        
        return matches
    
    def _parse_match_item(self, item, date):
        """Parse un élément de match et extrait les informations"""
        try:
            # Extraire les équipes
            teams = item.find_all('div', class_='team-name')
            if not teams or len(teams) < 2:
                teams = item.find_all('span', class_='team')
            
            if len(teams) < 2:
                # Essayer une autre méthode
                team_elems = item.find_all('a', class_='team-link')
                if len(team_elems) >= 2:
                    home_team = team_elems[0].get_text(strip=True)
                    away_team = team_elems[1].get_text(strip=True)
                else:
                    return None
            else:
                home_team = teams[0].get_text(strip=True)
                away_team = teams[1].get_text(strip=True)
            
            if not home_team or not away_team:
                return None
            
            # Extraire l'heure
            time_elem = item.find('span', class_='time')
            if not time_elem:
                time_elem = item.find('div', class_='match-time')
            if not time_elem:
                time_elem = item.find('span', attrs={'data-time': True})
            
            match_time = time_elem.get_text(strip=True) if time_elem else "TBD"
            
            # Nettoyer le format de l'heure (ex: "20:00" ou "08:00 PM")
            match_time = self._clean_time(match_time)
            
            # Extraire le score
            score_elem = item.find('div', class_='match-score')
            if not score_elem:
                score_elem = item.find('span', class_='result')
            
            score = "-"
            if score_elem:
                score_text = score_elem.get_text(strip=True)
                # Format peut être "2 - 1" ou "2-1" ou séparé
                score = self._clean_score(score_text)
            
            # Extraire la compétition/ligue
            competition_elem = item.find('div', class_='tournament')
            if not competition_elem:
                competition_elem = item.find('span', class_='league-name')
            if not competition_elem:
                competition_elem = item.find('a', class_='league')
            
            competition = competition_elem.get_text(strip=True) if competition_elem else "Unknown"
            
            # Extraire le statut
            status = "Scheduled"
            status_elem = item.find('span', class_='status')
            if not status_elem:
                status_elem = item.find('div', class_='match-status')
            
            if status_elem:
                status_text = status_elem.get_text(strip=True).lower()
                if 'مباشر' in status_text or 'live' in status_text:
                    status = "Live"
                elif 'انتهت' in status_text or 'finished' in status_text or 'ft' in status_text:
                    status = "Finished"
                elif 'مؤجل' in status_text or 'postponed' in status_text:
                    status = "Postponed"
            
            # Vérifier si le match est en direct
            is_live = status == "Live" or 'مباشر' in item.get_text()
            
            # Extraire les logos (optionnel)
            home_logo = ""
            away_logo = ""
            logo_elems = item.find_all('img', class_='team-logo')
            if len(logo_elems) >= 2:
                home_logo = logo_elems[0].get('src', '')
                away_logo = logo_elems[1].get('src', '')
            
            # Extraire les chaînes de diffusion
            channels = []
            channel_section = item.find('div', class_='channels')
            if channel_section:
                channel_elems = channel_section.find_all('span', class_='channel-name')
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
                'home_logo': home_logo if home_logo else None,
                'away_logo': away_logo if away_logo else None,
                'source': 'Filgoal'
            }
            
        except Exception as e:
            print(f"Erreur _parse_match_item: {e}")
            return None
    
    def _clean_time(self, time_str):
        """Nettoie et standardise le format de l'heure"""
        try:
            # Supprimer les espaces et caractères inutiles
            time_str = time_str.strip()
            
            # Si format "08:00 PM", convertir en format 24h
            if 'pm' in time_str.lower() or 'am' in time_str.lower():
                time_str = time_str.upper()
                time_part = time_str.split()[0]
                period = time_str.split()[1] if len(time_str.split()) > 1 else 'AM'
                
                hour, minute = time_part.split(':')
                hour = int(hour)
                
                if period == 'PM' and hour != 12:
                    hour += 12
                elif period == 'AM' and hour == 12:
                    hour = 0
                
                return f"{hour:02d}:{minute}"
            
            # Si déjà au format HH:MM
            if re.match(r'\d{1,2}:\d{2}', time_str):
                parts = time_str.split(':')
                return f"{int(parts[0]):02d}:{parts[1]}"
            
            return time_str
            
        except:
            return time_str
    
    def _clean_score(self, score_str):
        """Nettoie et standardise le format du score"""
        try:
            # Supprimer les espaces
            score_str = score_str.strip()
            
            # Si contient des chiffres séparés par - ou vs
            match = re.search(r'(\d+)\s*[-vs]\s*(\d+)', score_str, re.IGNORECASE)
            if match:
                return f"{match.group(1)} - {match.group(2)}"
            
            # Si format "X:Y"
            match = re.search(r'(\d+):(\d+)', score_str)
            if match:
                return f"{match.group(1)} - {match.group(2)}"
            
            return score_str if score_str else "-"
            
        except:
            return "-"
    
    def get_live_matches(self):
        """Récupère uniquement les matchs en direct"""
        try:
            url = f"{self.base_url}/matches?status=live"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Parser les matchs live
                # ... logique similaire
                pass
                
        except Exception as e:
            print(f"Erreur lors de la récupération des matchs live: {e}")
        
        return []
