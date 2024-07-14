import sqlite3
import pandas as pd

# Define the path to your CSV file
csv_file_path = 'StudentsPerformance.csv'

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('students.db')

df.to_sql('students', conn, if_exists='replace', index=False)

# Execute the ALTER TABLE statement
conn.execute('ALTER TABLE students ADD COLUMN average_score REAL;')

# Execute the UPDATE statement
conn.execute('UPDATE students SET average_score = ("math score" + "reading score" + "writing score") / 3;')

queries = {
    "filtered_male": "SELECT * FROM students WHERE gender = 'male';",
    "filtered_female": "SELECT * FROM students WHERE gender = 'female';",
    "scores_by_race": """
        SELECT "race/ethnicity", AVG("math score") AS avg_math_score, AVG("reading score") AS avg_reading_score, AVG("writing score") AS avg_writing_score
        FROM students GROUP BY "race/ethnicity";
    """,
    "students_by_education": """
        SELECT "parental level of education", COUNT(*) AS student_count
        FROM students GROUP BY "parental level of education";
    """,
    "scores_by_lunch": """
        SELECT lunch, AVG("math score") AS avg_math_score, AVG("reading score") AS avg_reading_score, AVG("writing score") AS avg_writing_score
        FROM students GROUP BY lunch;
    """,
    "top_performers": """
        SELECT * FROM students
        ORDER BY average_score DESC
        LIMIT (SELECT COUNT(*) FROM students) / 10;
    """
}

# Execute each query and save the results to CSV
for name, query in queries.items():
    df_result = pd.read_sql_query(query, conn)
    df_result.to_csv(f'{name}.csv', index=False)


# Write the DataFrame to the SQL database
df.to_sql('students', conn, if_exists='replace', index=False)

# Close the connection
conn.close()


