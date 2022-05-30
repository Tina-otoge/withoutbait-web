import flask

from . import bp


@bp.route('/')
def tools():
    return flask.render_template('admin/tools_list.html')
