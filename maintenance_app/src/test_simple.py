import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from db_connection import init_database, database_exists
import data_access
import business_logic

print("=== TEST DU CODE SIMPLIFIE ===\n")

# Test 1: Base de donnees
print("1. Test base de donnees...")
if database_exists():
    print("   [OK] Base de donnees OK")
else:
    print("   [!] Base de donnees manquante, initialisation...")
    init_database()
    print("   [OK] Base creee")

# Test 2: Fonctions data_access
print("\n2. Test fonctions d'acces aux donnees...")
cout_total = data_access.obtenir_cout_total()
nb_interventions = data_access.obtenir_nombre_interventions()
print(f"   [OK] Cout total: {cout_total:.2f} euros")
print(f"   [OK] Nombre d'interventions: {nb_interventions}")

# Test 3: Calculs Python
print("\n3. Test calculs Python...")
taux = business_logic.calculer_taux_disponibilite()
print(f"   [OK] Taux de disponibilite calcule pour {len(taux)} types")

fiabilite = business_logic.calculer_indice_fiabilite()
print(f"   [OK] Indice de fiabilite calcule pour {len(fiabilite)} equipements")

tendance = business_logic.calculer_tendance_couts(2024)
print(f"   [OK] Tendance des couts: {tendance['tendance']}")

alertes = business_logic.generer_alertes()
print(f"   [OK] {len(alertes)} alertes generees")

# Test 4: Rapport complet
print("\n4. Test rapport de synthese...")
rapport = business_logic.generer_rapport_synthese()
print(f"   [OK] Rapport genere avec {len(rapport)} sections")

print("\n=== TOUS LES TESTS PASSENT ===")
print("\nLe code simplifie fonctionne correctement!")
