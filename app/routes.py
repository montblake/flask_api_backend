from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EpisodeForm, EditEpisodeForm
from flask_login import current_user, login_user, logout_user,login_required
from app.models import User, Episode
from datetime import datetime
from flask import jsonify
from flask_cors import cross_origin

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

# Root Route
@app.route('/')
@app.route('/index')
def index():
    return {
        "text": "stuff and nonsense. And then, more stuff.",
        "author": "Stuffy McStufferson"
    }


@app.route('/episodes', methods=['GET', 'POST'])
@cross_origin()
def episodes():
    if request.method == 'GET':
        episodes = Episode.query.order_by(Episode.timestamp.desc()).all()
        ep_list = []
        for episode in episodes:
            new_ep = {
                'title': episode.title,
                'plot': episode.plot,
                'writer': episode.writer.username,
                'episode_id': episode.id
            }
            ep_list.append(new_ep)
        return jsonify(ep_list)
    elif request.method == 'POST':
        print("Request received. Processing...")
        req = request.get_json()
        print(req['title'])
        ep = Episode(title=req['title'], plot=req['plot'], user_id=req['user_id'])
        db.session.add(ep)
        db.session.commit()
        print("Episode Added")
    return redirect(url_for('episodes'))

# @app.route('/episodes/<id>', methods=['DELETE'])
# def episode_delete(id):
#     episode = Episode.query.get(id)
#     db.session.delete(episode)
#     db.session.commit()
#     return redirect(url_for('episodes'))

@app.route('/episodes/<int:id>/delete')
# @cross_origin
def delete_episode(id):
    print('HERE I AM DELETING>>>')
    episode = Episode.query.filter_by(id=id).first()
    db.session.delete(episode)
    db.session.commit()
    return redirect(url_for('episodes'))