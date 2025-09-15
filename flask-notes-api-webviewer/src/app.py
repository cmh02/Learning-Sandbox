'''
Flask Notes API + Webviewer

Author: Chris Hinkson
Github: @cmh02
'''

# Module Imports
from flask import Flask, render_template, request, redirect, url_for, jsonify

# Flask Constructor (sets the name of the app)
app = Flask(__name__)

# Default notes data
notes = [
    {"id": 1, "text": "First note!"},
    {"id": 2, "text": "Flask is fun."},
    {"id": 3, "text": "War Eagle!"}
]
next_id = 4

'''
WEB ROUTES
'''

# API route for index page
@app.route('/')
def index():
    return render_template('index.html', notes=notes)

# API Route to get notes
@app.route("/add", methods=["POST"])
def add_note():
    global next_id
    text = request.form.get("note")
    if text:
        notes.append({"id": next_id, "text": text})
        next_id += 1
    return redirect(url_for("index"))

# API Route to delete notes
@app.route("/delete/<int:note_id>")
def delete_note(note_id):
    global notes
    notes = [n for n in notes if n["id"] != note_id]
    return redirect(url_for("index"))

'''
API ROUTES
'''

# API route to get notes
@app.route("/api/notes", methods=["GET"])
def api_get_notes():
    return jsonify(notes)

# API route to add a note
@app.route("/api/notes", methods=["POST"])
def api_add_note():
    global next_id
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing text"}), 400
    note = {"id": next_id, "text": data["text"]}
    notes.append(note)
    next_id += 1
    return jsonify(note), 201

# API route to delete a note
@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def api_delete_note(note_id):
    global notes
    notes = [n for n in notes if n["id"] != note_id]
    return jsonify({"status": "deleted"})

'''
APP DRIVER
'''

if __name__ == '__main__':
    app.run()