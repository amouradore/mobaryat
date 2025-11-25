"""
Script de test pour les scrapers de matchs
Utilisez ce script pour tester vos scrapers individuellement
"""

import sys
from datetime import datetime
from scrapers.kooora_scraper import KooraMatches
from scrapers.yallakora_scraper import YallaKoraMatches
from scrapers.filgoal_scraper import FilgoalMatches
from scrapers.api_football import APIFootballMatches

def print_separator():
    print("\n" + "="*80 + "\n")

def test_scraper(scraper_name, scraper_instance):
    """Test un scraper spécifique"""
    print(f"🔍 Test du scraper: {scraper_name}")
    print(f"{'─'*80}")
    
    try:
        # Récupérer les matchs du jour
        print("⏳ Récupération des matchs du jour...")
        matches = scraper_instance.get_today_matches()
        
        if not matches:
            print(f"⚠️  Aucun match trouvé (cela peut être normal s'il n'y a pas de matchs aujourd'hui)")
            return
        
        print(f"✅ {len(matches)} match(s) trouvé(s)")
        print()
        
        # Afficher les 5 premiers matchs
        max_display = min(5, len(matches))
        print(f"📋 Affichage des {max_display} premier(s) match(s):")
        print()
        
        for i, match in enumerate(matches[:max_display], 1):
            print(f"Match #{i}:")
            print(f"  🏠 Équipe à domicile: {match.get('home_team', 'N/A')}")
            print(f"  ✈️  Équipe à l'extérieur: {match.get('away_team', 'N/A')}")
            print(f"  ⏰ Heure: {match.get('time', 'N/A')}")
            print(f"  📅 Date: {match.get('date', 'N/A')}")
            print(f"  ⚽ Score: {match.get('score', 'N/A')}")
            print(f"  🏆 Compétition: {match.get('competition', 'N/A')}")
            print(f"  📊 Statut: {match.get('status', 'N/A')}")
            print(f"  🔴 En direct: {'Oui' if match.get('is_live') else 'Non'}")
            
            if match.get('channels'):
                print(f"  📺 Chaînes: {', '.join(match['channels'])}")
            
            print()
        
        # Statistiques
        live_count = sum(1 for m in matches if m.get('is_live'))
        finished_count = sum(1 for m in matches if m.get('status') == 'Finished')
        scheduled_count = sum(1 for m in matches if m.get('status') == 'Scheduled')
        
        print(f"📊 Statistiques:")
        print(f"  • Total: {len(matches)} matchs")
        print(f"  • En direct: {live_count}")
        print(f"  • Terminés: {finished_count}")
        print(f"  • À venir: {scheduled_count}")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """Fonction principale"""
    print("="*80)
    print("🧪 TEST DES SCRAPERS - MOBARYAT")
    print("="*80)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_separator()
    
    # Liste des scrapers à tester
    scrapers = [
        ("Kooora", KooraMatches()),
        ("Yallakora", YallaKoraMatches()),
        ("Filgoal", FilgoalMatches()),
        ("API-Football", APIFootballMatches()),
    ]
    
    # Tester chaque scraper
    for scraper_name, scraper_instance in scrapers:
        test_scraper(scraper_name, scraper_instance)
        print_separator()
    
    print("✅ Tests terminés!")
    print()
    
    # Résumé
    print("💡 Conseils:")
    print("  • Si un scraper ne retourne aucun match, vérifiez que le site est accessible")
    print("  • La structure HTML des sites peut changer, nécessitant des mises à jour")
    print("  • Pour API-Football, assurez-vous d'avoir configuré votre clé API")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur fatale: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
