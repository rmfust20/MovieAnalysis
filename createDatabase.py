import sqlite3

#open the files to import data into sql tables
with open('movies.dat', 'rb') as f:
    movies = f.readlines()

with open('ratings.dat', 'rb') as g:
    ratings = g.readlines()

with open('users.dat', 'rb') as h:
    users = h.readlines()

# Connect to SQLite database (creates a new database if it doesn't exist)
conn = sqlite3.connect('solution.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

#create the users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        UserID INTEGER PRIMARY KEY,
        Gender TEXT,
        Age INTEGER,
        Occupation INTEGER,
        ZipCode TEXT
    );
''')

#create the movies table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        MovieID INTEGER PRIMARY KEY,
        Title TEXT,
        Year INTEGER
    );
''')

# Create the ratings table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ratings (
        UserID INTEGER,
        MovieID INTEGER,
        Rating INTEGER,
        Timestamp INTEGER,
        PRIMARY KEY (UserID, MovieID),
        FOREIGN KEY (UserID) REFERENCES users(UserID),
        FOREIGN KEY (MovieID) REFERENCES movies(MovieID) 
    );
''')

#creates a genres table (this will help handle multi value dependencies)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS genres (
        genre TEXT,
        MovieID INTEGER,
        FOREIGN KEY (MovieID) REFERENCES movies(MovieID) 
    );
''')

#inser data into users
for currentUser in users:
    tempUser = currentUser.decode('utf-8')
    #split tempUser to extract each field
    user = tempUser.split("::")
    userData = (int(user[0]), user[1], int(user[2]), int(user[3]),user[4])
    cursor.execute('''
            Insert INTO users
            (UserID, Gender, Age, Occupation, ZipCode)
            Values
            (?,?,?,?,?);
    ''', userData)

#insert data into movies
for currentMovie in movies:
    #have to do latin here since we have some malformed titles
    tempMovie = currentMovie.decode('latin-1')
    #split tempMovie to extract each field
    movie = tempMovie.split("::")
    #year is always in the same spot if we go backwards
    year = movie[1][-5:-1]
    movieData = (int(movie[0]), movie[1], int(year))
    cursor.execute('''
            Insert INTO movies
            (MovieID, Title, Year)
            Values
            (?,?,?);
    ''', movieData)

#insert data into genres
for currentMovie in movies:
    #have to do latin here since we have some malformed titles
    tempMovie = currentMovie.decode('latin-1')
    #split tempMovie to extract fields
    movie = tempMovie.split("::")
    year = movie[1][-5:-1]
    #split genreList to extract each genre
    genreList = movie[2].split("|")
    #this removes the \"n" that was being generated
    genreList[len(genreList) -1] = genreList[len(genreList) -1][0:-1]
    #loop through each genre to add into genre table, with associated MovieID
    for currentGenre in genreList:
        genreData = (currentGenre, int(movie[0]))
        cursor.execute('''
                Insert INTO genres
                (Genre, MovieID)
                Values
                (?,?);
        ''', genreData)

#insert data into ratings
for currentRating in ratings:
    tempRating = currentRating.decode('utf-8')
    #split tempRating to extract fields
    rating = tempRating.split("::")
    ratingData = (int(rating[0]), int(rating[1]), int(rating[2]), int(rating[3]))
    cursor.execute('''
            Insert INTO ratings
            (UserID, MovieID, Rating, Timestamp)
            Values
            (?,?,?,?);
    ''', ratingData)

# Commit the changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

# Close our files
f.close()
g.close()
h.close()