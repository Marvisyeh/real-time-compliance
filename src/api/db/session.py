import sqlalchemy.orm as orm
from sqlalchemy import create_engine
from api.core.config import DBConfig

engine = create_engine(
    DBConfig.get_db_url(),
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)
Session = orm.sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    db = next(get_db())
    print(db)
