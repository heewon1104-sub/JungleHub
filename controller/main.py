from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route("/main")
def main():
    return render_template('main.html')

