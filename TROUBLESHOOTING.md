# 🔧 Guide de Dépannage - Mobaryat

## Problème: "لا توجد مباريات في هذا التاريخ" (Aucun match affiché)

### ✅ Solution Vérifiée

Le scraper **fonctionne maintenant parfaitement** et récupère les matchs. Si vous voyez toujours ce message, suivez ces étapes:

### Étape 1: Vérifier que les scrapers fonctionnent

```bash
python test_app_simple.py
```

Vous devriez voir:
- ✅ 15 matchs récupérés depuis Kooora
- ✅ Les équipes, compétitions et heures affichées

### Étape 2: Vérifier les logs de l'application

Quand vous lancez `python app.py`, vous devriez voir:

```
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

Si vous voyez des erreurs, vérifiez:

#### Erreur: "ModuleNotFoundError: No module named 'flask'"
**Solution:**
```bash
pip install flask flask-cors
```

#### Erreur: "Address already in use" (Port 5000 occupé)
**Solution Windows:**
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Solution Linux/Mac:**
```bash
lsof -i :5000
kill -9 <PID>
```

### Étape 3: Tester l'API directement

Avec l'application lancée, ouvrez dans votre navigateur:

```
http://localhost:5000/api/matches/today
```

Vous devriez voir un JSON avec la liste des matchs. Si c'est vide `[]`, c'est que:
- Les scrapers ont un problème de connexion
- Le cache est vide

**Solution:** Supprimez le cache et relancez:
```bash
# Windows
rmdir /s cache
python app.py

# Linux/Mac
rm -rf cache
python app.py
```

### Étape 4: Vérifier la console du navigateur

1. Ouvrez votre navigateur sur http://localhost:5000
2. Appuyez sur **F12** pour ouvrir les outils de développement
3. Allez dans l'onglet **Console**
4. Regardez s'il y a des erreurs

**Erreurs communes:**

#### Erreur: "Failed to fetch"
- Le serveur Flask n'est pas démarré
- Mauvaise URL

#### Erreur: "CORS policy"
- Ajoutez `flask-cors` et redémarrez

### Étape 5: Vérifier que JavaScript charge bien

Dans la console du navigateur, tapez:
```javascript
fetch('/api/matches/today')
  .then(r => r.json())
  .then(data => console.log(data))
```

Si vous voyez la liste des matchs, le problème est dans `app.js`.

---

## Problème: Les matchs se chargent mais les infos sont incorrectes

### Équipes dupliquées ou vides
Le scraper a été corrigé. Si le problème persiste:

1. Vérifiez que vous utilisez la dernière version du scraper
2. Testez avec:
```bash
python test_scrapers.py
```

### Heures ou compétitions manquantes

Le scraper récupère maintenant:
- ✅ Heures des matchs (format HH:MM)
- ✅ Compétitions (دوري أبطال آسيا النخبة, etc.)
- ✅ Scores (si disponibles)

Si ça ne marche pas, la structure HTML du site a peut-être changé.

---

## Problème: Les chaînes ne se chargent pas

### Vérifier les fichiers M3U

Les fichiers suivants doivent exister:
- `bein.m3u`
- `dazn.m3u`
- `espn.m3u`
- `premierleague.m3u`
- `roshnleague.m3u`
- `SeriaA.m3u`
- `generalsports.m3u`
- `mbc.m3u`

### Format M3U correct

Chaque fichier doit avoir ce format:
```
#EXTM3U
#EXTINF:-1,Nom de la Chaîne
http://url-du-stream
#EXTINF:-1,Autre Chaîne
http://autre-url
```

---

## Problème: Les streams ne démarrent pas

C'est normal! Les liens M3U peuvent:
- Expirer
- Être bloqués
- Nécessiter des mises à jour

**Solution:**
Utilisez les scripts dans le dossier `scripts/` pour mettre à jour les liens:
```bash
python scripts/update_bein.py
python scripts/update_dazn_pt.py
```

---

## Test Complet de l'Application

### 1. Test des Scrapers
```bash
python test_scrapers.py
```
**Attendu:** Liste de 15+ matchs avec toutes les infos

### 2. Test Simple
```bash
python test_app_simple.py
```
**Attendu:** Tous les tests passent ✅

### 3. Test de l'Application
```bash
python app.py
```
**Attendu:** Serveur démarre sur http://localhost:5000

### 4. Test de l'API
Dans le navigateur: `http://localhost:5000/api/matches/today`
**Attendu:** JSON avec liste des matchs

### 5. Test de l'Interface
Dans le navigateur: `http://localhost:5000`
**Attendu:** Page avec matchs affichés

---

## Checklist de Dépannage Rapide

- [ ] Python est installé (python --version)
- [ ] Les dépendances sont installées (pip install -r requirements.txt)
- [ ] Le serveur Flask démarre sans erreur
- [ ] L'API retourne des données (/api/matches/today)
- [ ] Les fichiers M3U existent
- [ ] Le cache est vide ou récent (supprimer /cache si nécessaire)
- [ ] Aucune erreur dans la console du navigateur (F12)
- [ ] Le port 5000 n'est pas utilisé par autre chose

---

## Besoin d'Aide Supplémentaire?

### 1. Collectez les informations

```bash
# Version Python
python --version

# Test des scrapers
python test_scrapers.py > debug_scrapers.txt

# Test simple
python test_app_simple.py > debug_simple.txt

# Logs de l'application
python app.py > debug_app.txt 2>&1
```

### 2. Vérifiez les versions

```bash
pip list | findstr "flask beautifulsoup4 requests"
```

Versions recommandées:
- Flask >= 2.0.0
- beautifulsoup4 >= 4.9.0
- requests >= 2.25.0

### 3. Réinstallation Complète

Si tout échoue:

```bash
# Supprimer l'environnement virtuel (si vous en utilisez un)
# Windows
rmdir /s venv

# Linux/Mac
rm -rf venv

# Réinstaller
pip install -r requirements.txt

# Tester
python test_app_simple.py
```

---

## Problèmes Connus

### 1. Sites sources changent leur structure
Les sites comme Kooora, Yallakora changent parfois leur HTML.

**Solution:** Les scrapers doivent être mis à jour. Créez une issue sur GitHub.

### 2. Blocage par certains sites
Certains sites peuvent bloquer les requêtes automatiques.

**Solution:** 
- Utilisez un User-Agent réaliste (déjà fait)
- Ajoutez des délais entre les requêtes
- Utilisez un VPN si nécessaire

### 3. Pas de matchs certains jours
C'est normal! Il n'y a pas de matchs tous les jours.

**Solution:** Naviguez vers un autre jour avec les flèches.

---

## Commandes Utiles

### Nettoyer le cache
```bash
# Windows
rmdir /s /q cache
mkdir cache

# Linux/Mac
rm -rf cache
mkdir cache
```

### Relancer proprement
```bash
# Arrêter (Ctrl+C)
# Nettoyer le cache
# Relancer
python app.py
```

### Vérifier les ports utilisés
```bash
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000
```

---

## Contact et Support

Si le problème persiste après avoir suivi ce guide:

1. 📝 Créez une issue sur GitHub avec:
   - La sortie de `python test_app_simple.py`
   - Les erreurs dans la console du navigateur
   - La version de Python
   - Votre système d'exploitation

2. 📧 Incluez les logs de l'application

3. 🖼️ Joignez des captures d'écran si possible

---

**Dernière mise à jour:** 2024-01-15
**Version:** 1.0.0
