# 🎨 Guide des Logos - Mobaryat

## Logos Actuellement Affichés

L'application affiche maintenant:
- ✅ **Logos des équipes** - Extraits automatiquement depuis Kooora.com
- ✅ **Logos des compétitions** - Depuis Kooora.com
- ✅ **Chaînes de diffusion** - Basées sur un mapping des compétitions

## Structure des Logos

### Logos des Équipes et Compétitions
Ces logos sont automatiquement récupérés depuis Kooora.com via l'URL:
```
https://cdn.sportfeeds.io/sdl/images/team/crest/small/[ID].png
```

Aucune action requise - ils sont extraits automatiquement!

### Logos des Chaînes de Diffusion

Les logos des chaînes doivent être placés dans: `static/logos/`

#### Fichiers Requis

Créez ou téléchargez ces fichiers PNG:

```
static/logos/
├── bein.png          # beIN SPORTS
├── ssc.png           # SSC Sport
├── shahid.png        # Shahid
├── starzplay.png     # Starzplay
├── onsport.png       # ON Sport
├── adtv.png          # Abu Dhabi Sports
├── alkass.png        # Alkass
├── fifa.png          # FIFA+
├── thmanyah.png      # Thmanyah
├── espn.png          # ESPN (optionnel)
├── dazn.png          # DAZN (optionnel)
└── tnt.png           # TNT Sports (optionnel)
```

## Comment Obtenir les Logos

### Option 1: Téléchargement Officiel (Recommandé)

1. **beIN SPORTS**
   - Site: https://www.beinmedia.com
   - Cherchez "Media Kit" ou "Press"

2. **SSC Sport**
   - Site: https://www.sscsports.com
   - Section "About" ou "Media"

3. **Shahid**
   - Site: https://shahid.mbc.net
   - Footer > Press Kit

4. **Google Images**
   ```
   Recherchez: "[nom de la chaîne] logo png transparent"
   ```
   - Choisissez des images haute résolution (300x150 minimum)
   - Préférez les PNG avec fond transparent

### Option 2: Création Manuelle

Si vous ne trouvez pas de logos officiels, créez-les avec:

#### En ligne:
- **Canva** (https://www.canva.com)
- **Figma** (https://www.figma.com)
- **LogoMakr** (https://logomakr.com)

#### Dimensions recommandées:
- Largeur: 120-200px
- Hauteur: 60-80px
- Format: PNG avec fond transparent
- Résolution: 72-150 DPI

### Option 3: Utiliser des Placeholders SVG

Des fichiers SVG placeholder ont été créés:
```
static/logos/*.png.svg
```

Pour les utiliser:
1. Renommez `.png.svg` en `.png` OU
2. Utilisez un convertisseur SVG vers PNG en ligne

## Mapping des Compétitions et Chaînes

Édité dans: `scrapers/channels_mapping.py`

```python
COMPETITION_CHANNELS = {
    "دوري أبطال آسيا النخبة": [
        {"name": "beIN SPORTS", "logo": "/static/logos/bein.png"},
        {"name": "SSC Sport", "logo": "/static/logos/ssc.png"}
    ],
    # ... autres compétitions
}
```

### Ajouter une Nouvelle Compétition

1. Ouvrez `scrapers/channels_mapping.py`
2. Ajoutez une entrée dans `COMPETITION_CHANNELS`:
```python
"Nom de la Compétition": [
    {"name": "Nom Chaîne", "logo": "/static/logos/chaine.png"}
],
```

### Ajouter une Nouvelle Chaîne

1. Téléchargez le logo: `static/logos/nouvelle_chaine.png`
2. Ajoutez-la dans les compétitions concernées
3. Redémarrez l'application

## Styles des Logos

### Dans l'Interface

Les logos sont stylisés via CSS dans `static/css/style.css`:

```css
.team-logo-img {
    width: 60px;
    height: 60px;
    object-fit: contain;
}

.channel-logo {
    height: 30px;
    max-width: 80px;
    padding: 0.25rem 0.5rem;
}

.competition-logo {
    width: 24px;
    height: 24px;
}
```

### Personnaliser la Taille

Modifiez les valeurs dans `style.css`:
```css
.team-logo-img {
    width: 80px;    /* Plus grand */
    height: 80px;
}
```

## Gestion des Erreurs

### Logo Manquant

Si un logo n'existe pas, l'application affiche:
- Pour les équipes: Icône bouclier (fallback)
- Pour les chaînes: Badge avec nom de la chaîne

### Logo Cassé

Code JavaScript gère les erreurs:
```javascript
onerror="this.style.display='none'; this.nextElementSibling.style.display='block';"
```

## Optimisation des Logos

### Compression

Compressez vos logos PNG avec:
- **TinyPNG** (https://tinypng.com)
- **ImageOptim** (https://imageoptim.com)

### Format WebP

Pour de meilleures performances:
```bash
# Convertir PNG en WebP
cwebp input.png -o output.webp
```

Puis dans le code:
```html
<img src="logo.webp" alt="Logo">
```

## Sources de Logos Sportifs

### Sites Utiles

1. **Wikipedia Commons**
   - https://commons.wikimedia.org
   - Logos officiels sous licence libre

2. **Brandslogos.com**
   - https://brandslogos.com/sport/

3. **Logos-World.net**
   - https://logos-world.net/sports-logos/

4. **API Sports Logos**
   - https://www.thesportsdb.com/

### APIs avec Logos

Si vous voulez automatiser davantage:

```python
# The Sports DB API
api_url = "https://www.thesportsdb.com/api/v1/json/1/lookupteam.php?id=133604"

# Football Data API
api_url = "https://api.football-data.org/v4/teams/86"
```

## Checklist de Validation

Avant de publier:

- [ ] Tous les logos sont en PNG ou WebP
- [ ] Les logos ont un fond transparent
- [ ] Taille: 120x60px minimum
- [ ] Poids: < 50KB par logo
- [ ] Noms de fichiers corrects (bein.png, ssc.png, etc.)
- [ ] Testés dans l'application
- [ ] Aucun logo cassé
- [ ] Attribution/licences vérifiées

## Licence et Droits

⚠️ **Important:**
- Les logos sont propriété de leurs marques respectives
- Utilisez-les uniquement à des fins éducatives/personnelles
- Ne redistribuez pas commercialement
- Respectez les droits d'auteur

## Contributeurs

Vous avez des logos de qualité? Contribuez!

1. Fork le projet
2. Ajoutez vos logos dans `static/logos/`
3. Mettez à jour `channels_mapping.py`
4. Créez une Pull Request

---

**Dernière mise à jour:** 2024-01-15
**Version:** 1.0.0
