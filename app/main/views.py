from flask import render_template

# import the main blue print instance
from app.main import main


@main.route('/')
def index():
    return render_template('index.html')
