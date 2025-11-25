# 🧪 Guide de Test - Bouton VLC pour Eleven Sports et Sky

## 🎯 Objectif

Tester le nouveau bouton VLC qui permet d'ouvrir directement les chaînes Eleven Sports et Sky dans VLC.

---

## 📋 Prérequis

- ✅ VLC Media Player installé
- ✅ Application lancée (`python app.py`)
- ✅ Cache supprimé (`rm -rf cache/`)

---

## 🚀 Test 1: Visualiser le Bouton VLC

### Étapes:

1. **Lancer l'application**
```bash
python app.py
```

2. **Ouvrir dans le navigateur**
```
http://localhost:5000/channels
```

3. **Cliquer sur "Eleven Sports"**
   - Le filtre affiche 4 chaînes

4. **Observer les cartes de chaînes**
   - Chaque carte devrait avoir un **bouton orange "VLC"** en haut à droite
   - Le bouton affiche: `🔗 VLC`

5. **Cliquer sur "Sky Sports"**
   - Le filtre affiche 12 chaînes
   - Toutes ont également le bouton orange VLC

### Résultat attendu:

```
┌─────────────────────────────────┐
│  🔗 VLC                         │  ← Bouton orange en haut à droite
│                                 │
│         📺                      │
│   PT Eleven Sports 1 FHD        │
│      elevendazn                 │
│                                 │
│    [ ▶️ مشاهدة ]               │  ← Bouton bleu "Regarder"
└─────────────────────────────────┘
```

**✅ Succès si:** Le bouton orange VLC est visible sur toutes les chaînes Eleven et Sky

---

## 🧪 Test 2: Tester le Bouton VLC

### Étapes:

1. **Cliquer sur le bouton orange "VLC"** (pas sur la carte)
   - PAS sur le bouton bleu "مشاهدة"
   - PAS sur la carte entière
   - UNIQUEMENT sur le petit bouton orange "VLC"

2. **Observer ce qui se passe:**

#### Scénario A: VLC s'ouvre automatiquement ✅

```
→ VLC se lance
→ Le flux commence à charger
→ La chaîne s'affiche dans VLC
```

**Bravo !** Le protocole `vlc://` fonctionne sur votre système.

#### Scénario B: Message de confirmation apparaît

```
┌──────────────────────────────────────┐
│ Ouverture de "PT Eleven Sports 1    │
│ FHD" dans VLC...                     │
│                                      │
│ Si VLC ne s'ouvre pas automatique-   │
│ ment, voulez-vous copier l'URL?     │
│                                      │
│     [ Annuler ]     [ OK ]          │
└──────────────────────────────────────┘
```

**Action:** Cliquez sur **OK** pour copier l'URL

#### Scénario C: URL copiée dans le presse-papier ✅

```
┌──────────────────────────────────────┐
│ URL copiée!                          │
│                                      │
│ Ouvrez VLC puis:                     │
│ 1. Média → Ouvrir un flux réseau     │
│ 2. Collez l'URL (Ctrl+V)             │
│ 3. Cliquez sur Lire                  │
│                                      │
│            [ OK ]                    │
└──────────────────────────────────────┘
```

**Action:** Suivez les instructions pour ouvrir dans VLC manuellement

---

## 🎬 Test 3: Lecture Manuelle dans VLC

Si le bouton automatique ne fonctionne pas, testez manuellement:

### Étapes:

1. **Ouvrir VLC**

2. **Menu → Média → Ouvrir un flux réseau** (ou `Ctrl+N`)

3. **Coller une URL de test:**
```
http://tv14s.xyz:8080/Zkv3Zw/765991/35264
```
Note: **SANS** .m3u8 pour VLC

4. **Cliquer sur "Lire"**

### Résultat attendu:

- ✅ VLC charge le flux
- ✅ La vidéo commence à jouer
- ✅ La qualité est bonne (FHD/HD)

**Si ça fonctionne:** Le problème vient du protocole `vlc://` qui n'est pas configuré
**Si ça ne fonctionne pas:** L'URL/token peut être expiré

---

## 🔍 Test 4: Comparer Navigateur vs VLC

### Test dans le Navigateur:

1. **Cliquer sur une carte Eleven Sports** (pas sur le bouton VLC)
2. **Cliquer sur le bouton bleu "مشاهدة"**
3. **Observer le lecteur:**

#### Résultat A: Ça fonctionne ✅
```
Console (F12):
- Manifest chargé, démarrage de la lecture...
→ La vidéo se lance dans le navigateur
```

#### Résultat B: Erreur CORS ❌
```
Console (F12):
- CORS error: No 'Access-Control-Allow-Origin' header
→ Le serveur bloque les navigateurs
→ Utiliser le bouton VLC
```

#### Résultat C: Erreur Network ❌
```
Console (F12):
- Network error / Failed to fetch
→ Le serveur refuse la connexion
→ Utiliser le bouton VLC
```

### Test dans VLC (via bouton):

1. **Cliquer sur le bouton orange "VLC"**
2. **VLC s'ouvre (ou copier l'URL)**
3. **La chaîne se lance**

**Comparaison:**
- Navigateur: Peut ne pas fonctionner (CORS, restrictions serveur)
- VLC: Fonctionne toujours ✅

---

## 📊 Résultats Attendus

### Configuration Idéale:

| Test | Résultat | Statut |
|------|----------|--------|
| Bouton VLC visible | 16 boutons (4 Eleven + 12 Sky) | ✅ |
| Clic sur bouton VLC | VLC s'ouvre OU URL copiée | ✅ |
| Lecture dans VLC | Flux fonctionne | ✅ |
| Design bouton | Orange, en haut à droite | ✅ |

### Si le protocole vlc:// ne fonctionne pas:

**Symptôme:** Message de confirmation apparaît mais VLC ne s'ouvre pas

**Solution 1: Configurer le protocole vlc://**

**Windows:**
1. Installer VLC normalement
2. Lors de l'installation, cocher "Register file associations"
3. OU manuellement:
   - Ouvrir VLC
   - Outils → Préférences
   - Cocher "Associer les fichiers avec VLC"

**Mac:**
1. Le protocole vlc:// devrait fonctionner par défaut
2. Si pas, autoriser VLC dans Préférences Système → Sécurité

**Linux:**
```bash
# Créer le handler
xdg-mime default vlc.desktop x-scheme-handler/vlc
```

**Solution 2: Utiliser la copie d'URL**
- Cliquer OK quand le message apparaît
- L'URL est copiée automatiquement
- Ouvrir VLC et coller (Ctrl+N → Ctrl+V → Lire)

---

## 🎯 Cas d'Usage Réels

### Utilisateur A: "Je veux regarder dans le navigateur"

```
1. Cliquer sur la carte (ou bouton bleu "مشاهدة")
2. Si ça fonctionne → Super! ✅
3. Si ça ne fonctionne pas → Utiliser le bouton VLC
```

### Utilisateur B: "Je préfère VLC directement"

```
1. Cliquer sur le bouton orange "VLC"
2. VLC s'ouvre avec le flux ✅
3. Pas besoin d'utiliser le navigateur
```

### Utilisateur C: "Rien ne fonctionne automatiquement"

```
1. Cliquer sur le bouton VLC
2. Cliquer OK pour copier l'URL
3. Ouvrir VLC manuellement
4. Ctrl+N → Ctrl+V → Lire ✅
```

---

## 🐛 Dépannage

### Problème 1: Le bouton VLC n'apparaît pas

**Vérification:**
```bash
# Vider le cache
rm -rf cache/

# Relancer l'application
python app.py

# Rafraîchir le navigateur (Ctrl+F5)
```

**Vérifier dans la console:**
```javascript
// Ouvrir la console (F12)
// Vérifier que la fonction existe
console.log(typeof openInVLC);
// Doit afficher: "function"
```

### Problème 2: VLC ne s'ouvre pas automatiquement

**Solution:**
- Utiliser la copie d'URL (cliquer OK quand demandé)
- OU configurer le protocole vlc:// (voir ci-dessus)

### Problème 3: URL copiée ne fonctionne pas dans VLC

**Vérification:**
- Assurez-vous de coller l'URL **sans** .m3u8
- Format correct: `http://tv14s.xyz:8080/Zkv3Zw/765991/35264`
- Format incorrect: `http://tv14s.xyz:8080/Zkv3Zw/765991/35264.m3u8`

**Note:** Le bouton VLC enlève automatiquement .m3u8

### Problème 4: Erreur "URL non valide" dans VLC

**Causes possibles:**
- Token expiré dans l'URL
- Serveur IPTV hors ligne
- Besoin d'authentification supplémentaire

**Solution:**
- Mettre à jour les fichiers M3U avec de nouvelles URLs
- Contacter le fournisseur IPTV

---

## ✅ Checklist Finale

Avant de considérer le test terminé, vérifiez:

- [ ] Boutons VLC visibles sur Eleven Sports (4 chaînes)
- [ ] Boutons VLC visibles sur Sky Sports (12 chaînes)
- [ ] Bouton VLC a le bon design (orange, en haut à droite)
- [ ] Clic sur bouton VLC ne lance PAS le lecteur web
- [ ] VLC s'ouvre OU URL est copiée
- [ ] Le flux fonctionne dans VLC
- [ ] Les autres catégories (beIN, ESPN, etc.) n'ont PAS de bouton VLC

---

## 📸 Captures d'Écran Attendues

### Vue de la page avec boutons VLC:

```
┌──────────────┬──────────────┬──────────────┐
│ 🔗 VLC       │ 🔗 VLC       │ 🔗 VLC       │
│     📺       │     📺       │     📺       │
│  Eleven 1    │  Eleven 3    │  Eleven 4    │
│  elevendazn  │  elevendazn  │  elevendazn  │
│ [▶️ مشاهدة] │ [▶️ مشاهدة] │ [▶️ مشاهدة] │
└──────────────┴──────────────┴──────────────┘
```

### Bouton VLC au survol:

```
┌─────────────────────────────────┐
│  🔗 VLC  ← Légèrement agrandi   │
│       (effet zoom)               │
│         📺                       │
│   PT Eleven Sports 1 FHD         │
└─────────────────────────────────┘
```

---

**Date de création:** 2025-01-25  
**Version:** 1.0  
**Statut:** ✅ Prêt pour les tests
