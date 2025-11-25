"""
Mapping des compétitions et leurs chaînes de diffusion
Basé sur les droits de diffusion connus
"""

COMPETITION_CHANNELS = {
    # Compétitions asiatiques
    "دوري أبطال آسيا النخبة": [
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"},
        {"name": "SSC Sport", "logo": "/static/logos/ssc.png"}
    ],
    "دوري أبطال آسيا 2": [
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"}
    ],
    
    # Ligues européennes
    "الدوري الإنجليزي الممتاز": [
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"},
        {"name": "Shahid", "logo": "/static/logos/shahid.png"}
    ],
    "Premier League": [
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"}
    ],
    "الدوري الإسباني": [
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"}
    ],
    "La Liga": [
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"}
    ],
    "الدوري الإيطالي": [
        {"name": "SSC Sport", "logo": "/static/logos/ssc.png"},
        {"name": "Starzplay", "logo": "/static/logos/starzplay.png"}
    ],
    "Serie A": [
        {"name": "SSC Sport", "logo": "/static/logos/ssc.png"}
    ],
    "الدوري الألماني": [
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"}
    ],
    "Bundesliga": [
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"}
    ],
    "الدوري الفرنسي": [
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"}
    ],
    "Ligue 1": [
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"}
    ],
    
    # Ligues arabes
    "دوري روشن السعودي": [
        {"name": "SSC Sport", "logo": "/static/logos/ssc.png"},
        {"name": "Thmanyah", "logo": "/static/logos/thmanyah.png"}
    ],
    "Roshn League": [
        {"name": "SSC Sport", "logo": "/static/logos/ssc.png"}
    ],
    "الدوري المصري": [
        {"name": "ON Sport", "logo": "/static/logos/onsport.png"},
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"}
    ],
    "دوري nile": [
        {"name": "ON Sport", "logo": "/static/logos/onsport.png"}
    ],
    "دوري الخليج العربي": [
        {"name": "Abu Dhabi Sports", "logo": "/static/logos/adtv.png"}
    ],
    "دوري قطر": [
        {"name": "Alkass", "logo": "/static/logos/alkass.png"}
    ],
    
    # Compétitions européennes
    "دوري أبطال أوروبا": [
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"}
    ],
    "UEFA Champions League": [
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"}
    ],
    "الدوري الأوروبي": [
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"}
    ],
    "UEFA Europa League": [
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"}
    ],
    "دوري المؤتمر الأوروبي": [
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"}
    ],
    
    # Autres compétitions
    "كأس العالم للأندية": [
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"},
        {"name": "FIFA+", "logo": "/static/logos/fifa.png"}
    ],
    "كأس الأمم الأفريقية": [
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"}
    ],
    "Copa America": [
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"}
    ],
}

def get_channels_for_competition(competition_name):
    """
    Retourne les chaînes de diffusion pour une compétition donnée
    """
    if not competition_name:
        return []
    
    # Recherche exacte
    if competition_name in COMPETITION_CHANNELS:
        return COMPETITION_CHANNELS[competition_name]
    
    # Recherche partielle
    competition_lower = competition_name.lower()
    for key, channels in COMPETITION_CHANNELS.items():
        if key.lower() in competition_lower or competition_lower in key.lower():
            return channels
    
    # Par défaut, retourner beIN SPORTS (diffuse la plupart des matchs)
    return [
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"}
    ]

def add_channels_to_matches(matches):
    """
    Ajoute les chaînes de diffusion aux matchs basé sur la compétition
    """
    for match in matches:
        if not match.get('channels') or len(match['channels']) == 0:
            competition = match.get('competition', '')
            match['channels'] = get_channels_for_competition(competition)
    
    return matches
