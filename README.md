# Learning-Flask
Just a repository for me to learn the Python Framework, Flask

## I am following the Corey Schafer Tutorial
[His Channel](https://www.youtube.com/@coreyms)
[The Playlist I'm Following](https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=1&ab_channel=CoreySchafer)

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

## Add data to db
>>> from flaskblog import db, app
>>> from flaskblog.models import MyUser, Post
>>> with app.app_context(): 
...     db.create_all()
...     MyUser.query.all()


```
from [project_name] import [tables] [tables]
```
* Create an instance of a table object
* db.session.add(the_object)
* db.session.commit()

## Querying data from db
* [table_name].query...
* .first()
* .filter_by()
* .all()
* .get([by id])