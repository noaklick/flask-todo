from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()

# /// = relative path, //// = absolute path
# configures the sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# sets up the database columns
# column concept example
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# route concept example
@app.route('/')
def home():
    todo_list = Todo.query.all()
    # renders the base template with the todo list from the db
    # example of render template concept
    return render_template("base.html", todo_list=todo_list)

# route concept example
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    # inserts a new todo item in the db
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))

# route concept example
@app.route("/update/<int:todo_id>")
def update(todo_id):
    # gets the selected todo and flips its box
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

# route concept example
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # gets the selected todo and deletes it
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)