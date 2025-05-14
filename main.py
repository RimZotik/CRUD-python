from db import Base, engine
from gui.main_window import create_main_window

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    create_main_window()
