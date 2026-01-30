# Documentation Projet - Application de Maintenance

---

## 1. Entités identifiées

**3 entités principales:**

1. **TECHNICIENS** - Les personnes qui effectuent les interventions
2. **EQUIPEMENTS** - Le matériel à maintenir
3. **INTERVENTIONS** - Les actions de maintenance (table de liaison)

---

## 2. Clés primaires

### Table TECHNICIENS
- **Clé primaire:** `id` (INTEGER, AUTO_INCREMENT)
- Contrainte unique: `email`

### Table EQUIPEMENTS
- **Clé primaire:** `id` (INTEGER, AUTO_INCREMENT)
- Contrainte unique: `numero_serie`

### Table INTERVENTIONS
- **Clé primaire:** `id` (INTEGER, AUTO_INCREMENT)
- **Clés étrangères:**
  - `equipement_id` → `equipements(id)`
  - `technicien_id` → `techniciens(id)`

---

## 3. Relations

```
TECHNICIENS (1,n) ──── (n,1) INTERVENTIONS (n,1) ──── (1,n) EQUIPEMENTS
```

**Type de relation:** N-N (Many-to-Many)
- Un technicien peut faire plusieurs interventions
- Un équipement peut avoir plusieurs interventions
- `INTERVENTIONS` est la table de liaison

---

## 4. Niveau 1 – Requêtes simples

### Exemple 1: SELECT simple
```sql
SELECT * FROM equipements ORDER BY nom;
```

### Exemple 2: SELECT avec WHERE
```sql
SELECT * FROM equipements WHERE id = ?;
```

### Exemple 3: INSERT
```sql
INSERT INTO interventions (equipement_id, technicien_id, date_intervention,
                           type_intervention, description, duree_minutes, cout, statut)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
```

---

## 5. Niveau 2 – Requêtes intermédiaires

### Exemple 1: Agrégat SUM
```sql
SELECT SUM(cout) as total
FROM interventions
WHERE statut = 'terminee';
```

### Exemple 2: Agrégat COUNT
```sql
SELECT COUNT(*) as count FROM interventions;
```

### Exemple 3: Agrégat AVG
```sql
SELECT AVG(duree_minutes) as moyenne
FROM interventions
WHERE statut = 'terminee';
```

### Exemple 4: Jointure INNER JOIN
```sql
SELECT i.*, e.nom as equipement_nom, e.type as equipement_type
FROM interventions i
INNER JOIN equipements e ON i.equipement_id = e.id
WHERE i.statut = 'terminee';
```

---

## 6. Niveau 3 – Requêtes avancées

### Exemple 1: GROUP BY + HAVING + Agrégats
```sql
SELECT e.id, e.nom, e.type,
       COUNT(i.id) as nombre_interventions,
       SUM(i.cout) as cout_total,
       SUM(i.duree_minutes) as duree_totale
FROM equipements e
LEFT JOIN interventions i ON e.id = i.equipement_id
GROUP BY e.id
HAVING COUNT(i.id) > 0
ORDER BY nombre_interventions DESC
LIMIT 5;
```

### Exemple 2: GROUP BY avec multiples agrégats
```sql
SELECT type_intervention,
       COUNT(*) as nombre,
       SUM(cout) as cout_total,
       AVG(cout) as cout_moyen,
       AVG(duree_minutes) as duree_moyenne
FROM interventions
WHERE statut = 'terminee'
GROUP BY type_intervention
ORDER BY nombre DESC;
```

### Exemple 3: GROUP BY + Jointure + COUNT DISTINCT
```sql
SELECT e.type,
       COUNT(DISTINCT e.id) as nombre_equipements,
       COUNT(i.id) as nombre_interventions,
       SUM(i.cout) as cout_total,
       AVG(i.cout) as cout_moyen_intervention
FROM equipements e
LEFT JOIN interventions i ON e.id = i.equipement_id AND i.statut = 'terminee'
GROUP BY e.type
ORDER BY cout_total DESC;
```

### Exemple 4: GROUP BY avec fonction de date (strftime)
```sql
SELECT strftime('%m', date_intervention) as mois,
       COUNT(*) as nombre_interventions,
       SUM(cout) as cout_total,
       SUM(duree_minutes) as duree_totale
FROM interventions
WHERE strftime('%Y', date_intervention) = '2024'
  AND statut = 'terminee'
GROUP BY strftime('%m', date_intervention)
ORDER BY mois;
```

### Exemple 5: LEFT JOIN + GROUP BY + concaténation
```sql
SELECT t.id,
       t.nom || ' ' || t.prenom as technicien,
       t.specialite,
       COUNT(i.id) as nombre_interventions,
       SUM(i.duree_minutes) as temps_total,
       SUM(i.cout) as valeur_interventions
FROM techniciens t
LEFT JOIN interventions i ON t.id = i.technicien_id AND i.statut = 'terminee'
GROUP BY t.id
ORDER BY nombre_interventions DESC;
```

---

## 7. Choix techniques

### Architecture
- **3 couches**: Interface (main.py) → Logique métier (business_logic.py) → Accès données (data_access.py)
- Séparation des responsabilités pour faciliter la maintenance

### Base de données
- **SQLite**: Base légère, un seul fichier, pas de serveur, parfait pour un projet pédagogique
- Intégration native avec Python (module sqlite3)

### Sécurité
- **Requêtes paramétrées**: Utilisation de `?` pour éviter les injections SQL
- Exemple: `cursor.execute("SELECT * FROM equipements WHERE id = ?", (id,))`

### Calculs Python
Certains indicateurs sont calculés en Python (pas en SQL):
- **Taux de disponibilité**: Pourcentage d'équipements actifs par type
- **Indice de fiabilité**: Score basé sur pannes, coûts et âge
- **Tendance des coûts**: Analyse semestrielle avec variation %
- **Alertes**: Génération de messages selon règles métier

### Code simplifié
- Fonctions simples au lieu de classes complexes
- Nommage en français pour faciliter la compréhension
- Pas de patterns avancés (Singleton, décorateurs, etc.)
- Adapté au niveau étudiant 2ème année
