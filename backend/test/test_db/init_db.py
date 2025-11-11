from infra.db import Base, engine
from infra.posts import PostORM

def init_db():
    Base.metadata.create_all(bind=engine)


