import mariadb
import csv
import sys
import os

if __name__ == "__main__":
    
    try:
        conn = mariadb.connect(
            user="root",
            password= os.environ["ROOTPWD"],
            host="localhost",
            port=3306,
            database="products"
        )
    
    except mariadb.Error as e:
        sys.exit(1)
    
    cur = conn.cursor()

    cur.execute(

        "DROP TABLE items;"

    )

    cur.execute(

        "CREATE TABLE items(p_id int not null,"
                            "title varchar(800)," 
                            "rating numeric(5,1),"
                            "price numeric(8,2),"
                            "available varchar(200),"
                            "review_count int,"
                            "description varchar(5000),"
                            "category varchar(200),"
                            "primary key (p_id)"
                            ");"
    )

    with open('cleaned.csv', mode='r', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t",escapechar="\\", quoting=csv.QUOTE_NONE)
        next(csv_reader)
        for line in csv_reader:
            
            cur.execute(

                "INSERT INTO items(p_id,title,rating,price,available,review_count,description,category) VALUES (?,?,?,?,?,?,?,?);",
                (line[7],line[0],line[1],line[2],line[3],line[4],line[5],line[6])
            )
    
    conn.commit()

    conn.close()