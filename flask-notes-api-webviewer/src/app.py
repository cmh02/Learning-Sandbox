'''
Flask Notes API + Webviewer

Author: Chris Hinkson
Github: @cmh02
'''

# Module Imports
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

# Instance configuration
PATH_BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PATH_INSTANCE = os.path.join(PATH_BASE_DIR, "instance")
PATH_SQLDB = os.path.join(PATH_INSTANCE, "notes.db")
os.makedirs(PATH_INSTANCE, exist_ok=True)

# Flask Constructor (sets the name of the app)
app = Flask(__name__, instance_path=PATH_INSTANCE)

# Configure the SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{PATH_SQLDB}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Create the Note model
class Note(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(200), nullable=False)

'''
WEB ROUTES

This section will create some web routes that can be used to interact with the notes database via a simple web interface.
'''

# API route for index page
@app.route('/')
def web_index():
	# Query all notes from the database
	notes = Note.query.all()
	
	# Render the index.html template with the notes
	return render_template("index.html", notes=notes)

# API Route to get notes
@app.route("/add", methods=["POST"])
def web_addNote():

	# Get the note text from the form
	note_text = request.form.get("noteText")
	if note_text:
		
		# Create a new Note object, add it to the db, commit the change
		new_note = Note(text=note_text)
		db.session.add(new_note)
		db.session.commit()
		
	# Redirect back to the index page
	return redirect(url_for("web_index"))


# API Route to delete notes
@app.route("/delete/<int:note_id>")
def web_deleteNote(note_id):

	# Check if the note_id exists
	note = Note.query.get(note_id)
	if note:
		
		# Delete the note, commit the change
		db.session.delete(note)
		db.session.commit()
		
	# Redirect back to the index page
	return redirect(url_for("web_index"))

'''
API ROUTES

This section will create some API endpoints that can be used to interact with the notes database.

Example Usage with curl:

-> Get all notes: curl http://127.0.0.1:5000/api/notes
-> Add a note: curl -X POST -H "Content-Type: application/json" -d '{"text":"Sample Note"}' http://127.0.0.1:5000/api/notes
-> Delete a note: curl -X DELETE http://127.0.0.1:5000/api/notes/<note_id>
'''

# API route to get notes
@app.route("/api/notes", methods=["GET"])
def api_getAllNotes():
      
	# Query all notes from the database
	notes = Note.query.all()
		  
	# Convert notes to a list of dictionaries
	notes_list = [{"id": note.id, "text": note.text} for note in notes]
		  
	# Return the list of notes as JSON
	return jsonify(notes_list), 200
    

# API route to add a note
@app.route("/api/notes", methods=["POST"])
def api_addNote():

	# Get the note text from the request
	note_text = request.json.get("text")
	if note_text:
		  
		# Create a new Note object, add it to the db, commit the change
		new_note = Note(text=note_text)
		db.session.add(new_note)
		db.session.commit()
		  
		# Return the new note as JSON
		return jsonify({"id": new_note.id, "text": new_note.text}), 201
	else:
		  
		# If no text is provided, return an error
		return jsonify({"error": "No text provided"}), 400


# API route to delete a note from the database
@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def api_deleteNote(note_id):

	# Check if the note_id exists
	note = Note.query.get(note_id)
	if note:
          
		# Delete the note, commit the change, return success
		db.session.delete(note)
		db.session.commit()
		return jsonify({"message": "Note deleted"}), 200
	else:
          
		# If the note_id does not exist, return an error
		return jsonify({"error": "Note not found"}), 404
    
'''
APP DRIVER
'''
if __name__ == '__main__':

	# Create db
	with app.app_context():
		db.create_all()

	# Run the app
	app.run(debug=True)