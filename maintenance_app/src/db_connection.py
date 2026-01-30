import sqlite3
from pathlib import Path


# Chemin vers la base de données
DATABASE_PATH = Path(__file__).parent.parent / "database" / "maintenance.db"
SCHEMA_PATH = Path(__file__).parent.parent / "database" / "schema.sql"

# Connexion globale (plus simple qu'un Singleton)
connexion = None


def obtenir_connexion():
    """Retourne la connexion à la base de données."""
    global connexion

    if connexion is None:
        connexion = sqlite3.connect(DATABASE_PATH)
        connexion.row_factory = sqlite3.Row  # Pour avoir des dictionnaires

    return connexion


def fermer_connexion():
    """Ferme la connexion."""
    global connexion
    if connexion:
        connexion.close()
        connexion = None


def init_database():
    """Initialise la base de données avec le script schema.sql."""
    # Lire le fichier SQL
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    # Créer les tables
    conn = obtenir_connexion()
    conn.executescript(schema_sql)
    conn.commit()
    print(f"Base de données créée: {DATABASE_PATH}")


def database_exists():
    """Vérifie si la base existe."""
    if not DATABASE_PATH.exists():
        return False

    try:
        conn = obtenir_connexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name IN ('techniciens', 'equipements', 'interventions')
        """)
        tables = cursor.fetchall()
        return len(tables) == 3
    except:
        return False
