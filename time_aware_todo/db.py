import mysql.connector as my
def get_connect():
    return my.connect ( host = "localhost",
                        user = "root",
                        password = "ChiragSamaiya",
                        database = "to_do_app"
    )

   

