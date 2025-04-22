from sqlalchemy import create_engine,inspect
from sqlalchemy.orm import sessionmaker
from app.orm.registry import mapper_registry
from app.orm.mapper import start_mappers


                     

def create_database():
    start_mappers()
    engine=create_engine("sqlite:///bujji-bus.db",echo=True)
    
    mapper_registry.metadata.create_all(engine)



    inspector=inspect(engine)
    # print(inspector.get_table_names())


if __name__=="__main__":
    create_database()   