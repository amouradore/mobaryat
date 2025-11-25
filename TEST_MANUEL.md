# 📋 Guide de Test Manuel - Application Mobaryat

## 🚀 Lancement de l'Application

### Windows
```bash
python app.py
```

### Linux/Mac
```bash
python3 app.py
```

L'application démarre sur: **http://localhost:5000**

---

## ✅ Tests à Effectuer

### 1. Test de la Page Principale (/)

**URL:** http://localhost:5000

**À vérifier:**
- ✅ La page se charge correctement
- ✅ Les matchs du jour s'affichent
- ✅ Les chaînes diffuseurs sont visibles pour chaque match
- ✅ Les logos des équipes s'affichent
- ✅ Les scores et horaires sont corrects

**Exemple de match à vérifier:**
- Rechercher un match avec plusieurs chaînes
- Vérifier que les noms de chaînes sont spécifiques (ex: "beIN Sports Mena 2" au lieu de juste "beIN SPORTS")

---

### 2. Test de la Page des Chaînes (/channels)

**URL:** http://localhost:5000/channels

**À vérifier:**

#### 2.1. Chargement Initial
- ✅ La page affiche toutes les chaînes (73 au total)
- ✅ Les cartes de chaînes sont bien organisées

#### 2.2. Filtre "Sky Sports"
1. Cliquer sur le bouton **"Sky Sports"**
2. Vérifier que **12 chaînes** s'affichent:
   - UK-Sky Cinema Premier
   - UK-Sky Sports Action
   - UK-Sky Sports Arena
   - UK Sky Sports F1 FHD (D)
   - UK Sky Sports Golf FHD
   - UK-Sky Sports Main Event
   - UK Sky Sports Mix FHD (D)
   - UK-Sky Sports News
   - UK Sky Sports Cricket FHD (D)
   - UK Sky Sports F1 FHD
   - UK: SKY SPORTS ARENA FHD
   - UK: SKY SPORTS MAIN EVENT HD

#### 2.3. Filtre "ESPN"
1. Cliquer sur le bouton **"ESPN"**
2. Vérifier que **7 chaînes** s'affichent:
   - ESPN 1
   - ESPN 2
   - ESPN 3
   - ESPN 4
   - ESPN 5
   - ESPN 6
   - ESPN 7

#### 2.4. Recherche
1. Taper "Sky" dans la barre de recherche
2. Vérifier que seules les chaînes Sky s'affichent
3. Effacer la recherche
4. Taper "ESPN"
5. Vérifier que seules les chaînes ESPN s'affichent

#### 2.5. Lecture d'une Chaîne
1. Cliquer sur une chaîne Sky ou ESPN
2. Vérifier que le lecteur vidéo se charge
3. Vérifier que le titre de la chaîne s'affiche correctement

---

### 3. Test de l'API - Matchs du Jour

**URL:** http://localhost:5000/api/matches/today

**Méthode de test:**

#### Via le Navigateur:
1. Ouvrir l'URL dans le navigateur
2. Vérifier le JSON retourné

#### Via curl:
```bash
curl http://localhost:5000/api/matches/today
```

**À vérifier dans la réponse JSON:**
```json
[
  {
    "home_team": "Nom de l'équipe",
    "away_team": "Nom de l'équipe",
    "channels": [
      {
        "name": "beIN Sports Mena 2",  // ← Nom spécifique
        "logo": "..."
      }
    ],
    ...
  }
]
```

**Points de contrôle:**
- ✅ Chaque match a une liste de `channels`
- ✅ Les noms de chaînes sont **spécifiques** (pas génériques)
- ✅ Au moins 10 matchs sur 15 ont des chaînes

---

### 4. Test de l'API - Chaînes Disponibles

**URL:** http://localhost:5000/api/channels

**Méthode de test:**

#### Via le Navigateur:
1. Ouvrir l'URL dans le navigateur
2. Compter les chaînes par catégorie

#### Via curl:
```bash
# Toutes les chaînes
curl http://localhost:5000/api/channels

# Compter les chaînes Sky (avec jq)
curl http://localhost:5000/api/channels | jq '[.[] | select(.category=="sky")] | length'

# Compter les chaînes ESPN (avec jq)
curl http://localhost:5000/api/channels | jq '[.[] | select(.category=="espn")] | length'
```

**À vérifier:**
- ✅ Total: **73 chaînes**
- ✅ Sky: **12 chaînes**
- ✅ ESPN: **7 chaînes**

**Structure JSON attendue:**
```json
[
  {
    "name": "UK-Sky Sports Action",
    "url": "http://...",
    "category": "sky",
    "logo": "/static/logos/sky.png"
  },
  {
    "name": "ESPN 1",
    "url": "http://...",
    "category": "espn",
    "logo": "/static/logos/espn.png"
  }
]
```

---

## 🔍 Test avec Python

Créer un fichier `test_integration.py`:

```python
import requests

# Test 1: Chaînes disponibles
print("Test 1: API Channels")
response = requests.get('http://localhost:5000/api/channels')
channels = response.json()

sky_channels = [ch for ch in channels if ch['category'] == 'sky']
espn_channels = [ch for ch in channels if ch['category'] == 'espn']

print(f"✅ Total chaînes: {len(channels)}")
print(f"✅ Sky Sports: {len(sky_channels)} chaînes")
print(f"✅ ESPN: {len(espn_channels)} chaînes")

# Test 2: Matchs du jour
print("\nTest 2: API Matches")
response = requests.get('http://localhost:5000/api/matches/today')
matches = response.json()

matches_with_channels = [m for m in matches if m.get('channels')]
print(f"✅ Matchs du jour: {len(matches)}")
print(f"✅ Matchs avec chaînes: {len(matches_with_channels)}")

# Afficher un exemple
if matches_with_channels:
    match = matches_with_channels[0]
    print(f"\nExemple de match:")
    print(f"  {match['home_team']} vs {match['away_team']}")
    print(f"  Chaînes: {[ch['name'] for ch in match['channels'][:3]]}")
```

Exécuter:
```bash
python test_integration.py
```

---

## ✅ Résultats Attendus

### Récapitulatif des Tests

| Test | Résultat Attendu |
|------|------------------|
| Page principale | Matchs avec chaînes spécifiques |
| Page chaînes - Total | 73 chaînes affichées |
| Page chaînes - Filtre Sky | 12 chaînes Sky |
| Page chaînes - Filtre ESPN | 7 chaînes ESPN |
| API /api/channels | JSON avec 73 chaînes |
| API /api/matches/today | Matchs avec chaînes détaillées |
| Recherche "Sky" | Résultats filtrés |
| Lecture vidéo | Lecteur se charge |

---

## 🐛 Problèmes Courants

### Problème: Aucune chaîne ne s'affiche
**Solution:** Vérifier que les fichiers `sky_channels.m3u` et `espn.m3u` existent à la racine

### Problème: Le cache affiche de vieilles données
**Solution:** Supprimer le dossier `cache/`
```bash
rm -rf cache/
# ou sur Windows
rmdir /s cache
```

### Problème: Erreur 404 sur les logos
**Solution:** Les logos peuvent être manquants, c'est normal. L'application utilise des icônes par défaut.

---

## 📊 Métriques de Succès

✅ **100% de réussite si:**
- Les 73 chaînes sont accessibles via l'API
- Les 12 chaînes Sky s'affichent dans l'interface
- Les 7 chaînes ESPN s'affichent dans l'interface
- Les matchs affichent des chaînes avec noms spécifiques
- Tous les filtres fonctionnent correctement

---

**Date de création:** 2025-01-25  
**Version de l'application:** 1.0  
**Statut:** ✅ Prêt pour les tests
