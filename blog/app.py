from flask import Flask, request, g, render_template
from time import time
from werkzeug.exceptions import BadRequest
from blog.views.users import users_app
from blog.views.articles import articles_app
from blog.models.database import db
from blog.views.auth import login_manager, auth_app
import os
from flask_migrate import Migrate
from blog.models import User
from blog.security import flask_bcrypt
from blog.views.authors import authors_app
from blog.models import Tag

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/greet/<name>/")
def greet_name(name: str):
    return f"Hello {name}!"

@app.route("/user/")
def read_user():
    name = request.args.get("name")
    surname = request.args.get("surname")
    return f"User {name or '[no name]'} {surname or '[no surname]'}"

@app.route("/status/", methods=["GET", "POST"])
def custom_status_code():
    if request.method == "GET":
        return """\
        To get response with custom status code send request using POST method
        and pass `code` in JSON body / FormData """

    print("raw bytes data:", request.data)
    if request.form and "code" in request.form:
        return "code from form", request.form["code"]

    if request.json and "code" in request.json:
        return "code from json", request.json["code"]

    return "", 204


@app.before_request
def process_before_request():
    """
    Sets start_time to `g` object """
    g.start_time = time()


@app.after_request
def process_after_request(response):
    """
    adds process time in headers """
    if hasattr(g, "start_time"):
        response.headers["process-time"] = time() - g.start_time

    return response

@app.route("/power/")
def power_value():
    x = request.args.get("x") or ""
    y = request.args.get("y") or ""
    if not (x.isdigit() and y.isdigit()):
        app.logger.info("invalid values for power: x=%r and y=%r", x, y)

        raise BadRequest("please pass integers in `x` and `y` query params")
    x = int(x)
    y = int(y)
    result = x ** y
    app.logger.debug("%s ** %s = %s", x, y, result)
    return str(result)


@app.route("/divide-by-zero/")
def do_zero_division():
    return 1 / 0


@app.errorhandler(ZeroDivisionError)
def handle_zero_division_error(error):
    print(error) # prints str version of error: 'division by zero'
    app.logger.exception("Here's traceback for zero division error")
    return "Never divide by zero!", 400

app.register_blueprint(users_app, url_prefix="/users")

app.register_blueprint(articles_app, url_prefix="/articles")

app.config["SECRET_KEY"] = "abcdefg123456"
app.register_blueprint(auth_app, url_prefix="/auth")
login_manager.init_app(app)
flask_bcrypt.init_app(app)
app.register_blueprint(authors_app, url_prefix="/authors")

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user:password@localhost:5432/blog"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
cfg_name = os.environ.get("CONFIG_NAME") or "ProductionConfig"
# app.config.from_object(f"blog.configs.{cfg_name}")
migrate = Migrate(app, db)
# app.register_blueprint(db)


# @app.cli.command("init-db")
# def init_db():
#     """
#     Run in your terminal: flask init-db
#     """
#     db.create_all()
#     print("done!")


@app.cli.command("create-admin")
def create_admin():
    """
    Run in your terminal:
    ➜ flask create-admin
    > created admin: <User #1 'admin'> """
    admin = User(username="admin", is_staff=True)
    admin.username = "admin"
    admin.is_staff = True
    # james = User()
    # james.username = "james"
    admin.password = os.environ.get("ADMIN_PASSWORD") or "adminpass"
    db.session.add(admin)
    # db.session.add(james)
    db.session.commit()

    print("created admin:", admin)


@app.cli.command("create-tags")
def create_tags():
    """
    Run in your terminal:
    ➜ flask create-tags
    """
    for name in [
            "flask",
            "django",
            "python",
            "sqlalchemy",
            "news",
        ]:
        tag = Tag(name=name)
        db.session.add(tag)

        db.session.commit()
        print("created tags")

