import psycopg2

# Database connection configuration
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'DISProject'
DB_USER = 'testServer'
DB_PASS = '123'

def test_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        print("Connection successful")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_connection()
