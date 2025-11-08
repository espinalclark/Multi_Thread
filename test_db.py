from database import get_connection

conn = get_connection()
cur = conn.cursor()
cur.execute("SELECT DATABASE();")
print("Conectado a la base de datos:", cur.fetchone()[0])
conn.close()

