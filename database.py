import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

db_conn = os.environ['db_uri']

engine = create_engine(db_conn, connect_args={
  "ssl":{
    #insert ssl key here
    "ssl_ca": "/etc/ssl/cert.pem"
  }
})

def load_movies():
  with engine.connect() as conn:
    movies = conn.execute(text("select * from movies"))
    #movies_dic= []
  
    movies_list = [dict(zip(movies.keys(), row)) for row in movies.fetchall()]
    return movies_list
    
    
  #print(movies_dic)

def insert_user_info(username, email, password):
    with engine.connect() as conn:
        try:
            conn.execute(text("INSERT INTO user_info (username, email, password)  VALUES (:username, :email, :password)"), {"username": username,"email": email, "password": password})
            return True
        except IntegrityError:
            return False

def get_user_by_email(email):
    with engine.connect() as conn:
        #query = text("SELECT * FROM user_info WHERE email = :email")
        result = conn.execute(text("SELECT * FROM user_info WHERE email = :email"), {"email":email})

        result_list = [dict(zip(result.keys(), row)) for row in result.fetchall()]
        f_result = result_list[0]
        #print("DICTIONARY RESULT @#@@@##@##@##@#", result_list)

        if f_result:
          return f_result

        else:
          return False
        
