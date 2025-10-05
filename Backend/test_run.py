import sys
from pathlib import Path
# Ensure Backend is on path
sys.path.append(r'C:\Users\samue\Documents\DEV\UDEM-NASA-SPACE-APPS-MORDECAI-Y-LOS-RIGBIES\Backend')

from app.database import Base, engine, SessionLocal
from app.models.user import User
from app.models.project import Project
from datetime import datetime

# Create DB tables
Base.metadata.create_all(bind=engine)

# Quick CRUD smoke test
db = SessionLocal()
try:
    # ensure a user exists
    user = db.query(User).filter(User.username == 'test_user').first()
    if not user:
        user = User(username='test_user', email='test@example.com', role='creator')
        db.add(user)
        db.commit()
        db.refresh(user)
        print('USER_CREATED', user.id, user.username)
    else:
        print('USER_EXISTS', user.id, user.username)

    # create a project
    proj = Project(name='Test LEO Project', description='A test project in LEO', goal_amount=50000.0, creator_id=user.id)
    db.add(proj)
    db.commit()
    db.refresh(proj)
    print('PROJECT_CREATED', proj.id, proj.name)

    # list projects
    projects = db.query(Project).all()
    print('TOTAL_PROJECTS', len(projects))
    for p in projects:
        print('P:', p.id, p.name, p.creator_id)

finally:
    db.close()

print('SMOKE_TEST_DONE')
