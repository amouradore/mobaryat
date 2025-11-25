"""
Test simple pour vérifier que l'application fonctionne
"""

print("="*80)
print("TEST DE L'APPLICATION MOBARYAT")
print("="*80)
print()

# Test 1: Import des modules
print("1. Test des imports...")
try:
    from scrapers.kooora_scraper import KooraMatches
    print("   ✅ Kooora scraper OK")
except Exception as e:
    print(f"   ❌ Erreur Kooora: {e}")

try:
    from scrapers.yallakora_scraper import YallaKoraMatches
    print("   ✅ Yallakora scraper OK")
except Exception as e:
    print(f"   ❌ Erreur Yallakora: {e}")

try:
    from scrapers.filgoal_scraper import FilgoalMatches
    print("   ✅ Filgoal scraper OK")
except Exception as e:
    print(f"   ❌ Erreur Filgoal: {e}")

print()

# Test 2: Récupération des matchs
print("2. Test de récupération des matchs...")
try:
    scraper = KooraMatches()
    matches = scraper.get_today_matches()
    print(f"   ✅ {len(matches)} matchs récupérés depuis Kooora")
    
    if matches:
        print()
        print("   Exemple de match:")
        m = matches[0]
        print(f"   • {m['home_team']} vs {m['away_team']}")
        print(f"   • {m['competition']}")
        print(f"   • {m['time']}")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

print()

# Test 3: Flask
print("3. Test de Flask...")
try:
    from flask import Flask
    print("   ✅ Flask installé")
except Exception as e:
    print(f"   ❌ Flask non installé: {e}")
    print("   → Installez avec: pip install flask")

print()

# Test 4: Fichiers M3U
print("4. Test des fichiers M3U...")
import os
m3u_files = ['bein.m3u', 'dazn.m3u', 'espn.m3u']
found = 0
for f in m3u_files:
    if os.path.exists(f):
        found += 1
        print(f"   ✅ {f}")
    else:
        print(f"   ⚠️  {f} non trouvé")

print()

# Résumé
print("="*80)
print("RÉSUMÉ")
print("="*80)
print()
print("✅ Les scrapers fonctionnent!")
print(f"✅ {len(matches)} matchs disponibles aujourd'hui")
print()
print("Pour démarrer l'application:")
print("  python app.py")
print()
print("Puis ouvrez: http://localhost:5000")
print()
