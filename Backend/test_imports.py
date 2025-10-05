import sys
sys.path.append(r'C:\Users\samue\Documents\DEV\UDEM-NASA-SPACE-APPS-MORDECAI-Y-LOS-RIGBIES\Backend')
try:
    import app.database as db
    import app.models.project as mp
    import app.models.user as mu
    import app.controllers.projects_controller as pc
    print('IMPORTS_OK')
except Exception as e:
    print('IMPORT_ERROR', e)