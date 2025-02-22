import sqlite3
from sqlite3 import Error
import os

class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """Initialise la connexion à la base de données SQLite."""
        if not hasattr(self, 'initialized'):
            self.db_file = os.path.join(os.path.dirname(__file__), '..', 'database', 'db.sqlite')
            self.connection = None
            try:
                self.connection = sqlite3.connect(self.db_file)
                print(f"Connexion à la base de données SQLite réussie : {self.db_file}")
            except Error as e:
                print(f"Erreur lors de la connexion à la base de données : {e}")
            self.initialized = True

    def execute_query(self, query, params=None):
        """Exécute une requête SQL."""
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            print("Requête exécutée avec succès")
        except Error as e:
            print(f"Erreur lors de l'exécution de la requête : {e}")

    def execute_read_query(self, query, params=None):
        """Exécute une requête SQL de lecture et retourne les résultats."""
        cursor = self.connection.cursor()
        result = None
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Erreur lors de l'exécution de la requête de lecture : {e}")
            return result

    def close_connection(self):
        """Ferme la connexion à la base de données."""
        if self.connection:
            self.connection.close()
            print("Connexion à la base de données fermée")

    def create_table(self, table_name, fields):
        """Crée une table dans la base de données."""
        fields_sql = ", ".join(fields)
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({fields_sql})"
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_sql)
            self.connection.commit()
            print(f"Table '{table_name}' créée avec succès")
        except Error as e:
            print(f"Erreur lors de la création de la table '{table_name}' : {e}")