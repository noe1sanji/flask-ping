from datetime import datetime

import click
from flask import Flask, flash, redirect, render_template, request, url_for
from flask.json import jsonify
from flask_cors import CORS

from app.database import db_session, init_db
from app.models import Log, Server

app = Flask(__name__)
app.config["SECRET_KEY"] = "mikey"
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.cli.command("init-db")
@click.command()
def init():
    init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/")
def index():
    servers = Server.query.all()
    return render_template("index.html", servers=servers)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["name"]
        host = request.form["host"]
        server = Server(name, host)
        db_session.add(server)
        db_session.commit()
        flash(f"Servidor {name} añadido correctamente")
        return redirect(url_for("index"))

    return render_template("create.html")


@app.route("/edit/<int:id_server>", methods=["GET", "POST"])
def edit(id_server):
    server = db_session.get(Server, id_server)

    if request.method == "POST":
        name = request.form["name"]
        host = request.form["host"]
        server.name = name
        server.host = host
        db_session.add(server)
        db_session.commit()
        flash(f"{name} actualizado correctamente.")
        return redirect(url_for("index"))

    return render_template("edit.html", server=server)


@app.route("/delete/<int:id_server>", methods=["POST"])
def delete(id_server):
    server = db_session.get(Server, id_server)
    db_session.delete(server)
    db_session.commit()
    flash(f"{server.name} eliminado correctamente.")
    return redirect(url_for("index"))


@app.route("/dashboard/<int:id_server>")
def dashboard(id_server):
    server = db_session.get(Server, id_server)
    return render_template("dashboard.html", server=server)


@app.route("/api/servers")
def servers():
    results = Server.query.all()
    servers = [{"name": server.name, "host": server.host} for server in results]
    return jsonify(servers)


@app.route("/api/storage", methods=["POST"])
def storage():
    data = request.get_json()
    host = data["host"]
    response = data["response"]
    timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
    log = Log(host, response, timestamp)
    db_session.add(log)
    db_session.commit()
    return jsonify({"status": "ok"})


@app.route("/api/metrics/<int:id_server>")
def metrics(id_server):
    server = db_session.get(Server, id_server)
    results = Log.query.filter(Log.server == server.host).all()
    metrics = [
        {
            "server": server.server,
            "response_time": server.response_time,
            "timestamp": server.timestamp.strftime("%Y-%m-%d %H:%M"),
        }
        for server in results
    ]
    return jsonify(metrics)
