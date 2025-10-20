@echo off
echo ========================================
echo    LANCEMENT ALTERNATIF - APPLICATION NANA
echo ========================================
echo.

:: Vérifier si Python est installé
echo [1/6] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERREUR: Python n'est pas installé ou pas dans le PATH
    echo Veuillez installer Python depuis https://python.org
    pause
    exit /b 1
)
echo ✅ Python detecte

:: Vérifier si Node.js est installé
echo [2/6] Verification de Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERREUR: Node.js n'est pas installé ou pas dans le PATH
    echo Veuillez installer Node.js depuis https://nodejs.org
    pause
    exit /b 1
)
echo ✅ Node.js detecte

:: Créer et activer l'environnement virtuel Python
echo [3/6] Configuration de l'environnement Python...
if not exist "venv" (
    echo Creation de l'environnement virtuel...
    python -m venv venv
)
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

:: Installer les dépendances Python avec des versions pré-compilées
echo [4/6] Installation des dependances Python (versions pre-compilees)...
cd backend

:: Mettre à jour pip d'abord
python -m pip install --upgrade pip

:: Installer les packages un par un pour éviter les conflits
echo Installation de Django...
pip install Django==5.0.2

echo Installation de Django REST Framework...
pip install djangorestframework==3.15.0

echo Installation de django-cors-headers...
pip install django-cors-headers==4.3.1

echo Installation de channels...
pip install channels==4.0.0

echo Installation de channels-redis...
pip install channels-redis==4.1.0

echo Installation de numpy (version compatible)...
pip install numpy==1.26.4

echo Installation de pandas (version compatible)...
pip install pandas==2.2.0

echo Installation de scipy...
pip install scipy==1.12.0

echo Installation de matplotlib...
pip install matplotlib==3.8.3

echo Installation de seaborn...
pip install seaborn==0.13.2

echo Installation de scikit-learn...
pip install scikit-learn==1.4.0

echo Installation des autres packages...
pip install python-decouple==3.8
pip install redis==5.0.1
pip install celery==5.3.4
pip install daphne==4.0.0

echo ✅ Dependances Python installees

:: Démarrer Django en arrière-plan
echo [5/6] Demarrage du serveur Django...
start "Django Backend" cmd /k "cd /d %CD% && python manage.py runserver"
echo ✅ Serveur Django demarre (port 8000)

:: Retourner au dossier racine et installer les dépendances Node.js
cd ..
cd frontend
echo [6/6] Installation des dependances Node.js...
npm install
if errorlevel 1 (
    echo ❌ ERREUR: Impossible d'installer les dependances Node.js
    pause
    exit /b 1
)
echo ✅ Dependances Node.js installees

:: Démarrer React
echo Demarrage de l'application React...
start "React Frontend" cmd /k "cd /d %CD% && npm start"
echo ✅ Application React demarree (port 3000)

:: Retourner au dossier racine
cd ..

echo.
echo ========================================
echo    🎉 APPLICATION LANCEE AVEC SUCCES !
echo ========================================
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend:  http://localhost:8000
echo.
echo ⏳ Ouverture du navigateur dans 5 secondes...
timeout /t 5 /nobreak >nul

:: Ouvrir le navigateur
start http://localhost:3000

echo.
echo ✅ Navigateur ouvert automatiquement !
echo.
echo 💡 Pour arreter l'application:
echo    1. Fermez les fenetres de terminal
echo    2. Ou appuyez sur Ctrl+C dans chaque terminal
echo.
echo 🚀 Votre application est maintenant accessible !
pause



