from flask import Blueprint, render_template, url_for

home_route = Blueprint('home', __name__)


@home_route.get("/")
async def get_home():

    social_url = url_for('home.get_home', _external=True)
    context = dict(social_url=social_url)
    return render_template('index.html', **context)
