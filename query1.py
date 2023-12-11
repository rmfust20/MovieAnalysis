import sqlite3

conn = sqlite3.connect('solution.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

#This query will give us movies sorted by average rating
cursor.execute('''
               with h as (
                Select 
                    MovieID as ID, avg(rating) as average
                From
                    ratings
                Group by 
                    MovieID
                Order by 
                    average)
               select
                     movies.Title, h.average
               from 
                    movies, h
               where
                    movies.MovieID = h.ID;
               ''')
rows = cursor.fetchall()

#Open a file to write to
f = open("Answer1.txt", "w")
f.write("Title, Average Rating \n")

# Write the results to a file
for row in rows:
    f.write(str(row[0]) + ", " + str(row[1]) +  "\n")

# Close the cursor and connection
cursor.close()
conn.close()

#Close the file
f.close()