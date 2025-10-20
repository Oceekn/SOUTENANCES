@echo off
chcp 65001 >nul
title Application de Gestion des Risques de Crédit

echo.
echo ============================================================
echo    APPLICATION DE GESTION DES RISQUES DE CREDIT
echo ============================================================
echo.

echo Vérification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Erreur: Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python depuis https://python.org
    pause
    exit /b 1
)

echo Vérification de Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Erreur: Node.js n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Node.js depuis https://nodejs.org
    pause
    exit /b 1
)

echo Vérification de npm...
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Erreur: npm n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer npm avec Node.js
    pause
    exit /b 1
)

echo.
echo ✅ Toutes les dépendances sont installées
echo.
echo 🚀 Lancement de l'application...
echo.

python start_app.py

echo.
echo Appuyez sur une touche pour fermer...
pause >nul





