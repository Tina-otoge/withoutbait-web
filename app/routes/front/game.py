import flask
import flask_login
from flask_wtf import FlaskForm
from wtforms import BooleanField, TextAreaField

from app import db
from app.db.models import Game, Review, Tag
from . import bp
from .admin import admin_check
from .delete import DeleteForm


def get_game(slug: str):
    game = db.session.query(Game).filter_by(slug=slug).first()
    if not game:
        flask.abort(404)
    return game


@bp.route('/games/<slug>')
def game(slug: str):
    game = get_game(slug)
    game.views += 1
    db.commit()
    return flask.render_template('game.html', entry=game)

@bp.route('/games/<slug>/delete', methods=['GET', 'POST'])
@flask_login.login_required
def delete_game(slug: str):
    admin_check()

    game = get_game(slug)
    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(game)
        db.session.commit()
        return flask.redirect('/')

    return flask.render_template('delete.html', form=form, entity=game)

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
            BooleanField(tag, description=tag.description, render_kw={'data-icon': tag.icon}),
        )

    form = ReviewForm()

    if not form.validate_on_submit():
        return flask.render_template('review.html', form=form, entry=game)

    review = Review(
        author=flask_login.current_user,
        game=game,
        comment=form.comment.data,
    )
    for tag in tags:
        if not getattr(form, tag.slug.replace('-', '_')).data:
            continue
        review.tags.append(tag)
    db.session.add(review)
    db.session.flush()
    game.update()
    db.commit()
    return flask.redirect(f'/games/{game.slug}')

@bp.route('/games/<slug>/reviews/<int:id>/delete', methods=('GET', 'POST'))
@flask_login.login_required
def delete_review(slug, id):
    admin_check()

    review = db.session.get(Review, id)
    if not review or review.game.slug != slug:
        return flask.redirect('/')

    form = DeleteForm()

    if form.validate_on_submit():
        game = review.game
        db.session.delete(review)
        db.session.flush()
        game.update()
        db.session.commit()
        return flask.redirect(f'/games/{slug}')

    return flask.render_template('delete.html', entity=review, form=form)
