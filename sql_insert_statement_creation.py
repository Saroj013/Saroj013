### create insert statement

import pandas as pd

# Load the CSV file
df = pd.read_csv("athlete_events.csv")

# Function to make values SQL-safe based on column type
def sql_safe(value, is_numeric=False):
    if pd.isna(value) or value == "":  
        return "NULL"
    elif is_numeric:  # Numeric values (id, age, year)
        return str(int(value)) if isinstance(value, float) and value.is_integer() else str(value)
    elif isinstance(value, str):  
        return "'{}'".format(value.replace("'", "''"))  # Escape single quotes
    else:  
        return str(value)

# Generate SQL insert statements
sql_statements = "INSERT INTO athlete_events (id, name, sex, age, height, weight, team, noc, games, year, season, city, sport, event, medal) VALUES\n"
values_list = []

for _, row in df.iterrows():
    values = (
        sql_safe(row["ID"], is_numeric=True),   # number(10)
        sql_safe(row["Name"]),                  # varchar2(20)
        sql_safe(row["Sex"]),                   # varchar2(1)
        sql_safe(row["Age"], is_numeric=True),  # number(3)
        sql_safe(str(row["Height"])),           # varchar2(5) (string)
        sql_safe(str(row["Weight"])),           # varchar2(20) (string)
        sql_safe(row["Team"]),                  # varchar2(25)
        sql_safe(row["NOC"]),                   # varchar2(10)
        sql_safe(row["Games"]),                 # varchar2(20)
        sql_safe(row["Year"], is_numeric=True), # number(4)
        sql_safe(row["Season"]),                # varchar2(10)
        sql_safe(row["City"]),                  # varchar2(20)
        sql_safe(row["Sport"]),                 # varchar2(15)
        sql_safe(row["Event"]),                 # varchar2(20)
        sql_safe(row["Medal"])                  # varchar2(10)
    )
    values_list.append("({})".format(", ".join(values)))

sql_statements += ",\n".join(values_list) + ";\n"

# Save to a file
with open("insert_athlete_events.sql", "w", encoding="utf-8") as f:
    f.write(sql_statements)

print("✅ SQL file generated: insert_athlete_events.sql")
