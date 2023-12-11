import sqlite3


conn = sqlite3.connect('solution.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

#Similar to query2 this won't give us our data all in one line 
#So we will need to post process
cursor.execute('''
              Select year, count(genre), genre
              From 
                    genres, movies
              Where 
                    genres.MovieID = movies.MovieID
              Group by
                    year, genre;
               ''')
rows = cursor.fetchall()

#Open a file to write to
f = open("Answer3.txt", "w")
f.write("Year, Count, Genre \n")

answer_dict = {}

#Format our data
#row[0] is our year
#row[1] is our count
#row[2] is our genre
for row in rows:
    #We want to check if our year already exists, if it does, add more genres
    if row[0] in answer_dict:
        answer_dict[row[0]] += ", " + str(row[1]) + " " + row[2]
    else:
       answer_dict[row[0]] = str(row[1]) + " " + row[2]

#Write the results to the file
for title in answer_dict:
  f.write(str(title) +  " : " + answer_dict[title] + "\n")
# Close the cursor and connection
cursor.close()
conn.close()

#Close the file
f.close()