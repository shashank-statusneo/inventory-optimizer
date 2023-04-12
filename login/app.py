from flask import Flask, request, render_template, redirect, url_for
# from flask_restx import api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

db = SQLAlchemy()
username = "sql12612529"
password="TZuKC2mhtc"
host="sql12.freemysqlhosting.net"
port=3306
database="sql12612529"
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{username}:{password}@{host}:{port}/{database}"
db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100))

with app.app_context():
    db.create_all()
    
@app.route("/users", methods=["GET"])
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    print(users)
    return "OK"


@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            username=request.args["username"],
            email=request.args["email"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_detail", id=user.id))

    return render_template("user/create.html")

@app.route("/user/<int:id>")
def user_detail(id):
    user = db.get_or_404(User, id)
    return render_template("user/detail.html", user=user)

@app.route("/user/<int:id>/delete", methods=["GET", "POST"])
def user_delete(id):
    user = db.get_or_404(User, id)

    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("user_list"))

    return render_template("user/delete.html", user=user)

@app.route("/ping", methods=["GET"])
def ping():
    return "hello world"

if __name__ == ("__main__"):
    app.run(debug=True)
    
    