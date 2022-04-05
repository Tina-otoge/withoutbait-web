import flask
import flask_login
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired

from app import db
from app.db.models import Game, Review, Tag
from . import bp


def get_game(slug: str):
    game = db.session.query(Game).filter_by(slug=slug).first()
    if not game:
        flask.abort(404)
    return game


@bp.route('/games/<slug>')
def game(slug: str):
    game = get_game(slug)
    game.views += 1
    db.session.commit()
    return flask.render_template('game.html', entry=game)

@bp.route('/games/<slug>/review', methods=('GET', 'POST'))
@flask_login.login_required
def add_game_review(slug: str):
    game = get_game(slug)
    tags = db.session.query(Tag)

    class ReviewForm(FlaskForm):
        comment = TextAreaField()
    for tag in tags:
        setattr(
            ReviewForm,
            tag.slug.replace('-', '_'),
            BooleanField(tag, description=tag.description),
        )

    form = ReviewForm()

    if not form.validate_on_submit():
        return flask.render_template('review.html', form=form, entry=game)

    review = Review(
        author=flask_login.current_user,
        game=game,
        comment=form.comment.data,
    )
    db.session.add(review)
    db.session.commit()
    return flask.redirect(f'/games/{game.slug}')

@bp.route('/add', methods=('GET', 'POST'))
@flask_login.login_required
def add_game():
    class AddGameForm(FlaskForm):
        is_slug_from_igdb = BooleanField()
        slug = StringField()
        name = StringField(validators=[DataRequired()])
        subtitle = StringField()
        official_url = StringField()
        cover_url = StringField()

    form = AddGameForm()

    if not form.validate_on_submit():
        return flask.render_template('add_game.html', form=form)

    slug = form.slug.data or Game.slugify(form.name.data)
    game = db.session.query(Game).filter_by(slug=slug).first()
    if game:
        raise Exception(f'Game with slug {slug} already exists')
    game = Game(
        slug=slug,
        is_slug_from_igdb=form.is_slug_from_igdb.data,
        name=form.name.data,
        subtitle=form.subtitle.data,
        official_url=form.official_url.data,
        cover_url=form.cover_url.data,
    )
    db.session.add(game)
    db.session.commit()
    return flask.redirect(f'/games/{slug}')
