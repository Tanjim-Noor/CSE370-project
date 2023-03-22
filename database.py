from sqlalchemy import create_engine

db_conn = "mysql+pymysql://cux5iveggmqsihc5c3ra:pscale_pw_iNpA4HNutyoQSVlm4nQ84k2FpDLqKWXzXMeMI3WhR8P@370_project/dbname?charset=utf8mb4")

engine = create_engine(db_conn, connect_args={
  "ssl":{
    #insert ssl key here
  }
  
})