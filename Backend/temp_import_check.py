import sys
sys.path.append(r'C:\Users\samue\Documents\DEV\UDEM-NASA-SPACE-APPS-MORDECAI-Y-LOS-RIGBIES\Backend')
modules = [
    'app.api.v1.routes.projects',
    'app.schemas.project',
    'app.controllers.pledge_controller',
    'app.controllers.project_update_controller'
]
for m in modules:
    try:
        __import__(m)
        print(m, 'OK')
    except Exception as e:
        print(m, 'IMPORT_ERROR', e)
