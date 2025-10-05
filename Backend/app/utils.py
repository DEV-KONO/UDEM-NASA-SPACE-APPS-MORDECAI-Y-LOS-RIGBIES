import os

def init_db():
    db_path = r'..\Backend\db\local_nasa_spaceapps.db'
    if os.path.exists(db_path):
        return {"message": "la base de datos ya existe"}
    else:
        with open(db_path, "w") as f:
            pass
        return {"message": "Se creará una nueva base de datos"}