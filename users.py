from flask import render_template, request, jsonify

from app_setup import app, conn

USERS = {
    1: {'name': 'Oleg', 'age': 30},
    2: {'name': 'Ivan', 'age': 25},
    3: {'name': 'Igor', 'age': 20},
}


@app.post('/create_table_users')
def create_table_users():
    cur = conn.cursor()
    cur.execute('CREATE TABLE users (id serial PRIMARY KEY, name varchar, age integer);')
    conn.commit()
    response_data = {'status': 'table created'}
    return jsonify(response_data), 201


@app.post('/alter_table_users')
def alter_table_users():
    cur = conn.cursor()
    cur.execute('ALTER TABLE users ADD COLUMN post_id integer;')
    conn.commit()
    response_data = {'status': 'table altered'}
    return jsonify(response_data), 201


@app.get('/get_users')
def get_users():
    cur = conn.cursor()
    cur.execute('SELECT * FROM users;')
    users = cur.fetchall()
    response_data = {'users': users}
    return jsonify(response_data), 200


@app.route('/users/<int:id>')
def users(id):
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s;', (id,))
    users = cur.fetchall()
    response_data = {'users': users}
    return jsonify(response_data), 200


@app.post('/add_user/')
def add_user():
    cur = conn.cursor()
    cur.execute('INSERT INTO users (name, age, post_id) VALUES (%s, %s, %s);',
                (request.json['name'], request.json['age'], request.json['post_id']))
    conn.commit()
    response_data = {'status': 'user created'}
    return jsonify(response_data), 201


@app.get('/get_users_post/<int:id>')
def get_users_post(id):
    cur = conn.cursor()
    cur.execute('SELECT name, text FROM users LEFT JOIN posts ON users.post_id = posts.id WHERE users.id = %s;',
                (id,))
    users = cur.fetchall()
    response_data = {'users': users}
    return jsonify(response_data), 200


@app.route('/user_info', methods=['GET'])
def user_info():
    return render_template('user_info.html')


@app.route('/get_user_info', methods=['POST'])
def get_user_info():
    user_id = request.form['user_id']

    cur = conn.cursor()
    cur.execute('SELECT name, text FROM users INNER JOIN posts ON users.post_id = posts.id WHERE users.post_id = %s;',
                (user_id,))
    user_info = cur.fetchall()

    return render_template('user_info_response.html', user_info=user_info)


if __name__ == '__main__':
    app.run()
