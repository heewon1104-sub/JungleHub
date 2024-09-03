from flask import Blueprint, render_template, redirect, session

bp = Blueprint('main', __name__)

@bp.route("/")
def root():
    return redirect('/main')

@bp.route("/main")
def main():
    clientInfo = session.get('clientInfo')
    return render_template('main.html', clientInfo = clientInfo)