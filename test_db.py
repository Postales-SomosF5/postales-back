import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

try:
    conn = pymysql.connect(
        host=os.getenv('MYSQL_HOST', '127.0.0.1'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', '1234'),  # ¡vacío!
        database=os.getenv('MYSQL_DB', 'postales')
    )
    print("✅ ¡Conexión exitosa a MySQL!")
    conn.close()
except Exception as e:
    print("❌ Error:", e)