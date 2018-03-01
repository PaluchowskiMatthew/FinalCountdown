#!/usr/bin/env python3
import datetime, sys, csv
from random import randrange, randint
import random, string
import os
import pickle
# import numpy as np
# import pandas as pd
import hashlib
import crypt

date_start = datetime.date(2000, 1, 1)
date_period = 365 * 17

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
    email_hashes = {}
    movie_hashes = {}
    rating_hashes = {}

    db_salt = randomword(8)

    for i, line in enumerate(db):
        email = line[0]
        movie = line[1]
        date = line[2]
        rating = line[3]

        if email not in email_hashes:
            salted_entry = str(email) + crypt.mksalt(crypt.METHOD_SHA256)
            entry_bytes = str.encode(salted_entry)
            email_hashes[email] = hashlib.sha256(entry_bytes).hexdigest()
        db[i][0] = email_hashes[email]

        if movie not in movie_hashes:
            salted_entry = str(movie) + crypt.mksalt(crypt.METHOD_SHA256)
            entry_bytes = str.encode(salted_entry)
            movie_hashes[movie] = hashlib.sha256(entry_bytes).hexdigest()
        db[i][1] = movie_hashes[movie]

        if rating not in rating_hashes:
            salted_entry = str(rating) + crypt.mksalt(crypt.METHOD_SHA256)
            entry_bytes = str.encode(salted_entry)
            rating_hashes[rating] = hashlib.sha256(entry_bytes).hexdigest()
        db[i][3] = rating_hashes[rating]

    save_obj(email_hashes, 'email_hashes' + db_salt)
    save_obj(movie_hashes, 'movie_hashes' + db_salt)
    save_obj(rating_hashes, 'rating_hashes' + db_salt)
    save_obj(db, 'anon_db' + db_salt)

    return db


# For a given anonymized-database and a rating, this function should return
# the films with the given rating.
def get_movies_with_rating(anon, rating):
    db_salt = ''
    for filename in os.listdir():
        if 'anon_db' in filename:
            loaded_anon = load_obj('' + filename[:-4])

            no_ext = filename[:-4]
            current_salt = no_ext[7:]

            loaded_email_hashes = load_obj('email_hashes' + current_salt)

            name_paintext = anon[0][0]
            name_hashed = loaded_anon[0][0]

            if name_paintext in loaded_email_hashes and (loaded_email_hashes[name_paintext] == name_hashed):
                db_salt = current_salt

    loaded_rating_hashes = load_obj('rating_hashes' + db_salt)
    loaded_movie_hashes = load_obj('movie_hashes' + db_salt)

    loaded_rating_hashes_inv = {v: k for k, v in loaded_rating_hashes.items()}
    loaded_movie_hashes_inv = {v: k for k, v in loaded_movie_hashes.items()}

    movies = []
    for i, line in enumerate(anon):
        # print(line)
        email_hash = line[0]
        movie_hash = line[1]
        date_hash = line[2]
        rating_hash = line[3]

        if movie_hash in loaded_movie_hashes_inv:
            movie_deanon = loaded_movie_hashes_inv[movie_hash]
        elif movie_hash in loaded_movie_hashes:
            movie_deanon = movie_hash

        if rating_hash in loaded_rating_hashes_inv:
            rating_deanon = loaded_rating_hashes_inv[rating_hash]
        elif rating_hash in loaded_rating_hashes:
            rating_deanon = rating_hash

        if rating == rating_deanon:
            movies += [movie_deanon]

    return list(set(movies))


# A bit lesser anonymization than anonymize_1, but still no date. The returned
# database should have enough information to be used by get_top_rated. If you
# use a too simple hashing-function like sha-256, the result will be rejected.
def anonymize_2(db):
    return db


# get_top_rated searches for all users having rated a movie and searches their
# top-rated movie(s). It returns a list of all found movies, also doubles!
def get_top_rated(anon, movie):
    return [anon[0][1]]


##### HELPER METHODS
def hash_list(unique_list):
    hashes_dict = {}
    for entry in unique_list:
        salted_entry = str(entry) + crypt.mksalt(crypt.METHOD_SHA256)
        entry_bytes = str.encode(salted_entry)
        hashes_dict[entry] = hashlib.sha256(entry_bytes).hexdigest()
    return hashes_dict

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def randomword(length):
   return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

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
