#!/usr/bin/env python3
"""
Script de test pour vérifier la configuration de l'Application Nana
Exécutez ce script pour vérifier que tout est correctement configuré
"""

import sys
import os
import subprocess
from pathlib import Path

def test_python():
    """Teste l'installation de Python"""
    print("🐍 Test de Python...")
    try:
        version = subprocess.check_output([sys.executable, "--version"], 
                                       text=True, stderr=subprocess.STDOUT)
        print(f"✓ Python détecté: {version.strip()}")
        return True
    except Exception as e:
        print(f"✗ Erreur Python: {e}")
        return False

def test_dependencies():
    """Teste les dépendances Python"""
    print("\n📦 Test des dépendances Python...")
    required_packages = [
        'django', 'djangorestframework', 'pandas', 'numpy', 
        'scipy', 'matplotlib', 'seaborn', 'scikit-learn'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} manquant")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Packages manquants: {', '.join(missing_packages)}")
        print("Exécutez: pip install -r backend/requirements.txt")
        return False
    
    return True

def test_node():
    """Teste l'installation de Node.js"""
    print("\n🟢 Test de Node.js...")
    try:
        version = subprocess.check_output(['node', '--version'], 
                                       text=True, stderr=subprocess.STDOUT)
        print(f"✓ Node.js détecté: {version.strip()}")
        return True
    except Exception as e:
        print(f"✗ Erreur Node.js: {e}")
        return False

def test_npm():
    """Teste l'installation de npm"""
    print("\n📦 Test de npm...")
    try:
        version = subprocess.check_output(['npm', '--version'], 
                                       text=True, stderr=subprocess.STDOUT)
        print(f"✓ npm détecté: {version.strip()}")
        return True
    except Exception as e:
        print(f"✗ Erreur npm: {e}")
        return False

def test_directories():
    """Teste la structure des répertoires"""
    print("\n📁 Test de la structure des répertoires...")
    base_dir = Path(__file__).parent
    required_dirs = [
        base_dir / "backend",
        base_dir / "frontend",
        base_dir / "backend" / "users",
        base_dir / "backend" / "simulations",
        base_dir / "frontend" / "src",
    ]
    
    missing_dirs = []
    for directory in required_dirs:
        if directory.exists():
            print(f"✓ {directory.name}")
        else:
            print(f"✗ {directory.name} manquant")
            missing_dirs.append(directory.name)
    
    if missing_dirs:
        print(f"\n⚠️  Répertoires manquants: {', '.join(missing_dirs)}")
        return False
    
    return True

def test_files():
    """Teste l'existence des fichiers importants"""
    print("\n📄 Test des fichiers importants...")
    base_dir = Path(__file__).parent
    required_files = [
        base_dir / "backend" / "requirements.txt",
        base_dir / "backend" / "manage.py",
        base_dir / "frontend" / "package.json",
        base_dir / "README.md",
    ]
    
    missing_files = []
    for file_path in required_files:
        if file_path.exists():
            print(f"✓ {file_path.name}")
        else:
            print(f"✗ {file_path.name} manquant")
            missing_files.append(file_path.name)
    
    if missing_files:
        print(f"\n⚠️  Fichiers manquants: {', '.join(missing_files)}")
        return False
    
    return True

def test_django_setup():
    """Teste la configuration Django"""
    print("\n⚙️  Test de la configuration Django...")
    try:
        os.chdir("backend")
        
        # Vérifier si la base de données existe
        if Path("db.sqlite3").exists():
            print("✓ Base de données SQLite")
        else:
            print("⚠️  Base de données SQLite manquante (sera créée au premier démarrage)")
        
        # Vérifier les migrations
        try:
            result = subprocess.run([sys.executable, "manage.py", "showmigrations", "--list"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✓ Migrations Django")
            else:
                print("⚠️  Erreur lors de la vérification des migrations")
        except subprocess.TimeoutExpired:
            print("⚠️  Timeout lors de la vérification des migrations")
        
        os.chdir("..")
        return True
    except Exception as e:
        print(f"✗ Erreur Django: {e}")
        os.chdir("..")
        return False

def test_react_setup():
    """Teste la configuration React"""
    print("\n⚛️  Test de la configuration React...")
    try:
        os.chdir("frontend")
        
        # Vérifier package.json
        if Path("package.json").exists():
            print("✓ package.json")
        
        # Vérifier node_modules
        if Path("node_modules").exists():
            print("✓ node_modules")
        else:
            print("⚠️  node_modules manquant (exécutez: npm install)")
        
        os.chdir("..")
        return True
    except Exception as e:
        print(f"✗ Erreur React: {e}")
        os.chdir("..")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 TEST DE CONFIGURATION - APPLICATION NANA")
    print("=" * 50)
    
    tests = [
        ("Python", test_python),
        ("Dépendances Python", test_dependencies),
        ("Node.js", test_node),
        ("npm", test_npm),
        ("Structure des répertoires", test_directories),
        ("Fichiers importants", test_files),
        ("Configuration Django", test_django_setup),
        ("Configuration React", test_react_setup),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Erreur lors du test {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé des tests
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:.<30} {status}")
    
    print(f"\nRésultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 Tous les tests sont réussis! L'application est prête.")
        print("Vous pouvez maintenant exécuter start.bat (Windows) ou start.sh (Linux/Mac)")
    else:
        print(f"\n⚠️  {total - passed} test(s) ont échoué.")
        print("Veuillez corriger les problèmes avant de continuer.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)





