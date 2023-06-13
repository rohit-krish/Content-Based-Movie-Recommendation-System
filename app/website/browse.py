from flask import Blueprint, redirect, render_template

browse = Blueprint('browse', __name__)

popular_50 = [
    91314, 8869, 19995, 411, 102382, 296096, 671, 168259, 1858, 672, 557, 673, 674, 157336, 767, 68718, 1930, 76203, 597, 675, 585, 24428, 216015, 808, 238,
    232672, 198663, 862, 559, 1865, 14836, 8587, 22803, 38757, 2062, 106, 50014, 106646, 293660, 118340, 809, 22, 14160, 37165, 285, 99861, 425, 177572, 18785, 10198
]


@browse.route('/')
def reroute():
    return redirect('/browse')


@browse.route('/browse')
def home():
    return render_template('browse.html', genres=['Animation', 'Adventure', 'Family', 'Comedy'])
