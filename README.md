# Learning-Flask
Just a repository for me to learn the Python Framework, Flask

## Environment Setup and Running through ENVs
* EXPORT FLASK_APP=[name of file]
* EXPORT FLASK_DEBUG=1 --- make changes without restarting the server
* flask run --- run the app
* [NOTE] Environment variable may have to be set again if terminal is closed and re-opened


## Some Things to Remember for FLASK
* {{}} is used when passing in variables
* {} is used for loops, and logical statements
* In case, you get errors creating the db file for SQLAlchemy, run this python code below in terminal in cwd 
``` 
from [project_name] import app, db
app.app_context().push()
db.create_all()
```