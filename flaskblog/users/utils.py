import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

# SAVE PICTURE FUNCTION ------------------------------------------------------
def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # creating a random hex for the name of the picture file
    _, f_ext = os.path.splitext(form_picture.filename) # split the file name and the extension
    picture_fn = random_hex + f_ext # concatenate the random hex and the extension
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn) 
    
    output_size = (125, 125) # resize the image to 125x125, save time and storage
    i = Image.open(form_picture) 
    i.thumbnail(output_size) # resize the image
    i.save(picture_path) 
    
    return picture_fn
# ----------------------------------------------------------------------------

# SEND RESET EMAIL FUNCTION --------------------------------------------------
def send_reset_email(user):
    token = user.get_reset_token() # get the token from the user object
    msg = Message('Password Reset Request', 
                  sender='blogreset101@gmail.com',
                  recipients=[user.email]) # send the email to the user's email
    
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)} 

If you did not make this request then simply ignore this email and no changes will be made.
''' # triple quotes allows us to write multiple lines, _external=True allows us to get the absolute url instead of the relative url
    mail.send(msg) # send the message
#-----------------------------------------------------------------------------