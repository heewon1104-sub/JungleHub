from flask import Blueprint, render_template, redirect, request
from module.InMemoryCache import inMemoryCacheInstance

bp = Blueprint('main', __name__)

@bp.route("/")
def root():
    return redirect('/main')

@bp.route("/main")
def main():
    
    code = request.args.get('code')
    clientInfo = inMemoryCacheInstance.get(code)
    inMemoryCacheInstance.delete(code)

    if clientInfo is not None: 
        return render_template('main.html', clientInfo=clientInfo)
    else:
        return render_template('main.html')