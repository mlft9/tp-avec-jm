# Application de Suivi de Maintenance 🔧

Application Python/SQLite pour le suivi et l'analyse de la maintenance d'un parc matériel.

## ⚡ Démarrage Rapide

### Interface Graphique (Recommandée)
```bash
# Sous Windows, double-cliquez sur :
lancer_gui.bat
```

### Interface Ligne de Commande
```bash
# Sous Windows, double-cliquez sur :
lancer_cli.bat
```

## 📊 Aperçu du Projet

Cette application permet de gérer et analyser la maintenance de 10 équipements (ordinateurs, machines, équipements techniques) avec 29 interventions réalisées par 5 techniciens en 2024.

**Statistiques clés :**
- 💰 Coût total : 6,260 EUR
- 📅 29 interventions
- ⏱️ Durée moyenne : 130 minutes
- 📈 Tendance 2024 : HAUSSE (+75%)

## 🎯 Fonctionnalités

### 🆕 Gestion (CRUD - Create, Read, Update, Delete)
- ➕ **Ajouter Intervention** : Créer une nouvelle intervention de maintenance
- ➕ **Ajouter Technicien** : Enregistrer un nouveau technicien dans la base
- ➕ **Ajouter Équipement** : Ajouter un nouvel équipement au parc matériel

Chaque formulaire inclut :
- Validation des données en temps réel
- Messages d'erreur explicites
- Contraintes d'intégrité (email unique, numéro de série unique)
- Rollback automatique en cas d'erreur

📖 **Guide détaillé** : [GUIDE_GESTION.md](GUIDE_GESTION.md)

### Analyses SQL (Niveaux 1, 2 et 3)
- Indicateurs globaux (SUM, AVG, COUNT)
- Équipements les plus sollicités (GROUP BY, HAVING)
- Fréquence par type d'intervention (jointures multiples)
- Coût par type d'équipement (LEFT JOIN, COUNT DISTINCT)
- Interventions mensuelles (strftime, extraction de dates)
- Performance des techniciens (concaténation, agrégats)

### Calculs Python (Indicateurs Métier)
- ⚙️ **Taux de disponibilité** : % d'équipements actifs par type
- 📈 **Indice de fiabilité** : Score 0-100 basé sur pannes, coûts et âge
- 📊 **Tendance des coûts** : Analyse semestrielle avec variation %
- ⚠️ **Alertes maintenance** : Détection automatique des problèmes
- 📑 **Rapport de synthèse** : Vue consolidée de tous les indicateurs

## 🏗️ Architecture

```
maintenance_app/
├── database/
│   ├── maintenance.db          # Base SQLite (générée auto)
│   └── schema.sql              # Schéma + données de test
├── src/
│   ├── db_connection.py        # Couche connexion
│   ├── data_access.py          # Couche DAO (20 fonctions SQL + 4 fonctions INSERT)
│   ├── business_logic.py       # Couche métier (5 calculs Python)
│   ├── main.py                 # Interface CLI
│   ├── gui.py                  # Interface GUI Tkinter (+ formulaires de saisie)
│   ├── test_simple.py          # Tests de base
│   ├── test_fonctionnalites.py # Tests complets (10 tests)
│   ├── test_gui.py             # Tests de l'interface graphique (5 tests)
│   └── test_ajouts.py          # Tests des fonctionnalités d'ajout (4 tests)
├── lancer_gui.bat              # Script de lancement GUI
├── lancer_cli.bat              # Script de lancement CLI
├── GUIDE_DEMARRAGE.md          # Guide détaillé
└── DOCUMENTATION_PROJET.md     # Documentation technique
```

## 🔐 Sécurité

✅ Toutes les requêtes SQL utilisent des **paramètres** (`?`) pour éviter les injections SQL
✅ Gestion automatique des transactions (commit/rollback)
✅ Aucune f-string dans les requêtes SQL

```python
# ✅ CORRECT
cursor.execute("SELECT * FROM equipements WHERE id = ?", (equipement_id,))

# ❌ INTERDIT
cursor.execute(f"SELECT * FROM equipements WHERE id = {equipement_id}")
```

## 🧪 Tests

**Test simple (4 tests) :**
```bash
cd src
python test_simple.py
```

**Test complet (10 tests) :**
```bash
cd src
python test_fonctionnalites.py
```

**Test interface graphique (5 tests) :**
```bash
cd src
python test_gui.py
```

**Test fonctionnalités d'ajout (4 tests) :**
```bash
cd src
python test_ajouts.py
```
- Ajout de technicien
- Ajout d'équipement
- Ajout d'intervention
- Validation des contraintes

## 📚 Documentation

- **[GUIDE_DEMARRAGE.md](GUIDE_DEMARRAGE.md)** : Guide d'utilisation détaillé
- **[GUIDE_GESTION.md](GUIDE_GESTION.md)** : Guide des fonctionnalités d'ajout (CRUD)
- **[DOCUMENTATION_PROJET.md](DOCUMENTATION_PROJET.md)** : Architecture et choix techniques
- **[../RAPPORT_VERIFICATION.md](../RAPPORT_VERIFICATION.md)** : Rapport de tests et validation

## 💾 Base de Données

### Tables
- **techniciens** (5 entrées) : Informations sur les techniciens
- **equipements** (10 entrées) : Parc matériel à maintenir
- **interventions** (29 entrées) : Historique des interventions (table de liaison)

### Relations
```
TECHNICIENS (1,n) ──── (n,1) INTERVENTIONS (n,1) ──── (1,n) EQUIPEMENTS
```

### Contraintes
- Clés primaires auto-incrémentées
- Clés étrangères avec `ON DELETE RESTRICT`
- Contraintes `CHECK` pour valider types et statuts
- Contraintes `UNIQUE` sur numéro de série et email
- Index sur colonnes fréquemment interrogées

## 🛠️ Technologies

- **Python 3.x** : Langage principal
- **SQLite 3** : Base de données embarquée
- **Tkinter** : Interface graphique
- **sqlite3** : Driver Python natif (pas de dépendance externe)

## 📈 Exemples de Requêtes

### Niveau 1 : SELECT simple
```sql
SELECT * FROM equipements WHERE type = 'ordinateur' ORDER BY nom;
```

### Niveau 2 : Jointure + Agrégats
```sql
SELECT i.*, e.nom as equipement_nom, t.nom as technicien_nom
FROM interventions i
INNER JOIN equipements e ON i.equipement_id = e.id
INNER JOIN techniciens t ON i.technicien_id = t.id
WHERE i.statut = 'terminee';
```

### Niveau 3 : GROUP BY + HAVING + Fonctions de date
```sql
SELECT strftime('%m', date_intervention) as mois,
       COUNT(*) as nombre_interventions,
       SUM(cout) as cout_total
FROM interventions
WHERE strftime('%Y', date_intervention) = '2024'
GROUP BY strftime('%m', date_intervention)
ORDER BY mois;
```

## 📊 Captures d'Écran

### Interface Graphique
L'interface GUI Tkinter propose un menu latéral avec 12 fonctionnalités accessibles en un clic.

### Interface CLI
L'interface en ligne de commande offre les mêmes fonctionnalités via un menu numéroté.

## ✅ Validation

**État du projet :** ✅ 100% FONCTIONNEL

- ✅ Base de données relationnelle SQLite
- ✅ Requêtes SQL multi-niveaux (1, 2, 3)
- ✅ Calculs Python (5 indicateurs métier)
- ✅ Interface CLI complète
- ✅ Interface GUI Tkinter
- ✅ Architecture 3 couches
- ✅ Tests automatisés
- ✅ Documentation complète

## 🎓 Contexte Pédagogique

Ce projet a été développé dans le cadre d'un TP de Base de Données pour démontrer :
1. La maîtrise de SQL (niveaux 1, 2 et 3)
2. L'architecture logicielle en couches
3. Les bonnes pratiques de sécurité
4. Le calcul d'indicateurs métier
5. Le développement d'interfaces utilisateur

## 📝 Licence

Projet pédagogique - 2024

---

**🚀 Prêt à commencer ? Double-cliquez sur `lancer_gui.bat` !**
