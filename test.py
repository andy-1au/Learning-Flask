from flaskblog import app, db, MyUser, Post

with app.app_context():
    new_user = MyUser(username='Kevin Dotel', email='kd@example.com', password='password')
    db.session.add(new_user)
    db.session.commit()

with app.app_context():
    # Add a new post to the database
    new_post = Post(title='This is Kevin', content='Please work again!', author=new_user)
    db.session.add(new_post)
    db.session.commit()