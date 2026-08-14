import psycopg2

companies = [
    ("Apple", "Hardware", 391_000_000_000, 2024),
    ("Microsoft", "Software", 245_000_000_000, 2024),
    ("Amazon", "E-commerce", 638_000_000_000, 2024),
    ("Alphabet", "Internet Services", 350_000_000_000, 2024),
    ("Meta", "Internet Services", 164_000_000_000, 2024),
    ("Nvidia", "Semiconductors", 130_000_000_000, 2024),
    ("Samsung Electronics", "Hardware", 200_000_000_000, 2024),
    ("TSMC", "Semiconductors", 90_000_000_000, 2024),
    ("Tencent", "Internet Services", 90_000_000_000, 2024),
    ("Oracle", "Software", 53_000_000_000, 2024),
    ("IBM", "Software", 62_000_000_000, 2024),
    ("Intel", "Semiconductors", 53_000_000_000, 2024),
    ("Salesforce", "Software", 37_000_000_000, 2024),
    ("Adobe", "Software", 21_000_000_000, 2024),
    ("SAP", "Software", 34_000_000_000, 2024),
    ("Sony", "Hardware", 85_000_000_000, 2024),
    ("Cisco", "Hardware", 54_000_000_000, 2024),
    ("Netflix", "Internet Services", 39_000_000_000, 2024),
    ("Qualcomm", "Semiconductors", 39_000_000_000, 2024),
    ("Spotify", "Internet Services", 15_000_000_000, 2024),
]

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="techrevenue",
    user="postgres",
    password="postgres",
)
cur = conn.cursor()

for name, sector, revenue, year in companies:
    cur.execute(
        "INSERT INTO companies (name, sector, revenue, revenue_year) VALUES (%s, %s, %s, %s)",
        (name, sector, revenue, year),
    )

conn.commit()
cur.close()
conn.close()
print(f"Inserted {len(companies)} companies.")