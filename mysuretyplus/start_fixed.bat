@echo off
echo ========================================
echo   LANCEMENT DE L'APPLICATION NANA
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python depuis https://python.org
    pause
    exit /b 1
)

REM Vérifier si Node.js est installé
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Node.js depuis https://nodejs.org
    pause
    exit /b 1
)

echo ✅ Python et Node.js détectés
echo.

REM Activer l'environnement virtuel
echo 🔧 Activation de l'environnement virtuel...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Erreur lors de l'activation de l'environnement virtuel
    pause
    exit /b 1
)

echo ✅ Environnement virtuel activé
echo.

REM Installer les dépendances Python si nécessaire
echo 📦 Vérification des dépendances Python...
pip install -r backend\requirements.txt
if errorlevel 1 (
    echo ❌ Erreur lors de l'installation des dépendances Python
    pause
    exit /b 1
)

echo ✅ Dépendances Python installées
echo.

REM Installer les dépendances Node.js si nécessaire
echo 📦 Vérification des dépendances Node.js...
cd frontend
npm install
if errorlevel 1 (
    echo ❌ Erreur lors de l'installation des dépendances Node.js
    pause
    exit /b 1
)
cd ..

echo ✅ Dépendances Node.js installées
echo.

REM Lancer le backend Django
echo 🚀 Lancement du backend Django...
start "Backend Django" cmd /k "cd /d %CD% && venv\Scripts\activate.bat && cd backend && python manage.py runserver"

REM Attendre un peu pour que le backend démarre
timeout /t 3 /nobreak >nul

REM Lancer le frontend React
echo 🚀 Lancement du frontend React...
start "Frontend React" cmd /k "cd /d %CD% && cd frontend && npm start"

echo.
echo ========================================
echo   ✅ APPLICATION LANCÉE AVEC SUCCÈS
echo ========================================
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend:  http://localhost:8000
echo.
echo Appuyez sur une touche pour fermer cette fenêtre...
pause >nul

