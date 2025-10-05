import os

from .controllers.database.database_controller import create_db


def init_db():
    db_path = r'..\Backend\db\local_nasa_spaceapps.db'
    if os.path.exists(db_path):
        return {"message": "la base de datos ya existe"}
    else:
        create_db()
        return {"message": "Se creará una nueva base de datos"}