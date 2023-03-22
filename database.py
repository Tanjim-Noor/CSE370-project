from sqlalchemy import create_engine, text

db_conn = "mysql+pymysql://cux5iveggmqsihc5c3ra:pscale_pw_iNpA4HNutyoQSVlm4nQ84k2FpDLqKWXzXMeMI3WhR8P@ap-southeast.connect.psdb.cloud/theatre_movies?charset=utf8mb4"

engine = create_engine(db_conn, connect_args={
  "ssl":{
    #insert ssl key here
    "ssl_ca": "/etc/ssl/cert.pem"
  }
})

with engine.connect() as conn:
  movies = conn.execute(text("select * from movies"))
  movies_dic= []

  movies_list = [dict(zip(movies.keys(), row)) for row in movies.fetchall()]
  print(movies_list)
    
  #print(movies_dic)

