from flask import Flask, render_template, request, redirect
import os
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__)) 
database_file = "sqlite:///{}".format(os.path.join(project_dir, "todo.db"))
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
print(database_file)

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(500))
    complete = db.Column(db.Boolean)


@app.route('/')
def index():
    todos = Todo.query.all()

    return render_template('index.html', todos = todos)

@app.route('/addTask', methods=['POST'])
def add():
    text = request.form['text']
    if text:
        todo = Todo(text=text, complete=False)
        db.session.add(todo)
        db.session.commit()
    return redirect('/')

@app.route('/updateTask/<id>', methods=['GET'])
def update(id):    
    todo  = Todo.query.filter_by(id=int(id)).first()
    if todo:
        todo.complete = not todo.complete
        db.session.commit()
    return redirect('/')

@app.route('/deleteTask/<id>', methods=['GET'])
def delete(id):    
    todo  = Todo.query.filter_by(id=int(id)).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
