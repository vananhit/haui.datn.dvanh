import pyodbc
server = 'DESKTOP-H1KK6UA'
database = 'CheckInDB'
username = 'dvanh'
password = '12345678@Abc'
driver = '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect(f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}")
cursor = cnxn.cursor()