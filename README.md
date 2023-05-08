# Learning-Flask
Just a repository for me to learn the Python Framework, Flask

## I am following the Corey Schafer Tutorial
* [His Channel](https://www.youtube.com/@coreyms)
* [The Playlist I'm Following](https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=1&ab_channel=CoreySchafer)

## Environment Setup and Running through ENVs
* EXPORT FLASK_APP=[name of file]
* EXPORT FLASK_DEBUG=1 --- make changes without restarting the server
* flask run --- run the app
* [NOTE] Environment variable may have to be set again if terminal is closed and re-opened
* When updating bash profile, run source ~/.bash_profile to update it without having to close the terminal 

## Some Things to Remember for FLASK and Python
* {{}} is used when passing in variables
* {} is used for loops, and logical statements
* In case, you get errors creating the db file for SQLAlchemy, run this python code below in terminal in cwd 
* There are empty __init__.py files because its just there to tell python that the folder is a package

``` 
from [project_name] import app, db
app.app_context().push()
db.create_all()
```

## Querying data from db
* [table_name].query...
* .first()
* .filter_by()
* .all()
* .get([by id])

## IN CASE itsdangerous error occurs
* Reference [this link](https://stackoverflow.com/questions/74039971/importerror-cannot-import-name-timedjsonwebsignatureserializer-from-itsdange)