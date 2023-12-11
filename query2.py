import sqlite3

conn = sqlite3.connect('solution.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

#This quert will give us the average rating for each gender
#We will have to do a bit of work after the query since this will give us
#Male and female seperate ratings, we want both on the same line
cursor.execute('''
               with h as(
               Select 
                    users.UserID, MovieID as ID, Gender as gender, avg(Rating) as average
                From
                    users, ratings
                Where 
                    users.UserID = ratings.UserID
                Group by 
                    MovieID, Gender)
               Select
                    h.gender, movies.Title, h.average
               From
                    movies,h
               Where
                    movies.MovieID = h.ID
               Order by 
                    Title
               ''')
rows = cursor.fetchall()

#Open a file to write to 
f = open("Answer2.txt", "w")
f.write("Title, Average Rating, Gender \n")

#Using a dictionary will help us with our reformatting 
answer_dict = {}
#Movie_Name - 3.5 (Avg. male users rating) - 4.5 (Avg. female Users rating)
for row in rows:
    #Figure out what our gender is 
    gender = str(row[0])
    if gender == 'F':
       gender = "female"
    else:
       gender = "male"
    rating = str(row[2])
    #Check if the record is already in the dictionary
    #If it is we will just add the second gender and their rating
    if row[1] in answer_dict:
       answer_dict[row[1]] += "- " + rating + " (Avg. " + gender + " users rating) "
    else:
       answer_dict[row[1]] = rating + " (Avg. " + gender + " users rating) " 

#Write to the file
for x in answer_dict:
  f.write(x +  " : " + answer_dict[x] + "\n")

# Close the cursor and connection
cursor.close()
conn.close()

#Close the File
f.close()