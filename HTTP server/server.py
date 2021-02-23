from flask import Flask, request, abort
from Models.end_user import EndUser

users_list = []

app = Flask(__name__)
app.run(host="0.0.0.0")


@app.route("/Create", methods=["POST"])
def create_room():
    users_list.append(
        EndUser(
            name=request.form["name"],
            ip=request.remote_addr,
            chat_port=request.form["chat_port"],
            voice_port=request.form["voice_port"],
            host=True,
        )
    )
    return "Added to database"


@app.route("/Seek", methods=["POST"])
def seek_user():
    for user in users_list:
        if user.name == request.form["name"]:
            return vars(user)
    abort(404)
