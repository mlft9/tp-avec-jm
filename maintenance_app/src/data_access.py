from db_connection import obtenir_connexion


# ========== FONCTIONS DE BASE ==========
def obtenir_tous_equipements():
    """Retourne tous les équipements."""
    conn = obtenir_connexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM equipements ORDER BY nom")
    return [dict(row) for row in cursor.fetchall()]


def obtenir_equipement_par_id(equipement_id):
    """Retourne un équipement par son ID."""
    conn = obtenir_connexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM equipements WHERE id = ?", (equipement_id,))
    row = cursor.fetchone()
    return dict(row) if row else None


def obtenir_toutes_interventions():
    """Retourne toutes les interventions."""
    conn = obtenir_connexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interventions ORDER BY date_intervention DESC")
    return [dict(row) for row in cursor.fetchall()]


# ========== STATISTIQUES SIMPLES ==========
def obtenir_cout_total():
    """Calcule le coût total de maintenance."""
    conn = obtenir_connexion()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(cout) as total FROM interventions WHERE statut = 'terminee'")
    result = cursor.fetchone()
    return result['total'] if result['total'] else 0.0


def obtenir_nombre_interventions():
    """Compte le nombre total d'interventions."""
    conn = obtenir_connexion()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM interventions")
    return cursor.fetchone()['count']


def obtenir_duree_moyenne():
    """Calcule la durée moyenne des interventions."""
    conn = obtenir_connexion()
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(duree_minutes) as moyenne FROM interventions WHERE statut = 'terminee'")
    result = cursor.fetchone()
    return round(result['moyenne'], 2) if result['moyenne'] else 0.0


# ========== STATISTIQUES AVANCÉES ==========
def obtenir_equipements_sollicites(limit=5):
    """Retourne les équipements avec le plus d'interventions."""
    conn = obtenir_connexion()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id, e.nom, e.type,
               COUNT(i.id) as nombre_interventions,
               SUM(i.cout) as cout_total,
               SUM(i.duree_minutes) as duree_totale
        FROM equipements e
        LEFT JOIN interventions i ON e.id = i.equipement_id
        GROUP BY e.id
        HAVING COUNT(i.id) > 0
        ORDER BY nombre_interventions DESC
        LIMIT ?
    """, (limit,))
    return [dict(row) for row in cursor.fetchall()]


def obtenir_frequence_par_type():
    """Nombre d'interventions par type."""
    conn = obtenir_connexion()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT type_intervention,
               COUNT(*) as nombre,
               SUM(cout) as cout_total,
               AVG(cout) as cout_moyen,
               AVG(duree_minutes) as duree_moyenne
        FROM interventions
        WHERE statut = 'terminee'
        GROUP BY type_intervention
        ORDER BY nombre DESC
    """)
    return [dict(row) for row in cursor.fetchall()]


def obtenir_cout_par_type_equipement():
    """Coût de maintenance par type d'équipement."""
    conn = obtenir_connexion()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.type,
               COUNT(DISTINCT e.id) as nombre_equipements,
               COUNT(i.id) as nombre_interventions,
               SUM(i.cout) as cout_total,
               AVG(i.cout) as cout_moyen_intervention
        FROM equipements e
        LEFT JOIN interventions i ON e.id = i.equipement_id AND i.statut = 'terminee'
        GROUP BY e.type
        ORDER BY cout_total DESC
    """)
    return [dict(row) for row in cursor.fetchall()]


def obtenir_interventions_par_mois(annee):
    """Interventions groupées par mois pour une année."""
    conn = obtenir_connexion()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT strftime('%m', date_intervention) as mois,
               COUNT(*) as nombre_interventions,
               SUM(cout) as cout_total,
               SUM(duree_minutes) as duree_totale
        FROM interventions
        WHERE strftime('%Y', date_intervention) = ?
          AND statut = 'terminee'
        GROUP BY strftime('%m', date_intervention)
        ORDER BY mois
    """, (str(annee),))
    return [dict(row) for row in cursor.fetchall()]


def obtenir_performance_techniciens():
    """Performance des techniciens."""
    conn = obtenir_connexion()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id,
               t.nom || ' ' || t.prenom as technicien,
               t.specialite,
               COUNT(i.id) as nombre_interventions,
               SUM(i.duree_minutes) as temps_total,
               SUM(i.cout) as valeur_interventions
        FROM techniciens t
        LEFT JOIN interventions i ON t.id = i.technicien_id AND i.statut = 'terminee'
        GROUP BY t.id
        ORDER BY nombre_interventions DESC
    """)
    return [dict(row) for row in cursor.fetchall()]


def obtenir_historique_equipement(equipement_id):
    """Historique complet d'un équipement."""
    conn = obtenir_connexion()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.date_intervention,
               i.type_intervention,
               i.description,
               i.duree_minutes,
               i.cout,
               i.statut,
               t.nom || ' ' || t.prenom as technicien
        FROM interventions i
        INNER JOIN techniciens t ON i.technicien_id = t.id
        WHERE i.equipement_id = ?
        ORDER BY i.date_intervention DESC
    """, (equipement_id,))
    return [dict(row) for row in cursor.fetchall()]


def obtenir_interventions_completes():
    """Toutes les interventions avec détails (pour les calculs Python)."""
    conn = obtenir_connexion()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.*,
               e.nom as equipement_nom,
               e.type as equipement_type
        FROM interventions i
        INNER JOIN equipements e ON i.equipement_id = e.id
        WHERE i.statut = 'terminee'
        ORDER BY i.date_intervention
    """)
    return [dict(row) for row in cursor.fetchall()]
