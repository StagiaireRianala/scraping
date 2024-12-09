import psycopg2

try:
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="myuser",
        password="mypassword",
        host="postgres",
        port=5432
    )
    print("Connexion réussie à PostgreSQL !")
    conn.close()
except Exception as e:
    print(f"Erreur de connexion : {e}")
