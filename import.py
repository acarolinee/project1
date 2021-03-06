import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Set up database
engine = create_engine("postgres://vhxpyztttqopeq:d9f88853016924d9a7e9c30990a5c3d1ea59afafd6b31d33e3db56bbc2afdfbc@ec2-50-17-227-28.compute-1.amazonaws.com:5432/d7pcko0iplvkj8", echo=True)
db = scoped_session(sessionmaker(bind=engine))

def main():

    with open('books.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        first_row = next(spamreader)

        autores = []

        for row in spamreader:
            if row[2] not in autores:
                autores.append(row[2])

        print("Guardando autores...")

        for autor in autores:
            db.execute("INSERT INTO autor (name) VALUES (:name)", {"name": autor})

        print("Fin guardado de autores")

        csvfile.seek(0)
        first_row = next(spamreader)

        print("Guardando libros y autores asociados...")

        for row in spamreader:
            isbn = row[0]
            title = row[1]
            autor = row[2]
            year = row[3]

            autor_row = db.execute("SELECT id from autor where name = :name", {"name": autor}).fetchone()
            db.execute("INSERT INTO libro (isbn, title, autor_id, year) VALUES (:isbn, :title, :autor_id, :year)", {"isbn": isbn, "title": title, "autor_id": autor_row["id"], "year": year})

        print("Fin guardado de libros y autores asociados")

        db.commit()

if __name__ == "__main__":
    main()
