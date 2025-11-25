import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

class KooraMatches:
    """Scraper pour récupérer les matchs depuis Kooora.com"""
    
    def __init__(self):
        self.base_url = "https://www.kooora.com"
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
            print(f"Erreur lors de la récupération des matchs Kooora: {e}")
            return []
    
    def get_matches_by_date(self, date):
        """Récupère les matchs pour une date spécifique"""
        matches = []
        
        try:
            # Kooora utilise maintenant une structure différente
            # La page principale affiche les matchs du jour
            url = self.base_url
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                print(f"Erreur HTTP {response.status_code}")
                return matches
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Nouvelle structure Kooora - chercher les liens <a> avec classe fco-match-card
            match_items = soup.find_all('a', class_=lambda x: x and 'fco-match-card' in x)
            
            if not match_items:
                # Essayer d'autres sélecteurs
                match_items = soup.find_all('div', class_=lambda x: x and 'fco-match-card' in x)
            
            if not match_items:
                match_items = soup.find_all('a', href=lambda x: x and '/match/' in x if x else False)
            
            for item in match_items:
                try:
                    match = self._parse_match_item(item, date)
                    if match:
                        matches.append(match)
                except Exception as e:
                    print(f"Erreur lors du parsing d'un match: {e}")
                    continue
            
            print(f"Kooora: {len(matches)} matchs trouvés pour {date}")
            
        except Exception as e:
            print(f"Erreur lors du scraping Kooora: {e}")
        
        return matches
    
    def _parse_match_item(self, item, date):
        """Parse un élément de match et extrait les informations"""
        try:
            # Nouvelle structure Kooora avec classes fco-*
            
            # Extraire les équipes - chercher les divs fco-team-name
            home_team_container = item.find('div', class_='fco-match-card__team--home')
            away_team_container = item.find('div', class_='fco-match-card__team--away')
            
            if not home_team_container or not away_team_container:
                return None
            
            # Extraire le nom (chercher div avec fco-team-name dans la classe)
            home_team_elem = home_team_container.find('div', class_=lambda x: x and 'fco-team-name' in x)
            away_team_elem = away_team_container.find('div', class_=lambda x: x and 'fco-team-name' in x)
            
            if not home_team_elem or not away_team_elem:
                return None
            
            home_team = home_team_elem.get_text(strip=True)
            away_team = away_team_elem.get_text(strip=True)
            
            if not home_team or not away_team:
                return None
            
            # Extraire l'heure (time.fco-match-start-date)
            time_elem = item.find('time', class_='fco-match-start-date')
            match_time = time_elem.get_text(strip=True) if time_elem else "TBD"
            
            # Extraire le score (chercher les spans avec fco-match-card__score)
            home_score_elem = item.find('span', class_='fco-match-card__score--home')
            away_score_elem = item.find('span', class_='fco-match-card__score--away')
            
            if home_score_elem and away_score_elem:
                home_score = home_score_elem.get_text(strip=True)
                away_score = away_score_elem.get_text(strip=True)
                if home_score != '-' and away_score != '-':
                    score = f"{home_score} - {away_score}"
                else:
                    score = "-"
            else:
                score = "-"
            
            # Extraire la compétition (span.fco-match-card__competition)
            competition_elem = item.find('span', class_='fco-match-card__competition')
            competition = competition_elem.get_text(strip=True) if competition_elem else "Unknown"
            
            # Extraire les logos des équipes
            home_logo = ""
            away_logo = ""
            
            # Chercher l'image dans le conteneur home (classe fco-image__image)
            home_logo_elem = home_team_container.find('img', class_='fco-image__image')
            if home_logo_elem:
                home_logo = home_logo_elem.get('src', '')
            
            # Chercher l'image dans le conteneur away (classe fco-image__image)
            away_logo_elem = away_team_container.find('img', class_='fco-image__image')
            if away_logo_elem:
                away_logo = away_logo_elem.get('src', '')
            
            # Extraire le logo de la compétition
            competition_logo = ""
            comp_logo_elem = item.find('img', class_=lambda x: x and 'competition' in x.lower())
            if comp_logo_elem:
                competition_logo = comp_logo_elem.get('src', '')
                if competition_logo and not competition_logo.startswith('http'):
                    competition_logo = f"https://www.kooora.com{competition_logo}"
            
            # Extraire l'URL du match pour récupérer les chaînes
            match_url = item.get('href', '')
            if match_url and not match_url.startswith('http'):
                match_url = self.base_url + match_url
            
            # Récupérer les chaînes depuis la page du match
            channels = self._get_channels_from_match_page(match_url) if match_url else []
            
            # Déterminer le statut depuis l'attribut data-state
            data_state = item.get('data-state', 'FIXTURE')
            status = "Scheduled"
            is_live = False
            
            if data_state == 'LIVE' or data_state == 'IN_PLAY':
                status = "Live"
                is_live = True
            elif data_state == 'FINISHED' or data_state == 'FULL_TIME' or data_state == 'RESULT':
                status = "Finished"
            elif data_state == 'FIXTURE':
                status = "Scheduled"
            
            # Double vérification avec le texte si le score existe
            if score != "-" and not is_live:
                status = "Finished"
            
            return {
                'home_team': home_team,
                'away_team': away_team,
                'home_logo': home_logo,
                'away_logo': away_logo,
                'time': match_time,
                'date': date,
                'score': score,
                'competition': competition,
                'competition_logo': competition_logo,
                'channels': channels,
                'status': status,
                'is_live': is_live,
                'source': 'Kooora'
            }
            
        except Exception as e:
            print(f"Erreur _parse_match_item: {e}")
            return None
    
    def _get_channels_from_match_page(self, match_url):
        """Récupère les chaînes diffuseurs depuis la page du match"""
        channels = []
        
        try:
            # Ne récupérer les chaînes que pour les matchs futurs ou en direct
            # pour économiser les requêtes
            response = requests.get(match_url, headers=self.headers, timeout=5)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                return channels
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Chercher les conteneurs de chaînes (fco-match-ott__channels)
            channels_containers = soup.find_all('div', class_='fco-match-ott__channels')
            
            for container in channels_containers:
                # Chercher chaque chaîne (fco-match-ott__channel)
                channel_links = container.find_all('a', class_='fco-match-ott__channel')
                
                for channel_link in channel_links:
                    # Extraire le nom de la chaîne
                    channel_name_elem = channel_link.find('p', class_='fco-match-ott__channel-name')
                    if not channel_name_elem:
                        continue
                    
                    channel_name = channel_name_elem.get_text(strip=True)
                    
                    # Extraire le logo
                    channel_logo = ""
                    img_elem = channel_link.find('img', class_='fco-image__image')
                    if img_elem:
                        channel_logo = img_elem.get('src', '')
                    
                    # Éviter les doublons
                    if channel_name and not any(ch['name'] == channel_name for ch in channels):
                        channels.append({
                            'name': channel_name,
                            'logo': channel_logo
                        })
            
        except Exception as e:
            # Ne pas bloquer si on ne peut pas récupérer les chaînes
            pass
        
        return channels
    
    def search_match_streams(self, home_team, away_team):
        """Recherche les streams disponibles pour un match spécifique"""
        # Cette fonction peut être étendue pour chercher des liens de streaming
        # pour un match spécifique
        streams = []
        
        try:
            # Rechercher le match sur Kooora
            search_query = f"{home_team} {away_team}"
            # Implémenter la logique de recherche
            pass
            
        except Exception as e:
            print(f"Erreur lors de la recherche de streams: {e}")
        
        return streams
