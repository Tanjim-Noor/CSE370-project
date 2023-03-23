import os
from sqlalchemy import create_engine, text

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
    movies_dic= []
  
    movies_list = [dict(zip(movies.keys(), row)) for row in movies.fetchall()]
    return movies_list
    
    
  #print(movies_dic)

