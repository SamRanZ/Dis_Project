from flask import Flask, render_template, jsonify, request
import psycopg2

app = Flask(__name__)

# Database connection configuration
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'DISProject'
DB_USER = 'testuser'
DB_PASS = '123'

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schools', methods=['GET'])
def get_schools():
    search_query = request.args.get('search', '')
    sort_column = request.args.get('sort', 'School Name')
    sort_direction = request.args.get('direction', 'asc')
    
    # Ensure valid sort column and direction
    valid_columns = ['School Name', 'Number of Test Takers', 'Critical Reading Mean', 'Mathematics Mean', 'Writing Mean']
    if sort_column not in valid_columns:
        sort_column = 'School Name'
    if sort_direction not in ['asc', 'desc']:
        sort_direction = 'asc'
    
    conn = get_db_connection()
    if conn is None:
        return "Error connecting to the database", 500
    
    cursor = conn.cursor()
    query = f"""
        SELECT "DBN", "School Name", "Number of Test Takers", "Critical Reading Mean", "Mathematics Mean", "Writing Mean"
        FROM public."School"
    """
    
    if search_query:
        query += f" WHERE \"School Name\" ~* %s"
        query += f" ORDER BY \"{sort_column}\" {sort_direction} NULLS LAST;"
        cursor.execute(query, (search_query,))
    else:
        query += f" ORDER BY \"{sort_column}\" {sort_direction} NULLS LAST;"
        cursor.execute(query)
    
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    schools_list = []
    for row in rows:
        school = {
            'DBN': row[0],
            'School Name': row[1],
            'Number of Test Takers': row[2],
            'Critical Reading Mean': row[3],
            'Mathematics Mean': row[4],
            'Writing Mean': row[5]
        }
        schools_list.append(school)
    
    return jsonify(schools_list)

if __name__ == '__main__':
    app.run(debug=True)
