import json
from flask import Flask, request
from db import db, User
import random
import game_helper
import utils


app = Flask(__name__)
db_filename = 'assassins.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()
    utils.set_logger('game_log')


def name_exists(n):
    name_list = User.query.filter_by(name=n).all()
    return bool(name_list)


@app.route('/')
def root():
    return json.dumps({'success': True, 'data': "Who's ready to play?"})


@app.route('/api/user/create/', methods=['POST'])
def create_user():
    post_body = json.loads(request.data)
    name = post_body.get('name')
    if name_exists(name):
        return json.dumps({'success': False, 'data': 'That name is already taken.'})
    new_user = User(
        name=name
    )
    db.session.add(new_user)
    db.session.commit()
    return json.dumps({'success': True, 'data': new_user.serialize()})


@app.route('/api/user/login/', methods=['POST'])
def login_user():
    post_body = json.loads(request.data)
    name = post_body.get('name')
    exists = False
    if name_exists(name):
        exists = True
    return json.dumps({'success': exists})


@app.route('/api/users/all/', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return json.dumps({
        'success': True,
        'num_results': len(users),
        'data': [u.serialize() for u in users]
        })


@app.route('/api/users/delete/all/', methods=['DELETE'])
def delete_all_users():
    n = User.query.delete()
    db.session.commit()
    return json.dumps({'success': True, 'num_deleted': n})


@app.route('/api/users/assign_targets/all/', methods=['GET'])
def assign_targets_all():
    users = User.query.all()
    ids = [u.id for u in users]
    random.shuffle(ids)
    for u, i in zip(users, ids):
        u.target = i

    return json.dumps({'success': True, 'data': [u.serialize() for u in users]})


@app.route('/api/submit/photo/', methods=['POST'])
def recieve_photo():
    post_body = json.loads(request.data)
    img_string = post_body.get('photo')
    img = game_helper.convert_image(img_string)
    # img = base64.decodebytes(img_string)
    target_found = game_helper.classify_img(img, "TODO")
    utils.log(str(target_found))
    return json.dumps({'success': target_found})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
