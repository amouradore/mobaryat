# 🚀 Guide de Démarrage Rapide

## Pour les Débutants - Lancer l'Application en 3 Minutes!

### 📋 Ce dont vous avez besoin

1. **Python** installé sur votre ordinateur
   - Windows: Téléchargez depuis [python.org](https://www.python.org/downloads/)
   - Mac: `brew install python3`
   - Linux: `sudo apt install python3 python3-pip`

2. **Internet** - Pour scraper les données de matchs

---

## 🪟 Windows - Démarrage Ultra-Rapide

### Méthode 1: Double-clic (Le plus simple!)
1. Trouvez le fichier `start.bat` dans le dossier
2. **Double-cliquez** dessus
3. Une fenêtre noire s'ouvre et installe tout automatiquement
4. Attendez quelques secondes...
5. Ouvrez votre navigateur et allez sur: **http://localhost:5000**
6. 🎉 C'est tout!

### Méthode 2: Ligne de commande
```powershell
# Ouvrir PowerShell dans le dossier du projet
# Clic droit sur le dossier > "Ouvrir dans le Terminal"

# Lancer
.\start.bat
```

---

## 🍎 Mac / 🐧 Linux - Démarrage Ultra-Rapide

### Dans le Terminal:
```bash
# Naviguer vers le dossier
cd chemin/vers/mobaryat

# Rendre le script exécutable (une seule fois)
chmod +x start.sh

# Lancer l'application
./start.sh
```

Ou en une seule commande:
```bash
chmod +x start.sh && ./start.sh
```

---

## 🌐 Accéder à l'Application

Une fois lancée, ouvrez votre navigateur et allez sur:
- **http://localhost:5000** 
- ou **http://127.0.0.1:5000**

---

## 🎯 Que Faire Maintenant?

### Sur la Page d'Accueil
1. 📅 **Voir les matchs du jour** - Automatiquement affichés
2. ⬅️➡️ **Changer de date** - Utilisez les flèches
3. 🔴 **Filtrer** - Cliquez sur "مباشر" pour voir les matchs en direct
4. ▶️ **Regarder** - Cliquez sur "مشاهدة" sur un match

### Sur la Page des Chaînes
1. 📺 **Cliquez sur "القنوات"** dans le menu
2. 🔍 **Recherchez une chaîne** - Tapez dans la barre de recherche
3. 🏷️ **Filtrez par catégorie** - beIN, DAZN, ESPN, etc.
4. ▶️ **Regardez** - Cliquez sur une chaîne

---

## ⚠️ Problèmes Courants et Solutions

### ❌ "Python n'est pas reconnu..."
**Solution:** Python n'est pas installé ou pas dans le PATH
- Téléchargez Python depuis [python.org](https://www.python.org/downloads/)
- ⚠️ **Important:** Cochez "Add Python to PATH" lors de l'installation!

### ❌ "Le port 5000 est déjà utilisé"
**Solution:** Une autre application utilise ce port
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <numero_pid> /F

# Mac/Linux
lsof -i :5000
kill -9 <PID>
```

### ❌ "Aucun match trouvé"
**Solution:** C'est normal! Les sites peuvent:
- Ne pas avoir de matchs aujourd'hui
- Avoir changé leur structure HTML
- Être temporairement inaccessibles

**Essayez:**
- Changer de date avec les flèches
- Attendre quelques minutes et rafraîchir
- Vérifier votre connexion Internet

### ❌ "Les chaînes ne se chargent pas"
**Solution:** Vérifiez que les fichiers `.m3u` existent:
- `bein.m3u`
- `dazn.m3u`
- `espn.m3u`
- etc.

### ❌ "Le stream ne démarre pas"
**Solution:** Les liens de streaming peuvent:
- Avoir expiré
- Nécessiter une mise à jour
- Être bloqués dans votre région

---

## 🔧 Configuration Optionnelle

### Activer API-Football (Optionnel)
Pour obtenir plus de données de matchs:

1. Créez un compte gratuit sur [api-football.com](https://www.api-football.com/)
2. Obtenez votre clé API
3. Ajoutez-la:

**Windows:**
```powershell
setx API_FOOTBALL_KEY "votre_cle_api"
```

**Mac/Linux:**
```bash
echo 'export API_FOOTBALL_KEY="votre_cle_api"' >> ~/.bashrc
source ~/.bashrc
```

---

## 🧪 Tester les Scrapers

Pour vérifier que les scrapers fonctionnent:

**Windows:**
```powershell
.\run_tests.bat
```

**Mac/Linux:**
```bash
chmod +x run_tests.sh
./run_tests.sh
```

Cela testera tous les scrapers et affichera les résultats.

---

## 🛑 Arrêter l'Application

Dans la fenêtre où l'application tourne:
- **Windows/Mac/Linux:** Appuyez sur `Ctrl + C`
- Ou fermez simplement la fenêtre du terminal

---

## 📱 Accéder depuis un Téléphone

Si vous voulez accéder à l'application depuis votre téléphone:

1. Assurez-vous que votre téléphone et ordinateur sont sur le **même WiFi**
2. Trouvez l'adresse IP de votre ordinateur:

**Windows:**
```powershell
ipconfig
# Cherchez "Adresse IPv4"
```

**Mac:**
```bash
ifconfig | grep "inet "
# Cherchez une adresse comme 192.168.x.x
```

**Linux:**
```bash
ip addr show
# Cherchez une adresse comme 192.168.x.x
```

3. Sur votre téléphone, ouvrez le navigateur et allez sur:
   - `http://VOTRE_IP:5000`
   - Exemple: `http://192.168.1.100:5000`

---

## 📚 Documentation Complète

Pour plus de détails:
- **README.md** - Documentation complète
- **GUIDE_SCRAPERS.md** - Créer de nouveaux scrapers
- **DEPLOYMENT.md** - Déployer sur un serveur
- **CHANGELOG.md** - Historique des versions

---

## 🆘 Besoin d'Aide?

1. 📖 Lisez le **README.md**
2. 🔍 Consultez la section "Dépannage"
3. 🧪 Testez les scrapers avec `run_tests.bat` ou `run_tests.sh`
4. 💬 Ouvrez une Issue sur GitHub
5. 📧 Contactez le support

---

## 🎉 Profitez de l'Application!

Maintenant vous pouvez:
- ⚽ Voir tous les matchs du jour
- 📺 Regarder vos chaînes sportives préférées
- 🔴 Suivre les matchs en direct
- 📅 Naviguer entre les dates

**Bon visionnage! 🍿**

---

## 💡 Astuces Pro

### Rafraîchissement Automatique
L'application se met à jour automatiquement toutes les 2 minutes. Pas besoin de rafraîchir manuellement!

### Raccourcis Clavier
- `F5` - Rafraîchir la page
- `Ctrl + F` - Rechercher sur la page
- `F11` - Plein écran (pratique pour regarder!)

### Favoris
Ajoutez `http://localhost:5000` à vos favoris pour un accès rapide!

### Multi-onglets
Ouvrez plusieurs onglets pour regarder plusieurs matchs en même temps!

---

**Note:** Cette application est à des fins éducatives uniquement. Respectez les droits d'auteur et les conditions d'utilisation des sites sources.
