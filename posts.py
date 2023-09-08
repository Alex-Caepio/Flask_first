from flask import request, jsonify

from app_setup import conn, app

POSTS = [
    {
        'name': 'Oleg',
        'text': 'Hello World!',
        'date': '2020-01-01 00:00:00'
    },
    {
        'name': 'Ivan',
        'text': 'Hello World!',
        'date': '2020-01-01 00:00:00'
    },
    {
        'name': 'Igor',
        'text': 'Hello World!',
        'date': '2020-01-01 00:00:00'
    }
]


@app.post('/create_table')
def create_table():
    cur = conn.cursor()
    cur.execute('CREATE TABLE posts (id serial PRIMARY KEY, name varchar, text varchar, date varchar);')
    conn.commit()
    response_data = {'status': 'table created'}
    return jsonify(response_data), 201


@app.post('/create_post_in_table')
def create_post_in_table():
    cur = conn.cursor()
    cur.execute('INSERT INTO posts (name, text, date) VALUES (%s, %s, %s);',
                (request.json['name'], request.json['text'], request.json['date']))
    conn.commit()
    response_data = {'status': 'post created'}
    return jsonify(response_data), 201


@app.get('/get_posts')
def get_posts():
    return {'posts': POSTS}


@app.get('/get_posts_by_id/<int:id>')
def get_posts_by_id(id):
    cur = conn.cursor()
    cur.execute('SELECT * FROM posts WHERE id = %s;', (id,))
    posts = cur.fetchall()
    response_data = {'posts': posts}
    return jsonify(response_data), 200


@app.post('/add_post/')
def add_post():
    POSTS.append(request.json)
    response_data = {'status': 'post created'}
    return jsonify(response_data), 201


if __name__ == '__main__':
    app.run()
