from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('name')}:{os.getenv('password')}@{os.getenv('localhost')}:5432/{os.getenv('db_name')}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def is_success_connection():
    try:
        with engine.connect() as connection:
            print("Підключення до бази даних успішне!")
    except Exception as e:
        print(f"Помилка підключення: {e}")


class Base(DeclarativeBase):
    pass


class Status(Base):
    __tablename__ = 'status'

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(unique=True)
    version: Mapped[float] = mapped_column(nullable=False, default=1.0)

    def __repr__(self):
        return f"Status DB: {self.id}\n {self.status}\n{self.version}"


def create_table():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# create_table()
is_success_connection()
