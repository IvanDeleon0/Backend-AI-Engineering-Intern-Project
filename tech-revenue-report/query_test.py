import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="techrevenue",
    user="postgres",
    password="postgres",
)
cur = conn.cursor()
cur.execute("SELECT name, sector, revenue, revenue_year FROM companies ORDER BY revenue DESC")
rows = cur.fetchall()
cur.close()
conn.close()

for row in rows:
    print(row)