from app import app, db
from flask import flash, redirect, url_for, request, jsonify
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EpisodeForm, EditEpisodeForm
from flask_login import current_user, login_user, logout_user, login_required, login_manager
from app.models import User, Episode
from datetime import datetime
from flask_cors import CORS, cross_origin


@app.route('/')
@app.route('/index')
def index():
    if (current_user.is_authenticated):
        return {"username": current_user.username, "user_id": current_user.id}
    else:
        return {"message": "welcome"}
    

@app.route('/episodes', methods=['GET', 'POST'])
def episodes():
    if request.method == 'GET':
        episodes = Episode.query.order_by(Episode.timestamp.desc()).all()
        ep_list = []
        for episode in episodes:
            new_ep = {
                'title': episode.title,
                'plot': episode.plot,
                'writer': episode.writer.username,
                'writer_id': episode.writer.id,
                'episode_id': episode.id
            }
            ep_list.append(new_ep)
        if current_user.is_authenticated:
            return {
                "current_user": current_user.username,
                "user_id": current_user.user_id,
                "episodes": ep_list
            }
        else:
            return {
                "episodes": ep_list
            }
    elif request.method == 'POST':
        print("Request received. Processing...")
        req = request.get_json()
        print(req['title'])
        ep = Episode(title=req['title'], plot=req['plot'], user_id=req['user_id'])
        db.session.add(ep)
        db.session.commit()
        print("Episode Added")
    return redirect(url_for('episodes'))


@app.route('/episodes/<int:id>/delete')
def delete_episode(id):
    print('HERE I AM DELETING>>>')
    episode = Episode.query.filter_by(id=id).first()
    db.session.delete(episode)
    db.session.commit()
    return redirect(url_for('episodes'))


@app.route('/episodes/<int:id>/update', methods=['POST'])
def update_episode(id):
    print('HERE I AM UPDATING>>>')
    print("Request received. Processing...")
    # episode = Episode.query.get(id)
    req = request.get_json()
    print(req)
    # episode.title = req.title
    # episode.plot = req.plot
    # db.session.commit()
    # print("Episode Added")
    return redirect(url_for('episodes'))


@app.route('/writers')
def writers():
    episodes = Episode.query.all()
    writers_list = []
    for episode in episodes:
        new_writer = {
            'username': episode.writer.username,
            'writer_id': episode.writer.id,
        }
        if new_writer not in writers_list:
            writers_list.append(new_writer)
    return {
        "writers": writers_list
        }

    
#########################################################################
#  USER REGISTRATION/LOGIN/LOGOUT amd WRITERS
#########################################################################
@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # form = LoginForm(meta={'csrf': True})
    form = LoginForm(meta={'csrf': False})
    data = request.json
    print("Data 1:", data)
    if form.validate_on_submit():
        print("I'm inside the validation function")
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if user is None or not user.check_password(form.password.data):
            hash = user.password_hash
            print(hash)
            print("That's an invalid username or password!!!!!")
            return 'try entering your information again'
        login_user(user, remember=form.remember_me.data)
        print("current_user:", current_user.username)
        return {"message": "logged in", "username":  current_user.username, "user_id": current_user.id }
    print('please submit your information again')
    return {"message": "try again"}
    


@app.route('/logout')
def logout():
    logout_user()
    return {"username": "", "user_id": ""}


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return {"data": "you are registered AND logged in. Go to the index."}
    form = RegistrationForm(meta={'csrf': False} )
    data = request.json
    print("Data 1:", data)
    print("Form:", form.data)
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        print('This is the password being hashed:',form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        print('congratulations!! you are now a registered user!!!!')
        return {"data": "you are registered. now, go login"}
    return {"data": "please check your information and try again"}