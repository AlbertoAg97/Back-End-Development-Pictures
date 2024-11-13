from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data)
    
    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):

    if not id:
        return {"message": "Invalid input, no data provided"}, 400

    for pic in data:
        if pic["id"] == int(id):
            return pic

    return {"message": "Not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.get_json()

    if not new_picture:
       return {"message": "Invalid input, no data provided"}, 400

    id = int(new_picture["id"])

    for pic in data:
        if pic["id"] == id:
            return {"Message": f"picture with id {id} already present"}, 302

    data.append(new_picture)

    return new_picture, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_picture = request.get_json()

    if not new_picture:
       return {"message": "Invalid input, no data provided"}, 400

    id = int(new_picture["id"])

    i = 0
    for pic in data:
        if pic["id"] == id:
            data.remove(pic)
            data.append(new_picture)
            return new_picture, 201
    i+=1

    data.append(new_picture)

    return {"message": "Not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):

    if not id:
        return {"message": "Invalid input, no data provided"}, 400

    for pic in data:
        if pic["id"] == int(id):
            data.remove(pic)
            return jsonify(), 204

    return {"message": "Not found"}, 404
