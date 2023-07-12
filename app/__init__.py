from app.database import db_session
from flask import Flask, render_template, request, redirect, session, url_for, flash
from app.models import Server

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mikey'

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    servers = Server.query.all()
    return render_template('index.html', servers=servers)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        host = request.form['host']
        server = Server(name, host)
        db_session.add(server)
        db_session.commit()
        flash(f'Servidor {name} añadido correctamente')
        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/edit/<int:id_server>', methods=['GET', 'POST'])
def edit(id_server):
    server = db_session.get(Server, id_server)

    if request.method == 'POST':
        name = request.form['name']
        host = request.form['host']
        # server = Server.query.filter(Server.name == name).first()
        server.name = name
        server.host = host
        db_session.add(server)
        db_session.commit()
        flash(f'{name} actualizado correctamente.')
        return redirect(url_for('index'))

    return render_template('edit.html', server=server)

@app.route('/delete/<int:id_server>', methods=['POST'])
def delete(id_server):
    server = db_session.get(Server, id_server)
    db_session.delete(server)
    db_session.commit()
    flash(f'{server.name} eliminado correctamente.')
    return redirect(url_for('index'))
