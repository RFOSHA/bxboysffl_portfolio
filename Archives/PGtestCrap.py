import psycopg2

# Update connection string information
host = "bxboysffltestpostgres.postgres.database.azure.com"
dbname = "postgres"
user = "user@bxboysffltestpostgres"
password = "42itZX!1"
sslmode = "require"

# Construct connection string
conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)
print("Connection established")

cursor = conn.cursor()

sql = "SELECT * from fp_totals"
cursor.execute(sql)
records = cursor.fetchall()
for row in records:
    if row[1] == 'Ryan':
        print(row[2])
    print(row)

cursor.close()
conn.close()


