from backend import app
from backend.utils import check_argument, form_argument, query_argument, check_permission
from backend.model import get_db, jsonify, db_get_user_groups

from gridfs import GridFS
import hashlib
import os
from flask import session, send_file, make_response
from bson import ObjectId
from mimetypes import guess_type

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}


def allowed_file(file_extension):
    return file_extension[0] == '.' and file_extension[1:] in ALLOWED_EXTENSIONS


@app.route('/group/create', methods=['POST'])
@check_permission
@form_argument
@check_argument("avatar")
@check_argument("name")
def create_group(avatar, name):
    db = get_db()
    fs = GridFS(db, collection="images")
    filename, file_extension = os.path.splitext(avatar.filename)
    if not allowed_file(file_extension):
        return 'Image type is wrong!'
    data = avatar.read()
    sha1 = hashlib.sha1(data).hexdigest()
    filename = sha1 + file_extension
    image_obj = fs.find_one({"filename": filename})
    if not image_obj:
        image_obj = fs.put(data, filename=filename, content_type=avatar.content_type)
    else:
        image_obj = image_obj._id
    print(image_obj)
    gid = db.groups.insert({
        'name': name,
        'avatar': image_obj,
    })
    db.group_user.insert({
        'uid': session['uid'],
        'gid': gid,
    })
    return 'ok'


@app.route('/group/avatar/<string:object_id>')
def get_group_avatar(object_id):
    db = get_db()
    fs = GridFS(db, collection="images")
    image_obj = fs.find_one({"_id": ObjectId(object_id)})
    print(image_obj.content_type)
    response = make_response(image_obj.read())
    content_type = image_obj.content_type
    if not content_type:
        content_type, _ = guess_type(image_obj.filename)
    response.mimetype = content_type
    return response

