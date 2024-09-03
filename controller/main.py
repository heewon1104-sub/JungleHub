from flask import Blueprint, render_template, redirect

bp = Blueprint('main', __name__)

@bp.route("/")
def root():
    return redirect('/main')

@bp.route("/main")
def main():
    return render_template('main.html')