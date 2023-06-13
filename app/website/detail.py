from flask import Blueprint, render_template

detail = Blueprint('detail', __name__)

@detail.route('/detail')
def home():
    return render_template('detail.html')
