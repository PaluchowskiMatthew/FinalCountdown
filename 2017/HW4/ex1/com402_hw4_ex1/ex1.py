#!/usr/bin/env python3
import random, datetime, sys, csv
from random import randrange, randint
import random, string
import os
import pickle
import hashlib
import crypt

date_start = datetime.date(2000, 1, 1)
date_period = 365 * 17

def randomword(length):
   return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

# Reads in emails.txt and movies.txt and creates 'nbr_movies' entries for each
# email.
# Returns the database, the emails and the movies in the following format:
# [ [ user, movie, date, grade ], ... ]
def create_db(nbr_movies):
    with open("emails.txt") as f:
        emails = f.read().split("\n");
    while "" in emails:
        emails.remove("")

    with open("movies.txt") as f:
        movies = f.read().split("\n");
    while "" in movies:
        movies.remove("")

    db = []

    for email in emails:
        movies_index = list(range(0, len(movies)))
        random.shuffle(movies_index)
        for i, f in enumerate(movies_index[0:nbr_movies]):
            dat = date_start + datetime.timedelta(randint(1, date_period))
            db.append(
                [email, movies[f], dat.strftime("%Y/%m/%d"), randint(1, 5)])

    return db, emails, movies


# Anonymize the given database, but still let the get_movies_with_rating
# function give the right answers.
def anonymize_1(db):
    db_salt = randomword(8)


    for i, line in enumerate(db):
        email = line[0]
        movie = line[1]
        date = line[2]
        rating = line[3]

        salted_entry = str('*') + crypt.mksalt(crypt.METHOD_SHA512)
        entry_bytes = str.encode(salted_entry)
        email_hash = hashlib.sha512(entry_bytes).hexdigest()
        db[i][0] = '*'#email_hash

        # if movie not in movie_hashes:
        #     salted_entry = str(movie) + crypt.mksalt(crypt.METHOD_SHA256)
        #     entry_bytes = str.encode(salted_entry)
        #     movie_hashes[movie] = hashlib.sha256(entry_bytes).hexdigest()
        # db[i][1] = movie_hashes[movie]

        day_offset = random.randint(-356,356)
        date_1 = datetime.datetime.strptime(date, "%Y/%m/%d")
        end_date = date_1 + datetime.timedelta(days=day_offset)
        db[i][2] = '*' #end_date.strftime("%Y/%m/%d")

        # if rating not in rating_hashes:
        #     salted_entry = str(rating) + crypt.mksalt(crypt.METHOD_SHA256)
        #     entry_bytes = str.encode(salted_entry)
        #     rating_hashes[rating] = hashlib.sha256(entry_bytes).hexdigest()
        # db[i][3] = rating_hashes[rating]


    return db


# For a given anonymized-database and a rating, this function should return
# the films with the given rating.
def get_movies_with_rating(anon, rating):
    movies = []
    for i, line in enumerate(anon):
        # print(line)
        email = line[0]
        movie = line[1]
        date = line[2]
        rating_an = line[3]

        if rating == rating_an:
            movies += [movie]

    return list(set(movies))


# A bit lesser anonymization than anonymize_1, but still no date. The returned
# database should have enough information to be used by get_top_rated. If you
# use a too simple hashing-function like sha-256, the result will be rejected.
def anonymize_2(db):
    db_salt = randomword(8)

    for i, line in enumerate(db):
        email = line[0]
        movie = line[1]
        date = line[2]
        rating = line[3]

        salted_entry = str('*') + crypt.mksalt(crypt.METHOD_SHA512)
        entry_bytes = str.encode(salted_entry)
        email_hash = hashlib.sha512(entry_bytes).hexdigest()
        db[i][0] = email_hash

        # if movie not in movie_hashes:
        #     salted_entry = str(movie) + crypt.mksalt(crypt.METHOD_SHA256)
        #     entry_bytes = str.encode(salted_entry)
        #     movie_hashes[movie] = hashlib.sha256(entry_bytes).hexdigest()
        # db[i][1] = movie_hashes[movie]

        # day_offset = random.randint(-356,356)
        # date_1 = datetime.datetime.strptime(date, "%Y/%m/%d")
        # end_date = date_1 + datetime.timedelta(days=day_offset)
        db[i][2] = '*'#end_date.strftime("%Y/%m/%d")

    return db


# get_top_rated searches for all users having rated a movie and searches their
# top-rated movie(s). It returns a list of all found movies, also doubles!
def get_top_rated(anon, movie):
    users = {}

    users_who_rated = []
    for i, line in enumerate(anon):
        # print(line)
        # break
        email = line[0]
        movie_an = line[1]
        date = line[2]
        rating_an = line[3]

        if email in users:
            ratings = users[email]
            ratings[rating_an] += [movie_an]
            users[email] = ratings
        else:
            rated_movies = {1: [], 2: [], 3: [], 4: [], 5: []}
            rated_movies[rating_an] = [movie_an]
            users[email] = rated_movies

        if movie == movie_an:
            users_who_rated += [email]

    movies = []
    for user_who_rated in users_who_rated:
        ratings = users[user_who_rated]
        if ratings[5]:
            movies += ratings[5]
        elif ratings[4]:
            movies += ratings[4]
        elif ratings[3]:
            movies += ratings[3]
        elif ratings[2]:
            movies += ratings[2]
        else:
            movies += ratings[1]



    return movies


# This is called when you start the script on localhost, and when the
# checker wants to run your functions.
if __name__ == "__main__":
    # This part can be modified at your convenience.
    if len(sys.argv) == 1:
        print("Testing mode")
        db, emails, movies = create_db(20)

        anon_db1 = anonymize_1(db)
        print(get_movies_with_rating(anon_db1, 1))

        anon_db2 = anonymize_2(db)
        print(get_top_rated(anon_db2, movies[0]))

    # If you modify this part, don't complain if it doesn't work anymore!
    # This part is used to communicate with the verification-script. So you
    # should not touch it (unless you're looking for a bug to exploit the
    # verification script - but we didn't plan to put one in there).
    if len(sys.argv) >= 3:
        db_file, ex = sys.argv[1:3]
        with open(db_file) as f:
            db = list(csv.reader(f, skipinitialspace=True))
        # Get nice ints for comparisons
        for i, line in enumerate(db):
            db[i][3] = int(line[3])

        result = []
        if ex == "ex1aa":
            result = anonymize_1(db)
        elif ex == "ex1ag":
            rating = int(sys.argv[3])
            result = [get_movies_with_rating(db, rating)]
        elif ex == "ex1ba":
            result = anonymize_2(db)
        elif ex == "ex1bg":
            movie = sys.argv[3]
            result = [get_top_rated(db, movie)]

        with open("/tmp/student.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(iter(result))
