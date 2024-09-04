from flask import Blueprint, render_template

bp = Blueprint('commit', __name__)

@bp.route('/commit')
def login():
    return 'hello'