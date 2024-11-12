from sqlmodel import create_engine, Session, SQLModel

postgres_db = "mino"
postgres_url = f"postgresql://obakeng:12348765@localhost:5432/{postgres_db}"
engine = create_engine(postgres_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
