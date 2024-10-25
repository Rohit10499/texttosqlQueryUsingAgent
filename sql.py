import sqlite3
import pandas as pd

db_name = 'my_database.db'  
conn = sqlite3.connect(db_name)

customer_df = pd.read_csv('Customer.csv')  
sales_df = pd.read_csv('Sales.csv')        
product_df = pd.read_csv('Product.csv')    

customer_df.to_sql('Customer', conn, if_exists='replace', index=False)
sales_df.to_sql('Sales', conn, if_exists='replace', index=False)
product_df.to_sql('Product', conn, if_exists='replace', index=False)

cursor = conn.cursor()

print("Customer Table:")
cursor.execute('SELECT * FROM Customer LIMIT 5')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Query Sales Table
print("\nSales Table:")
cursor.execute('SELECT * FROM Sales LIMIT 5')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Query Product Table
print("\nProduct Table:")
cursor.execute('SELECT * FROM Product LIMIT 5')
rows = cursor.fetchall()
for row in rows:
    print(row)


conn.close()
