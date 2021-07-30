from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EpisodeForm, EditEpisodeForm
from flask_login import current_user, login_user, logout_user,login_required
from app.models import User, Episode
from datetime import datetime
from flask import jsonify
from flask_cors import cross_origin



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
        episodes = Episode.query.order_by(Episode.timestamp.desc()).all()
        ep_list = []
        for episode in episodes:
            new_ep = {
                'title': episode.title,
                'plot': episode.plot,
                'writer': episode.writer.username
            }
            ep_list.append(new_ep)
        return jsonify(ep_list)