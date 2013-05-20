from flask import Flask, render_template, url_for
from datetime import datetime

from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
from evernote.edam.notestore import NoteStore

app = Flask(__name__)

#put your development token below
dev_token = "your api key"

#load the client with the token
client = EvernoteClient(token=dev_token)

#initialize the client stores to access the data
user_store = client.get_user_store()
note_store = client.get_note_store()

#simple filter to get the notes ordered by update time
filter = NoteStore.NoteFilter(order=Types.NoteSortOrder.UPDATED)
spec_metadata = NoteStore.NotesMetadataResultSpec(includeTitle=True, includeUpdated=True)


@app.route('/')
def index():

    #load the username
    user = user_store.getUser()

    #load the notes
    notes = note_store.findNotesMetadata(filter, 0, 10, spec_metadata)
    notes = [{'guid':note.guid, 'title':note.title, 'updated':datetime.fromtimestamp(note.updated / 1e3).strftime('%Y/%m/%d %H:%M')} for note in notes.notes]
    
    return render_template('index.html', user=user.username, notes=notes)


@app.route('/note/<guid>')
def view_note(guid):
    note = note_store.getNote(guid, withContent=True, withResourcesData=False, withResourcesRecognition=False, withResourcesAlternateData=False)
    note.updated = datetime.fromtimestamp(note.updated / 1e3)
    return render_template('note.html', note={'title':note.title, 'content':note.content, 'updated':note.updated.strftime('%Y/%m/%d')})


if __name__ == "__main__":
    app.debug = True
    app.run()