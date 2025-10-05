from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.models import Project, User

db_path = r"..\Backend\db\local_nasa_spaceapps.db"

DATABASE_URL = f"sqlite:///{db_path}"

print("Creating Database...")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

print("DONE! =D")

print("Creating Tables...")

Base.metadata.create_all(bind=engine)

print("DONE! =D")

print("Adding test data")

session = SessionLocal()

try:
    # Primero aseguramos que haya un usuario creador
    creador = User(username="astro_kono", email="astro@leo.dev", role="creator")
    session.add(creador)
    session.commit()

    # Ahora creamos un proyecto asociado a ese usuario
    proyecto = Project(
        name="Orbital Greenhouse",
        description="Estación modular para cultivar plantas en microgravedad.",
        goal_amount=2000000,
        current_amount=175000,
        category="Biotecnología espacial",
        location="LEO",
        orbit_altitude_km=450,
        status="active",
        image_url="https://example.com/greenhouse.jpg",
        video_url="https://youtu.be/abc123",
        tech_summary="Usa LEDs espectrales y control térmico activo.",
        estimated_timeline="Prototipo: 2026, Lanzamiento: 2028",
        risks="Dependencia de transporte orbital y financiamiento adicional",
        tags=["biology", "sustainability", "modular design"],
        backers_count=42,
        launch_date=datetime(2028, 5, 1),
        creator_id=creador.id,
    )

    # Lo guardamos en la base
    session.add(proyecto)
    session.commit()

    print("✅ Proyecto guardado correctamente:", proyecto.name)

except Exception as e:
    session.rollback()
    print("❌ Error al guardar el proyecto:", e)

finally:
    session.close()

print("Done! =D")