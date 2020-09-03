import psycopg2

#to make initial DB on VM
#REMEMBER TO MAKE TRIGGERS TO LIMIT NO.OF FIELDS IN TAG TABLES
try:
    conn = psycopg2.connect("dbname='crajy' user='postgres' host='localhost' password='password'")
    cursor = conn.cursor()
except:
    print("Make the utils, set the password, use the right password here")

def create_prefixes_table() -> None:
    cursor.execute("CREATE TABLE IF NOT EXISTS prefixes (guild_id BIGINT PRIMARY KEY, prefix VARCHAR(3) DEFAULT '.')")

def create_global_tags_table() -> None:
    cursor.execute("CREATE TABLE IF NOT EXISTS global_tags (tag VARCHAR(20) PRIMARY KEY, value VARCHAR(500) UNIQUE NOT NULL, created_by BIGINT NOT NULL)")

def create_guild_tags_table() -> None:
    cursor.execute("CREATE TABLE IF NOT EXISTS guild_tags (guild_id BIGINT NOT NULL ,tag VARCHAR(20) PRIMARY KEY, value VARCHAR(500) UNIQUE NOT NULL, created_by BIGINT NOT NULL)")
