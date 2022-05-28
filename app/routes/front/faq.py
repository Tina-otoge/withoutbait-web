import flask

from . import bp


@bp.route('/faq')
def faq():
    return flask.render_template('faq.html')
