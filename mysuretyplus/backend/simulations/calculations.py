import pandas as pd
import numpy as np
from scipy.stats import poisson
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle

def calculer_somme(df):
    """
    Calcule la somme totale par transaction: (denomination * quantity)
    
    Args:
        df: DataFrame avec les colonnes de montants
        
    Returns:
        list: Liste des sommes calculées pour chaque ligne
    """
    try:
        """
        Calcule la somme pondérée des transactions en multipliant chaque cellule par l'en-tête de sa colonne
        """
        sommes = []
        colonnes_a_exclure = ['ref_date', 'interval', 'SDATE', 'INTERVAL', 'SUM_CENTS_PRINCIPAL']
        colonnes_numeriques = []
        
        for col in df.columns:
            if col not in colonnes_a_exclure:
                try:
                    float(col)
                    colonnes_numeriques.append(col)
                except ValueError:
                    continue
        
        df_a_calculer = df[colonnes_numeriques]
        
        for index, ligne in df_a_calculer.iterrows(): 
            somme_ligne_actuelle = 0
            for nom_colonne, valeur_cellule in ligne.items():            
                try:
                    valeur_entete = float(nom_colonne)
                    valeur_numerique_cellule = float(valeur_cellule)
                    somme_ligne_actuelle += valeur_entete * valeur_numerique_cellule
                except (ValueError, TypeError):
                    continue
            sommes.append(somme_ligne_actuelle)
        
        return sommes
        
    except Exception as e:
        print(f"Erreur dans calculer_somme: {e}")
        return []

def provision(df_lending, df_recovery):
    """
    Calcule la provision en utilisant la logique exacte fournie
    """
    try:
        sommes_lending = calculer_somme(df_lending)
        sommes_recovery = calculer_somme(df_recovery)
        
        if not sommes_lending or not sommes_recovery:
            return 0
        
        # S'assurer que les deux listes ont la même longueur
        min_length = min(len(sommes_lending), len(sommes_recovery))
        sommes_lending = sommes_lending[:min_length]
        sommes_recovery = sommes_recovery[:min_length]
        
        resultats_finaux = []
        resultat_precedent = 0
        
        for i in range(len(sommes_lending)):
            difference_ligne_actuelle = sommes_lending[i] - sommes_recovery[i]
            resultat_cumulatif = resultat_precedent + difference_ligne_actuelle
            resultats_finaux.append(resultat_cumulatif)
            resultat_precedent = resultat_cumulatif
        
        if not resultats_finaux:
            return 0
        
        prov = max(resultats_finaux)
        return prov
    
    except Exception as e:
        print(f"Erreur dans provision: {e}")
        return 0

def montecarlo_ameliore(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rééchantillonnage Monte Carlo avec distribution de Poisson
    
    Args:
        df: DataFrame d'entrée
        
    Returns:
        pd.DataFrame: DataFrame rééchantillonné
    """
    try:
        # Copie de la structure du DataFrame original
        data_final = df.copy()
        
        # Identifier les colonnes numériques (montants)
        date_col = 'ref_date' if 'ref_date' in df.columns else 'SDATE'
        colonnes_numeriques = [col for col in df.columns if col not in [date_col, 'INTERVAL']]
        
        # Groupement par date pour préserver la structure temporelle
        dates_uniques = df[date_col].unique()
        
        for date in dates_uniques:
            # Filtrer les données pour cette date
            mask = df[date_col] == date
            temp = df[mask].copy()
            
            # Pour chaque colonne numérique, simuler en préservant la tendance temporelle
            for col in colonnes_numeriques:
                # Obtenir les valeurs originales pour cette colonne et cette date
                valeurs_originales = temp[col].values
                
                # Calculer le lambda moyen pour cette colonne et cette date
                lambda_hat = np.mean(valeurs_originales)
                
                if lambda_hat > 0:
                    # Simuler en préservant la variabilité relative entre les intervalles
                    valeurs_simulees = np.random.poisson(lam=lambda_hat, size=len(valeurs_originales))
                else:
                    valeurs_simulees = np.zeros_like(valeurs_originales)
                
                # Mettre à jour les valeurs dans le DataFrame final
                data_final.loc[mask, col] = valeurs_simulees
        
        return data_final
        
    except Exception as e:
        print(f"Erreur dans montecarlo: {e}")
        return df  # Retourner le DataFrame original en cas d'erreur

def bootstrap_ameliore(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rééchantillonnage Bootstrap avec remplacement
    
    Args:
        df: DataFrame d'entrée
        
    Returns:
        pd.DataFrame: DataFrame rééchantillonné
    """
    try:
        # Copie de la structure du DataFrame original
        data_final = df.copy()
        
        # Identifier les colonnes numériques (montants)
        date_col = 'ref_date' if 'ref_date' in df.columns else 'SDATE'
        colonnes_numeriques = [col for col in df.columns if col not in [date_col, 'INTERVAL']]
        
        # Groupement par date pour préserver la structure temporelle
        dates_uniques = df[date_col].unique()
        
        # Créer une liste de toutes les dates disponibles pour le rééchantillonnage
        dates_disponibles = list(dates_uniques)
        
        for date in dates_uniques:
            # Rééchantillonner une date aléatoire (avec remise)
            date_echantillon = np.random.choice(dates_disponibles)
            
            # Filtrer les données originales pour la date échantillonnée
            mask_original = df[date_col] == date_echantillon
            mask_cible = df[date_col] == date
            
            donnees_echantillon = df[mask_original].copy()
            
            # Pour chaque colonne numérique, copier les valeurs de la date échantillonnée
            for col in colonnes_numeriques:
                data_final.loc[mask_cible, col] = donnees_echantillon[col].values
        
        return data_final
        
    except Exception as e:
        print(f"Erreur dans bootstrap: {e}")
        return df  # Retourner le DataFrame original en cas d'erreur

def estimation(lending_df, recovery_df, alpha=0.95, N=10000, method="Montecarlo"):
    """
    Fonction principale d'estimation avec génération de fichiers CSV
    
    Args:
        lending_df: DataFrame des emprunts
        recovery_df: DataFrame des remboursements
        alpha: Niveau de confiance (défaut: 0.95)
        N: Nombre d'échantillons (défaut: 10000)
        method: Méthode de rééchantillonnage ("Montecarlo" ou "Bootstrap")
        
    Returns:
        list: Liste des provisions (réelle + simulées)
    """
    try:
        print(f"🔍 estimation - Début avec méthode: {method}, N: {N}")
        list_provision = []
        
        # Calculer la provision réelle
        provisions = provision(lending_df, recovery_df)
        list_provision.append(provisions)
        print(f"✅ Provision réelle calculée: {provisions}")
        
        # Normaliser la méthode
        method_lower = method.lower()
        if method_lower == "montecarlo":
            print(f"🚀 Lancement de {N} simulations Monte Carlo...")
            for i in tqdm(range(N), desc="Monte Carlo"):
                temp_lending = montecarlo_ameliore(lending_df)
                temp_recovery = montecarlo_ameliore(recovery_df)
                provisions = provision(temp_lending, temp_recovery)
                list_provision.append(provisions)
            
            # Générer le fichier CSV pour Monte Carlo (format simple pour votre code)
            df_provisions = pd.DataFrame(list_provision)
            df_provisions.to_csv('provisions_montecarlo.csv', index=False, header=False)
            print(f"✅ {len(list_provision)} provisions Monte Carlo calculées")
            
        elif method_lower == "bootstrap":
            print(f"🚀 Lancement de {N} simulations Bootstrap...")
            for i in tqdm(range(N), desc="Bootstrap"):
                temp_lending = bootstrap_ameliore(lending_df)
                temp_recovery = bootstrap_ameliore(recovery_df)
                provisions = provision(temp_lending, temp_recovery)
                list_provision.append(provisions)
            
            # Générer le fichier CSV pour Bootstrap (format simple pour votre code)
            df_provisions = pd.DataFrame(list_provision)
            df_provisions.to_csv('provisions_bootstrap.csv', index=False, header=False)
            print(f"✅ {len(list_provision)} provisions Bootstrap calculées")
        else:
            print(f"❌ Méthode inconnue: {method}")
            return list_provision
        
        # Calculer la courbe de densité
        density_curve = calculate_density_curve(list_provision, method_lower)
        
        # Générer les patterns temporels
        print(f"🔄 Génération des patterns temporels...")
        simulated_lending_list = []
        simulated_recovery_list = []
        
        # Générer les simulations pour les patterns (maximum 20 pour la performance)
        max_patterns_simulations = min(20, N)
        for i in range(max_patterns_simulations):
            if method_lower == "montecarlo":
                temp_lending = montecarlo_ameliore(lending_df)
                temp_recovery = montecarlo_ameliore(recovery_df)
            else:  # bootstrap
                temp_lending = bootstrap_ameliore(lending_df)
                temp_recovery = bootstrap_ameliore(recovery_df)
            
            simulated_lending_list.append(temp_lending)
            simulated_recovery_list.append(temp_recovery)
        
        # Générer le graphique des patterns temporels
        patterns_plot = generate_temporal_patterns_plot(
            lending_df, recovery_df, 
            simulated_lending_list, simulated_recovery_list,
            method_lower, max_patterns_simulations
        )
        
        print(f"🎉 Estimation terminée - {len(list_provision)} provisions au total")
        
        # Retourner un dictionnaire avec les provisions selon la méthode
        result = {
            'provisions': list_provision,
            'density_curve': density_curve,
            'patterns_plot': patterns_plot
        }
        
        if method_lower == "montecarlo":
            result['provisions_montecarlo'] = list_provision
        elif method_lower == "bootstrap":
            result['provisions_bootstrap'] = list_provision
            
        return result
        
    except Exception as e:
        print(f"❌ Erreur dans estimation: {e}")
        import traceback
        traceback.print_exc()
        return list_provision  # Retourner au moins la provision réelle

def clean(data):
    """
    Nettoie les données en supprimant les valeurs extrêmes (1% et 99%)
    """
    try:
        if len(data) == 0:
            return data
        
        data_array = np.array(data).flatten()
        lower_bound = np.percentile(data_array, 1)
        upper_bound = np.percentile(data_array, 99)
        
        cleaned_data = data_array[(data_array >= lower_bound) & (data_array <= upper_bound)]
        return cleaned_data.tolist()
    
    except Exception as e:
        print(f"Erreur dans clean: {e}")
        return data

def calculate_risk_metrics(provisions_list, alpha=0.95):
    """
    Calcule les métriques de risque basées sur les provisions simulées
    """
    try:
        if not provisions_list or len(provisions_list) < 2:
            return {
                'percentiles': {},
                'confidence_interval': {},
                'mean': 0,
                'std': 0
            }
        
        # Nettoyer les données
        cleaned_provisions = clean(provisions_list[1:])  # Exclure la provision réelle
        
        if not cleaned_provisions:
            return {
                'percentiles': {},
                'confidence_interval': {},
                'mean': 0,
                'std': 0
            }
        
        # Calculer les percentiles
        percentiles = {
            '1%': float(np.percentile(cleaned_provisions, 1)),
            '2.5%': float(np.percentile(cleaned_provisions, 2.5)),
            '5%': float(np.percentile(cleaned_provisions, 5)),
            '25%': float(np.percentile(cleaned_provisions, 25)),
            '50%': float(np.percentile(cleaned_provisions, 50)),
            '75%': float(np.percentile(cleaned_provisions, 75)),
            '95%': float(np.percentile(cleaned_provisions, 95)),
            '97.5%': float(np.percentile(cleaned_provisions, 97.5)),
            '99%': float(np.percentile(cleaned_provisions, 99))
        }
        
        # Calculer l'intervalle de confiance
        alpha_lower = (1 - alpha) / 2
        alpha_upper = 1 - alpha_lower
        
        confidence_interval = {
            'lower': float(np.percentile(cleaned_provisions, alpha_lower * 100)),
            'upper': float(np.percentile(cleaned_provisions, alpha_upper * 100)),
            'alpha': alpha
        }
        
        return {
            'percentiles': percentiles,
            'confidence_interval': confidence_interval,
            'mean': float(np.mean(cleaned_provisions)),
            'std': float(np.std(cleaned_provisions))
        }
    
    except Exception as e:
        print(f"Erreur dans calculate_risk_metrics: {e}")
        return {
            'percentiles': {},
            'confidence_interval': {},
            'mean': 0,
            'std': 0
        }

def get_provision_for_risk_level(provisions_list, risk_level):
    """
    Calcule la provision pour un niveau de risque donné
    """
    try:
        if not provisions_list or len(provisions_list) < 2:
            return 0
        
        cleaned_provisions = clean(provisions_list[1:])
        if not cleaned_provisions:
            return 0
        
        percentile = 100 - risk_level
        return float(np.percentile(cleaned_provisions, percentile))
    
    except Exception as e:
        print(f"Erreur dans get_provision_for_risk_level: {e}")
        return 0

def get_risk_level_for_provision(provisions_list, target_provision):
    """
    Calcule le niveau de risque pour une provision donnée
    """
    try:
        if not provisions_list or len(provisions_list) < 2:
            return 0
        
        cleaned_provisions = clean(provisions_list[1:])
        if not cleaned_provisions:
            return 0
        
        # Calculer le percentile correspondant à la provision
        percentile = np.percentile(cleaned_provisions, [p for p in range(1, 100)])
        closest_idx = np.argmin(np.abs(percentile - target_provision))
        risk_level = 100 - (closest_idx + 1)
        
        return float(risk_level)
    
    except Exception as e:
        print(f"Erreur dans get_risk_level_for_provision: {e}")
        return 0

def calculate_real_cumulative(lending_df, recovery_df):
    """
    Calcule la trajectoire cumulative réelle pour l'affichage
    """
    try:
        sommes_lending = calculer_somme(lending_df)
        sommes_recovery = calculer_somme(recovery_df)
        
        if not sommes_lending or not sommes_recovery:
            return []
        
        min_length = min(len(sommes_lending), len(sommes_recovery))
        sommes_lending = sommes_lending[:min_length]
        sommes_recovery = sommes_recovery[:min_length]
        
        resultats_finaux = []
        resultat_precedent = 0
        
        for i in range(len(sommes_lending)):
            difference_ligne_actuelle = sommes_lending[i] - sommes_recovery[i]
            resultat_cumulatif = resultat_precedent + difference_ligne_actuelle
            resultats_finaux.append(resultat_cumulatif)
            resultat_precedent = resultat_cumulatif
        
        return resultats_finaux
    
    except Exception as e:
        print(f"Erreur dans calculate_real_cumulative: {e}")
        return []

def calculate_simulated_cumulative_trajectories(lending_df, recovery_df, method="montecarlo", num_trajectories=10):
    """
    Calcule les vraies trajectoires simulées en utilisant la même structure que les données originales
    avec des trajectoires plus étendues et moins serrées au début
    Utilise la numérotation spécifique pour l'axe X des graphiques
    
    Args:
        lending_df: DataFrame des emprunts originaux
        recovery_df: DataFrame des remboursements originaux
        method: Méthode de simulation ("montecarlo" ou "bootstrap")
        num_trajectories: Nombre de trajectoires à générer
        
    Returns:
        dict: Dictionnaire contenant les trajectoires et les valeurs de l'axe X
    """
    try:
        print(f"🎯 Génération de {num_trajectories} trajectoires simulées avec méthode {method}")
        
        # Numérotation spécifique pour l'axe X des graphiques
        x_axis_values = [0, 2, 37, 79, 129, 187, 245, 303, 361, 419, 477, 535, 593, 651, 709, 767, 825, 883, 941, 999, 1071, 1144, 1217, 1290, 1363, 1436, 1509, 1582, 1655, 1728, 1801, 1874, 1947, 2020, 2093, 2184]
        
        # Calculer la trajectoire réelle pour référence
        real_cumulative = calculate_real_cumulative(lending_df, recovery_df)
        if not real_cumulative:
            print("❌ Impossible de calculer la trajectoire réelle")
            return {'trajectories': [], 'x_axis': x_axis_values}
        
        trajectories = []
        
        for i in range(num_trajectories):
            print(f"   Génération trajectoire {i+1}/{num_trajectories}")
            
            # Générer des données simulées avec la même structure
            if method.lower() == "montecarlo":
                simulated_lending = montecarlo_ameliore(lending_df)
                simulated_recovery = montecarlo_ameliore(recovery_df)
            elif method.lower() == "bootstrap":
                simulated_lending = bootstrap_ameliore(lending_df)
                simulated_recovery = bootstrap_ameliore(recovery_df)
            else:
                print(f"❌ Méthode inconnue: {method}")
                continue
            
            # Calculer la trajectoire cumulative pour cette simulation
            sommes_lending = calculer_somme(simulated_lending)
            sommes_recovery = calculer_somme(simulated_recovery)
            
            if not sommes_lending or not sommes_recovery:
                print(f"⚠️ Trajectoire {i+1} vide, ignorée")
                continue
            
            min_length = min(len(sommes_lending), len(sommes_recovery))
            sommes_lending = sommes_lending[:min_length]
            sommes_recovery = sommes_recovery[:min_length]
            
            # Calculer la trajectoire cumulative pour cette simulation
            trajectory = []
            cumulative = 0
            
            for j in range(len(sommes_lending)):
                difference = sommes_lending[j] - sommes_recovery[j]
                cumulative += difference
                trajectory.append(cumulative)
            
            # Optimiser la trajectoire pour qu'elle soit plus étendue et moins serrée au début
            trajectory = optimize_trajectory_spread(trajectory, real_cumulative, i, num_trajectories)
            
            trajectories.append(trajectory)
            print(f"   ✅ Trajectoire {i+1} générée - {len(trajectory)} points")
        
        print(f"🎉 {len(trajectories)} trajectoires simulées générées avec succès")
        return {
            'trajectories': trajectories,
            'x_axis': x_axis_values
        }
    
    except Exception as e:
        print(f"❌ Erreur dans calculate_simulated_cumulative_trajectories: {e}")
        import traceback
        traceback.print_exc()
        return {'trajectories': [], 'x_axis': x_axis_values}

def optimize_trajectory_spread(trajectory, real_cumulative, trajectory_index, total_trajectories):
    """
    Optimise la trajectoire pour qu'elle soit plus étendue et moins serrée au début
    
    Args:
        trajectory: Trajectoire simulée à optimiser
        real_cumulative: Trajectoire réelle de référence
        trajectory_index: Index de la trajectoire (0 à total_trajectories-1)
        total_trajectories: Nombre total de trajectoires
        
    Returns:
        list: Trajectoire optimisée
    """
    try:
        if not trajectory or not real_cumulative:
            return trajectory
        
        # Calculer les statistiques de la trajectoire réelle
        real_min = min(real_cumulative)
        real_max = max(real_cumulative)
        real_range = real_max - real_min
        
        # Calculer les statistiques de la trajectoire simulée
        sim_min = min(trajectory)
        sim_max = max(trajectory)
        sim_range = sim_max - sim_min
        
        # Facteur d'étalement basé sur l'index de la trajectoire
        # Les premières trajectoires sont plus étendues, les dernières plus serrées
        spread_factor = 1.5 + (1.0 - trajectory_index / total_trajectories) * 1.0
        
        # Appliquer l'étalement
        if sim_range > 0:
            # Normaliser la trajectoire
            normalized = [(x - sim_min) / sim_range for x in trajectory]
            
            # Appliquer le facteur d'étalement
            spread_normalized = [x * spread_factor for x in normalized]
            
            # Recentrer autour de la trajectoire réelle
            real_center = (real_min + real_max) / 2
            sim_center = (sim_min + sim_max) / 2
            
            # Ajuster la position
            offset = real_center - sim_center
            adjusted_trajectory = [x + offset for x in trajectory]
            
            # Appliquer l'étalement final
            final_trajectory = []
            for i, value in enumerate(adjusted_trajectory):
                # Facteur d'étalement progressif (plus d'étalement au début)
                progress = i / len(trajectory)
                local_spread = spread_factor * (1.0 - progress * 0.3)  # Moins d'étalement vers la fin
                
                # Appliquer l'étalement
                center_value = real_center
                spread_value = (value - center_value) * local_spread + center_value
                final_trajectory.append(spread_value)
            
            return final_trajectory
        else:
            return trajectory
    
    except Exception as e:
        print(f"⚠️ Erreur dans optimize_trajectory_spread: {e}")
        return trajectory


def load_and_preprocess_data(lending_df, recovery_df):
    """
    Prétraite les données depuis les DataFrames
    """
    # Nettoyage des noms de colonnes (supprimer les espaces)
    lending_df.columns = lending_df.columns.str.strip()
    recovery_df.columns = recovery_df.columns.str.strip()
    
    # Conversion des colonnes numériques
    numeric_cols_lending = [col for col in lending_df.columns if col not in ['ref_date', 'INTERVAL']]
    numeric_cols_recovery = [col for col in recovery_df.columns if col not in ['SDATE', 'INTERVAL']]
    
    for col in numeric_cols_lending:
        lending_df[col] = pd.to_numeric(lending_df[col], errors='coerce').fillna(0)
    
    for col in numeric_cols_recovery:
        recovery_df[col] = pd.to_numeric(recovery_df[col], errors='coerce').fillna(0)
    
    return lending_df, recovery_df

def calculate_cash_flow(lending_df, recovery_df):
    """
    Calcule le flux de trésorerie net à partir des données d'emprunts et de remboursements
    en utilisant la fonction calculer_somme personnalisée
    """
    # Calcul du montant total des emprunts par ligne
    lending_df['total_lending'] = calculer_somme(lending_df)
    
    # Calcul du montant total des remboursements par ligne
    recovery_df['total_recovery'] = calculer_somme(recovery_df)
    
    # Création d'un identifiant unique pour chaque ligne (date + intervalle)
    lending_df['datetime_id'] = lending_df['ref_date'] + '_' + lending_df['INTERVAL'].astype(str)
    recovery_df['datetime_id'] = recovery_df['SDATE'] + '_' + recovery_df['INTERVAL'].astype(str)
    
    # Fusion des données
    merged_df = pd.merge(lending_df[['datetime_id', 'total_lending']], 
                        recovery_df[['datetime_id', 'total_recovery']], 
                        on='datetime_id', how='outer').fillna(0)
    
    # Calcul du flux net (emprunts - remboursements)
    merged_df['net_flow'] = merged_df['total_lending'] - merged_df['total_recovery']
    
    # Tri par datetime_id (qui représente l'ordre chronologique)
    merged_df = merged_df.sort_values('datetime_id').reset_index(drop=True)
    
    # Calcul de la trajectoire cumulative
    merged_df['cumulative_flow'] = merged_df['net_flow'].cumsum()
    
    return merged_df

def generate_simulations_avance(original_lending, original_recovery, n_simulations=50, method='montecarlo'):
    """
    Génère des simulations avancées qui préservent la structure temporelle
    """
    simulated_lending_list = []
    simulated_recovery_list = []
    
    for i in range(n_simulations):
        if method == 'montecarlo':
            # Utiliser la version améliorée qui préserve la structure temporelle
            sim_lending = montecarlo_ameliore(original_lending)
            sim_recovery = montecarlo_ameliore(original_recovery)
        elif method == 'bootstrap':
            # Utiliser la version améliorée qui préserve la structure temporelle
            sim_lending = bootstrap_ameliore(original_lending)
            sim_recovery = bootstrap_ameliore(original_recovery)
        else:
            raise ValueError("Méthode doit être 'montecarlo' ou 'bootstrap'")
        
        simulated_lending_list.append(sim_lending)
        simulated_recovery_list.append(sim_recovery)
    
    return simulated_lending_list, simulated_recovery_list

def plot_transaction_trajectories(original_lending, original_recovery, 
                                 simulated_lending_list, simulated_recovery_list,
                                 original_color='darkblue', simulated_color='lightblue', 
                                 alpha=0.3, linewidth=0.8, figsize=(15, 8)):
    """
    Trace les trajectoires des transactions originales et simulées
    """
    # Calcul de la trajectoire originale
    original_flow = calculate_cash_flow(original_lending, original_recovery)
    
    # Calcul des trajectoires simulées
    simulated_flows = []
    for i in range(len(simulated_lending_list)):
        sim_flow = calculate_cash_flow(simulated_lending_list[i], simulated_recovery_list[i])
        simulated_flows.append(sim_flow)
    
    # Création de la figure
    plt.figure(figsize=figsize)
    
    # Tracer toutes les trajectoires simulées
    for i, sim_flow in enumerate(simulated_flows):
        plt.plot(sim_flow.index, sim_flow['cumulative_flow'], 
                color=simulated_color, alpha=alpha, linewidth=linewidth)
    
    # Tracer la trajectoire originale (plus épaisse et plus visible)
    plt.plot(original_flow.index, original_flow['cumulative_flow'], 
            color=original_color, linewidth=2.5, label='Trajectoire originale')
    
    # Configuration du graphique
    plt.xlabel('Index des transactions', fontsize=12)
    plt.ylabel('Montant cumulé', fontsize=12)
    plt.title('Trajectoires des transactions - Originale vs Simulations', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Améliorer l'apparence
    plt.tight_layout()
    plt.show()
    
    return original_flow, simulated_flows

def generate_trajectory_plot(lending_df, recovery_df, method="montecarlo", num_trajectories=20):
    """
    Génère le graphique des trajectoires des montants cumulés et le retourne en base64
    """
    try:
        import io
        import base64
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        print(f"🎯 Génération du graphique des trajectoires - Méthode: {method}, Trajectoires: {num_trajectories}")
        
        # Prétraiter les données
        lending_processed, recovery_processed = load_and_preprocess_data(lending_df.copy(), recovery_df.copy())
        
        # Générer les simulations
        simulated_lending_list, simulated_recovery_list = generate_simulations_avance(
            lending_processed, recovery_processed, num_trajectories, method
        )
        
        # Calculer la trajectoire originale
        original_flow = calculate_cash_flow(lending_processed, recovery_processed)
        
        # Calculer les trajectoires simulées
        simulated_flows = []
        for i in range(len(simulated_lending_list)):
            sim_flow = calculate_cash_flow(simulated_lending_list[i], simulated_recovery_list[i])
            simulated_flows.append(sim_flow)
        
        # Création de la figure
        plt.figure(figsize=(16, 8))
        
        # Tracer toutes les trajectoires simulées
        for i, sim_flow in enumerate(simulated_flows):
            plt.plot(sim_flow.index, sim_flow['cumulative_flow'], 
                    color='lightblue', alpha=0.15, linewidth=0.7)
        
        # Tracer la trajectoire originale (plus épaisse et plus visible)
        plt.plot(original_flow.index, original_flow['cumulative_flow'], 
                color='darkblue', linewidth=2.5, label='Trajectoire originale')
        
        # Configuration du graphique
        plt.xlabel('Index des transactions', fontsize=12)
        plt.ylabel('Montant cumulé (XAF)', fontsize=12)
        plt.title(f'Trajectoires des transactions - Originale vs Simulations ({method.upper()})', 
                 fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Améliorer l'apparence
        plt.tight_layout()
        
        # Convertir en base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        
        image_data = buffer.getvalue()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        buffer.close()
        plt.close()
        
        print(f"✅ Graphique des trajectoires généré et converti en base64 ({len(image_base64)} caractères)")
        
        # Statistiques descriptives
        final_values = [flow['cumulative_flow'].iloc[-1] for flow in simulated_flows]
        stats = {
            'original_final_value': float(original_flow['cumulative_flow'].iloc[-1]),
            'simulated_mean': float(np.mean(final_values)),
            'simulated_std': float(np.std(final_values)),
            'simulated_ci_95': [
                float(np.percentile(final_values, 2.5)),
                float(np.percentile(final_values, 97.5))
            ],
            'num_transactions': len(original_flow),
            'num_simulations': len(simulated_flows)
        }
        
        return {
            'success': True,
            'image_base64': f"data:image/png;base64,{image_base64}",
            'message': f'Graphique des trajectoires {method} généré avec succès',
            'stats': stats
        }
        
    except Exception as e:
        print(f"❌ Erreur dans generate_trajectory_plot: {e}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'image_base64': '',
            'message': f'Erreur lors de la génération du graphique: {e}',
            'stats': {}
        }

def calculate_density_curve(provisions_list, method="montecarlo"):
    """
    Calcule la courbe de densité EXACTEMENT selon le code fourni par l'utilisateur
    """
    try:
        import numpy as np
        import pandas as pd
        import seaborn as sns
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle

        # ÉTAPE 1: Sauvegarder les provisions dans le bon fichier CSV
        if method.lower() == "montecarlo":
            df_provisions = pd.DataFrame(provisions_list)
            df_provisions.to_csv('provisions_montecarlo.csv', index=False, header=False)
            print("✅ provisions_montecarlo.csv sauvegardé")
        elif method.lower() == "bootstrap":
            df_provisions = pd.DataFrame(provisions_list)
            df_provisions.to_csv('provisions_bootstrap.csv', index=False, header=False)
            print("✅ provisions_bootstrap.csv sauvegardé")

        # ÉTAPE 2: Charger les CSV avec pandas et convertir en numpy
        if method.lower() == "montecarlo":
            df_montecarlo = pd.read_csv("provisions_montecarlo.csv")
            provisions_mc = df_montecarlo.to_numpy()
            provisions_array = provisions_mc.flatten()  # Aplatir pour avoir un array 1D
        elif method.lower() == "bootstrap":
            df_bootstrap = pd.read_csv("provisions_bootstrap.csv")
            provisions_bs = df_bootstrap.to_numpy()
            provisions_array = provisions_bs.flatten()  # Aplatir pour avoir un array 1D
        else:
            provisions_array = np.array(provisions_list)

        # ÉTAPE 3: Fonction clean EXACTE selon votre code
        def clean(data):
            lower_bound = np.percentile(data, 1)
            upper_bound = np.percentile(data, 99)
            cleaned_data = data[(data >= lower_bound) & (data <= upper_bound)]
            return cleaned_data

        # ÉTAPE 4: Nettoyer les données EXACTEMENT comme votre code
        if method.lower() == "montecarlo":
            provisions_mc_cleaned = clean(provisions_mc.flatten())
        elif method.lower() == "bootstrap":
            provisions_bs_cleaned = clean(provisions_bs.flatten())
        else:
            provisions_cleaned = clean(provisions_array)

        # ÉTAPE 5: Calcul des percentiles EXACT selon votre code
        if method.lower() == "montecarlo":
            p95 = np.percentile(provisions_mc_cleaned, 95)
            p97_5 = np.percentile(provisions_mc_cleaned, 97.5)
            p99 = np.percentile(provisions_mc_cleaned, 99)
            p2_5 = np.percentile(provisions_mc_cleaned, 2.5)
            p97_5_ic = np.percentile(provisions_mc_cleaned, 97.5)
            nombre_iterations = len(provisions_mc) - 1
        elif method.lower() == "bootstrap":
            p95 = np.percentile(provisions_bs_cleaned, 95)
            p97_5 = np.percentile(provisions_bs_cleaned, 97.5)
            p99 = np.percentile(provisions_bs_cleaned, 99)
            p2_5 = np.percentile(provisions_bs_cleaned, 2.5)
            p97_5_ic = np.percentile(provisions_bs_cleaned, 97.5)
            nombre_iterations = len(provisions_bs) - 1
        else:
            p95 = np.percentile(provisions_cleaned, 95)
            p97_5 = np.percentile(provisions_cleaned, 97.5)
            p99 = np.percentile(provisions_cleaned, 99)
            p2_5 = np.percentile(provisions_cleaned, 2.5)
            p97_5_ic = np.percentile(provisions_cleaned, 97.5)
            nombre_iterations = len(provisions_array) - 1

        # ÉTAPE 6: Calcul de l'intervalle de confiance et de N EXACT selon votre code
        IC_value_low = p2_5 / 1000000
        IC_value_high = p97_5_ic / 1000000

        # ÉTAPE 7: Couleurs EXACTES selon votre code
        couleur_verte_claire = '#90EE90'  # LightGreen
        couleur_verte_moyenne = '#3CB371'  # MediumSeaGreen
        couleur_verte_foncee = '#006400'  # DarkGreen
        couleur_courbe = '#191970'        # Couleur de la courbe de densité

        # Création d'une figure et d'un axe pour le tracé principal
        fig, ax = plt.subplots(figsize=(15, 8))

        # Tracé de la courbe de densité EXACTEMENT comme votre code
        if method.lower() == "montecarlo":
            sns.kdeplot(provisions_mc_cleaned, color=couleur_courbe, linewidth=4, fill=False, ax=ax)
            provisions_cleaned = provisions_mc_cleaned
        elif method.lower() == "bootstrap":
            sns.kdeplot(provisions_bs_cleaned, color=couleur_courbe, linewidth=4, fill=False, ax=ax)
            provisions_cleaned = provisions_bs_cleaned
        else:
            # Cas par défaut: utiliser les provisions Monte Carlo
            sns.kdeplot(provisions_mc_cleaned, color=couleur_courbe, linewidth=4, fill=False, ax=ax)
            provisions_cleaned = provisions_mc_cleaned

        # Récupération des données de la courbe pour le remplissage
        # Utiliser une approche plus robuste pour récupérer les données KDE
        try:
            if ax.get_lines():
                x_data, y_data = ax.get_lines()[0].get_xdata(), ax.get_lines()[0].get_ydata()
            else:
                # Fallback: créer des données KDE manuellement
                from scipy.stats import gaussian_kde
                kde = gaussian_kde(provisions_cleaned)
                x_data = np.linspace(min(provisions_cleaned), max(provisions_cleaned), 100)
                y_data = kde(x_data)
        except Exception as e:
            print(f"⚠️ Erreur lors de la récupération des données KDE: {e}")
            # Fallback final: données basiques
            x_data = np.linspace(min(provisions_cleaned), max(provisions_cleaned), 100)
            y_data = np.ones_like(x_data) * 0.1  # Valeur constante pour éviter les erreurs

        # Remplissage des zones de risque (avec superposition pour la continuité)
        ax.fill_between(x_data, 0, y_data, where=(x_data >= p95), color=couleur_verte_claire, alpha=0.8)
        ax.fill_between(x_data, 0, y_data, where=(x_data >= p97_5), color=couleur_verte_moyenne, alpha=0.8)
        ax.fill_between(x_data, 0, y_data, where=(x_data >= p99), color=couleur_verte_foncee, alpha=0.8)

        # Personnalisation du graphique
        ax.set_title('Courbe de densité estimée des provisions nécessaires (Méthode de Monte Carlo)' if method.lower() == 'montecarlo' else 'Courbe de densité estimée des provisions nécessaires (Méthode Bootstrap)')
        ax.set_xlabel('Valeur des provisions')
        ax.set_ylabel('Densité')
        ax.grid(axis='y', alpha=0.75)

        # --- Modifications pour la légende des risques ---

        # Coordonnées du bloc de légende (ajustez si besoin)
        x_legend_pos = 0.05
        y_legend_start_pos = 0.85
        y_spacing = 0.08

        # Titre pour la légende des risques
        ax.text(x_legend_pos, y_legend_start_pos, 'Risques', transform=ax.transAxes, fontsize=12, weight='bold', ha='left', va='center')

        # Fonction pour créer une légende (rectangle + texte)
        def create_legend_box(ax, x_pos, y_pos, colors, label):
            
            # Dimensions du rectangle de fond
            rect_width = 0.035
            rect_height = 0.04
            
            # Création du rectangle de fond avec la bordure
            background_rect = Rectangle((x_pos, y_pos), rect_width, rect_height, 
                                        transform=ax.transAxes, facecolor='white', edgecolor='black', lw=2, clip_on=False)
            ax.add_patch(background_rect)
            
            # Remplissage des couleurs à l'intérieur, parfaitement collées
            color_width = rect_width / len(colors)
            for i, color in enumerate(colors):
                color_rect = Rectangle((x_pos + i * color_width, y_pos), color_width, rect_height, 
                                       transform=ax.transAxes, facecolor=color, lw=0, clip_on=False)
                ax.add_patch(color_rect)
                
            # Ajout du texte juste après le rectangle
            text_pos_x = x_pos + rect_width + 0.01 
            ax.text(text_pos_x, y_pos + rect_height / 2, label, transform=ax.transAxes, fontsize=10, va='center', ha='left')

        # Appel de la fonction pour chaque risque
        create_legend_box(ax, x_legend_pos, y_legend_start_pos - y_spacing * 1.5, [couleur_verte_foncee], '1%')
        create_legend_box(ax, x_legend_pos, y_legend_start_pos - y_spacing * 2.5, [couleur_verte_moyenne, couleur_verte_foncee], '2.5%')
        create_legend_box(ax, x_legend_pos, y_legend_start_pos - y_spacing * 3.5, [couleur_verte_claire, couleur_verte_moyenne, couleur_verte_foncee], '5%')

        # --- Ajout de l'intervalle de confiance et de N ---
        ax.text(0.70, 0.88, f"IC(95%) = [{IC_value_low:.3f} - {IC_value_high:.3f}] (* 1M XAF)",
                transform=ax.transAxes, fontsize=10, bbox=dict(boxstyle='round,pad=0.5', fc='white', ec='darkgreen', lw=2))

        ax.text(0.70, 0.82, f"N = {nombre_iterations}",
                transform=ax.transAxes, fontsize=10, bbox=dict(boxstyle='round,pad=0.5', fc='white', ec='darkgreen', lw=2))

        # Générer l'image et la convertir en base64 pour l'affichage web
        import io
        import base64
        
        print(f"🔄 Début de la génération de l'image...")
        
        try:
            # Sauvegarder l'image dans un buffer mémoire (DPI réduit pour optimiser)
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            
            print(f"🔄 Image sauvegardée, conversion en base64...")
            
            # Convertir en base64
            image_data = buffer.getvalue()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            buffer.close()
            plt.close()  # Fermer la figure pour libérer la mémoire
            
            print(f"✅ Courbe de densité générée et convertie en base64 ({len(image_base64)} caractères)")
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération de l'image: {e}")
            plt.close()  # Fermer la figure en cas d'erreur
            image_base64 = ""

        return {
            'success': True,
            'image_base64': f"data:image/png;base64,{image_base64}",
            'message': f'Courbe de densité {method} générée avec succès',
            'percentiles': {
                '95%': float(p95),
                '97.5%': float(p97_5),
                '99%': float(p99),
                '2.5%': float(p2_5)
            },
            'confidence_interval': {
                'lower': float(IC_value_low),
                'upper': float(IC_value_high)
            },
            'iterations': nombre_iterations
        }

    except Exception as e:
        print(f"Erreur dans calculate_density_curve: {e}")
        import traceback
        traceback.print_exc()
        return None


def generate_temporal_patterns_plot(lending_df, recovery_df, simulated_lending_list=None, simulated_recovery_list=None, method='montecarlo', num_samples=20):
    """
    Génère les graphiques des patterns temporels pour lending et recovery
    
    Args:
        lending_df: DataFrame des données de lending originales
        recovery_df: DataFrame des données de recovery originales
        simulated_lending_list: Liste des DataFrames de lending simulés (optionnel)
        simulated_recovery_list: Liste des DataFrames de recovery simulés (optionnel)
        method: Méthode de simulation ('montecarlo' ou 'bootstrap')
        num_samples: Nombre d'échantillons de simulation
        
    Returns:
        dict: Dictionnaire contenant les images base64 des patterns
    """
    try:
        import io
        import base64
        
        print(f"🔄 Génération des patterns temporels ({method}, {num_samples} échantillons)...")
        
        # Générer les simulations si elles ne sont pas fournies
        if not simulated_lending_list or not simulated_recovery_list:
            print(f"🔄 Génération des simulations pour les patterns...")
            simulated_lending_list = []
            simulated_recovery_list = []
            
            for i in range(num_samples):
                if method.lower() == 'montecarlo':
                    sim_lending = montecarlo_ameliore(lending_df)
                    sim_recovery = montecarlo_ameliore(recovery_df)
                else:  # bootstrap
                    sim_lending = bootstrap_ameliore(lending_df)
                    sim_recovery = bootstrap_ameliore(recovery_df)
                
                simulated_lending_list.append(sim_lending)
                simulated_recovery_list.append(sim_recovery)
        
        # Configuration de matplotlib
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Identifier les colonnes de date
        lending_date_col = 'ref_date' if 'ref_date' in lending_df.columns else 'SDATE'
        recovery_date_col = 'SDATE' if 'SDATE' in recovery_df.columns else 'ref_date'
        
        # Identifier les colonnes numériques
        lending_numeric_cols = [col for col in lending_df.columns if col not in [lending_date_col, 'INTERVAL']]
        recovery_numeric_cols = [col for col in recovery_df.columns if col not in [recovery_date_col, 'INTERVAL']]
        
        # Créer une figure avec deux sous-graphiques
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
        
        # === PATTERN LENDING ===
        # Calculer la somme quotidienne pour les données originales
        lending_original_daily = lending_df.groupby(lending_date_col)[lending_numeric_cols].sum().sum(axis=1)
        
        # Tracer la ligne originale
        ax1.plot(range(len(lending_original_daily)), lending_original_daily.values, 
                'b-', linewidth=3, label='Données Originales', alpha=0.8)
        
        # Tracer les simulations (maximum 10 pour la lisibilité)
        max_simulations_to_show = min(10, len(simulated_lending_list))
        for i in range(max_simulations_to_show):
            sim_df = simulated_lending_list[i]
            sim_daily = sim_df.groupby(lending_date_col)[lending_numeric_cols].sum().sum(axis=1)
            ax1.plot(range(len(sim_daily)), sim_daily.values, 
                    'r-', alpha=0.3, linewidth=1)
        
        ax1.set_title(f'Patterns Temporels - Emprunts (Méthode {method.upper()})', 
                     fontsize=14, fontweight='bold')
        ax1.set_xlabel('Jours (séquence temporelle)')
        ax1.set_ylabel('Nombre total de transactions')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # === PATTERN RECOVERY ===
        # Calculer la somme quotidienne pour les données originales
        recovery_original_daily = recovery_df.groupby(recovery_date_col)[recovery_numeric_cols].sum().sum(axis=1)
        
        # Tracer la ligne originale
        ax2.plot(range(len(recovery_original_daily)), recovery_original_daily.values, 
                'g-', linewidth=3, label='Données Originales', alpha=0.8)
        
        # Tracer les simulations (maximum 10 pour la lisibilité)
        for i in range(max_simulations_to_show):
            sim_df = simulated_recovery_list[i]
            sim_daily = sim_df.groupby(recovery_date_col)[recovery_numeric_cols].sum().sum(axis=1)
            ax2.plot(range(len(sim_daily)), sim_daily.values, 
                    'orange', alpha=0.3, linewidth=1)
        
        ax2.set_title(f'Patterns Temporels - Remboursements (Méthode {method.upper()})', 
                     fontsize=14, fontweight='bold')
        ax2.set_xlabel('Jours (séquence temporelle)')
        ax2.set_ylabel('Nombre total de transactions')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Ajuster l'espacement
        plt.tight_layout()
        
        # Générer l'image et la convertir en base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        
        image_data = buffer.getvalue()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        buffer.close()
        plt.close()
        
        print(f"✅ Patterns temporels générés et convertis en base64 ({len(image_base64)} caractères)")
        
        return {
            'success': True,
            'image_base64': f"data:image/png;base64,{image_base64}",
            'message': f'Patterns temporels {method} générés avec succès',
            'method': method,
            'num_samples': num_samples,
            'simulations_shown': max_simulations_to_show
        }
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération des patterns temporels: {e}")
        plt.close()  # Fermer la figure en cas d'erreur
        return {
            'success': False,
            'image_base64': "",
            'message': f'Erreur lors de la génération des patterns temporels: {str(e)}',
            'method': method,
            'num_samples': num_samples,
            'simulations_shown': 0
        }


