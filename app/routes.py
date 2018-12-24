#
# Routes module
#
import os
import operator

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from app import app, db
from app.models import User
from app.forms import LoginForm, RegistrationForm, IndexForm
from app.pillow_magic import create_thumbnail, mouth_magic, eyes_magic
from app.User_Class import UserFace
from app.face_detect import detect_face

face_user = UserFace()

temp_file_url = ''
current_image_url = ''

@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
@login_required
def index():
    global temp_file_url
    global face_user
    form = IndexForm()

    if form.validate_on_submit() and form.submit.data:
        return redirect(url_for('add_mouth_effect'))

    if form.validate_on_submit() and form.submit_eyes.data:
        return redirect(url_for('add_eyes_effect'))

    if form.validate_on_submit() and form.default.data:
        return redirect(url_for('default'))

    temp_file_url = temp_file_url.replace('app/', '')
    phrase = welcome_phrase(face_user.mood)
    return render_template('index.html', title='Home',
                           image=temp_file_url, form=form, welcome_phrase = phrase)

@app.route('/add_mouth_effect',methods=['GET', 'POST'])
def add_mouth_effect():
    global temp_file_url
    global current_image_url
    global face_user
    print(current_image_url)
    print(temp_file_url)
    temp_file_url = current_image_url
    temp_file_url = mouth_magic(temp_file_url, face_user.face_coordinates)
    return redirect(url_for('index'))

@app.route('/add_eyes_effect',methods=['GET', 'POST'])
def add_eyes_effect():
    global temp_file_url
    global current_image_url
    global face_user
    temp_file_url = current_image_url
    temp_file_url = eyes_magic(temp_file_url, face_user.face_coordinates)
    return redirect(url_for('index'))

@app.route('/default',methods=['GET', 'POST'])
def default():
    global temp_file_url
    global current_image_url
    temp_file_url = current_image_url
    temp_file_url = temp_file_url.replace('moustache', 'temp')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login User
    :return:
    """
    global face_user

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        f = form.image.data
        filename = secure_filename(f.filename)
        user_directory = os.path.join(app.config['UPLOAD_FOLDER'], form.username.data) + '/'
        if filename.find('png') != -1:
            filename = form.username.data + '_temp.png'
        if filename.find('jpg') != -1:
            filename = form.username.data + '_temp.jpg'
        f.save(user_directory + filename)
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data) or \
                not user.check_photo(detect_face(os.path.join(user_directory + filename))):
            flash('Invalid username or password or photo')
            if os.path.isfile(os.path.join(user_directory + filename)):
                os.remove(os.path.join(user_directory + filename))
            return redirect(url_for('login'))
        login_user(user, remember=False)

        file_png = user_directory + current_user.username + '_temp.png'
        file_jpg = user_directory + current_user.username + '_temp.jpg'
        if os.path.isfile(file_png):
            image = create_thumbnail(file_png)
        elif os.path.isfile(file_jpg):
            image = create_thumbnail(file_jpg)
        else:
            image = ' '
        face_info = detect_face(os.path.join(user_directory + filename),
                                True,
                                True,
                                )
        face_user.parse_user_info(face_info)
        global temp_file_url
        global current_image_url
        current_image_url = temp_file_url = image
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registr User
    :return:
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user_directory = os.path.join(app.config['UPLOAD_FOLDER'], form.username.data) + '/'
        os.makedirs(new_user_directory)
        f = form.image.data
        filename = secure_filename(f.filename)
        if filename.find('png') != -1 :
            print('found')
            filename = form.username.data + '_avatar.png'
        if filename.find('jpg') != -1 :
            print(filename)
            filename = form.username.data + '_avatar.jpg'


        f.save(new_user_directory + filename)
        user = User(username=form.username.data, email=form.email.data,
                    photo_id=os.path.join(new_user_directory + filename))
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    """
    Logout User
    :return:
    """
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], current_user.username) + '/'
    file_png = user_folder + current_user.username + '_temp.png'
    file_jpg = user_folder + current_user.username + '_temp.jpg'


    file_moustache_png = user_folder + current_user.username + '_moustache.png'
    file_moustache_jpg = user_folder + current_user.username + '_moustache.jpg'


    file_glasses_png = user_folder + current_user.username + '_glasses.png'
    file_glasses_jpg = user_folder + current_user.username + '_glasses.jpg'

    if os.path.isfile(file_png):
        os.remove(file_png)
    elif os.path.isfile(file_jpg):
        os.remove(file_jpg)

    if os.path.isfile(file_moustache_png):
        os.remove(file_moustache_png)
    elif os.path.isfile(file_moustache_jpg):
        os.remove(file_moustache_jpg)

    if os.path.isfile(file_glasses_png):
        os.remove(file_glasses_png)
    elif os.path.isfile(file_glasses_jpg):
        os.remove(file_glasses_jpg)

    logout_user()
    return redirect(url_for('index'))


def welcome_phrase(mood_dict):
    print(mood_dict)

    phrase = ''
    emotion = max(mood_dict, key=mood_dict.get)
    if emotion == 'neutral':
        phrase = 'You are so cold today...'
    if emotion == 'anger':
        phrase = 'Why are you so angry?'
    if emotion == 'fear':
        phrase = 'What are you afraid of?'
    if emotion == 'happiness':
        phrase = 'Oh, you are so happy today.'
    if emotion == 'sadness':
        phrase == 'Why are you so sad?'
    if emotion == 'surprise':
        phrase == 'You are so surprised.'
    return phrase
