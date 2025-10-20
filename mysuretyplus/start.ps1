# Script de démarrage PowerShell pour l'Application Nana
# Exécuter avec: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    APPLICATION NANA - DEMARRAGE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si Python est installé
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python détecté: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERREUR: Python n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    Write-Host "Veuillez installer Python et l'ajouter au PATH" -ForegroundColor Yellow
    Read-Host "Appuyez sur Entrée pour continuer"
    exit 1
}

# Vérifier si Node.js est installé
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Node.js détecté: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERREUR: Node.js n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    Write-Host "Veuillez installer Node.js et l'ajouter au PATH" -ForegroundColor Yellow
    Read-Host "Appuyez sur Entrée pour continuer"
    exit 1
}

Write-Host ""
Write-Host "Python et Node.js détectés avec succès!" -ForegroundColor Green
Write-Host ""

# Démarrer le backend Django
Write-Host "[1/3] Démarrage du backend Django..." -ForegroundColor Yellow
Set-Location backend

if (-not (Test-Path "venv")) {
    Write-Host "Création de l'environnement virtuel Python..." -ForegroundColor Blue
    python -m venv venv
}

Write-Host "Activation de l'environnement virtuel..." -ForegroundColor Blue
& "venv\Scripts\Activate.ps1"

Write-Host "Installation des dépendances Python..." -ForegroundColor Blue
pip install -r requirements.txt

Write-Host "Démarrage du serveur Django..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; & 'venv\Scripts\Activate.ps1'; python manage.py runserver" -WindowStyle Normal

# Attendre un peu pour que Django démarre
Write-Host "Attente du démarrage de Django..." -ForegroundColor Blue
Start-Sleep -Seconds 5

# Démarrer le frontend React
Write-Host "[2/3] Démarrage du frontend React..." -ForegroundColor Yellow
Set-Location ..\frontend

Write-Host "Installation des dépendances Node.js..." -ForegroundColor Blue
npm install

Write-Host "Démarrage du serveur React..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; npm start" -WindowStyle Normal

# Attendre un peu pour que React démarre
Write-Host "Attente du démarrage de React..." -ForegroundColor Blue
Start-Sleep -Seconds 5

Write-Host "[3/3] Ouverture du navigateur..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Ouvrir le navigateur
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "    APPLICATION DEMARRÉE AVEC SUCCÈS!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend Django: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend React: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Appuyez sur Entrée pour fermer cette fenêtre..." -ForegroundColor Yellow
Read-Host





