@echo off
echo ========================================
echo   Mobaryat - Application de Streaming
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou n'est pas dans le PATH
    echo Téléchargez Python depuis: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python est installé
echo.

REM Vérifier si les dépendances sont installées
echo Vérification des dépendances...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installation des dépendances...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERREUR] Échec de l'installation des dépendances
        pause
        exit /b 1
    )
) else (
    echo [OK] Dépendances installées
)

echo.
echo Création des dossiers nécessaires...
if not exist "cache" mkdir cache
if not exist "templates" mkdir templates
if not exist "static\css" mkdir static\css
if not exist "static\js" mkdir static\js
if not exist "static\logos" mkdir static\logos
if not exist "scrapers" mkdir scrapers

echo [OK] Dossiers créés
echo.
echo ========================================
echo   Démarrage de l'application...
echo ========================================
echo.
echo L'application sera accessible sur:
echo   http://localhost:5000
echo.
echo Appuyez sur Ctrl+C pour arrêter le serveur
echo.

REM Lancer l'application
python app.py

pause
