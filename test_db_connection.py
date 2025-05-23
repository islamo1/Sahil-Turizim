import psycopg2

try:
    connection = psycopg2.connect(
        dbname="railway",
        user="postgres",
        password="OPUaepLnyJRwgMkFtQAYZZtgZztUUEwy",
        host="maglev.proxy.rlwy.net",
        port="44581",
        sslmode="require"
    )
    print("✅ الاتصال ناجح!")
    connection.close()

except Exception as e:
    print("❌ فشل الاتصال:")
    print(e)
