from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request

from ..models import db, Note
from ..schemas import (
    NoteCreateSchema,
    NoteUpdateSchema,
    NoteResponseSchema,
)
from ..auth_utils import login_required

blp = Blueprint("Notes", "notes", url_prefix="/api/notes", description="Operations on notes")

# PUBLIC_INTERFACE
@blp.route("/")
class NotesList(MethodView):
    """Handles /api/notes endpoint for list and note creation."""

    @blp.response(200, NoteResponseSchema(many=True))
    @login_required
    def get(self):
        """Get all notes for the authenticated user."""
        user_id = request.user_id
        notes = Note.query.filter_by(user_id=user_id).order_by(Note.created_at.desc()).all()
        return notes

    @blp.arguments(NoteCreateSchema)
    @blp.response(201, NoteResponseSchema)
    @login_required
    def post(self, note_data):
        """Create a new note for the authenticated user."""
        user_id = request.user_id
        note = Note(title=note_data["title"], content=note_data["content"], user_id=user_id)
        db.session.add(note)
        db.session.commit()
        return note

# PUBLIC_INTERFACE
@blp.route("/<int:note_id>")
class NoteDetail(MethodView):
    """Handles /api/notes/<note_id> endpoint for note CRUD."""

    @blp.response(200, NoteResponseSchema)
    @login_required
    def get(self, note_id):
        """Get a single note by id (must belong to user)."""
        user_id = request.user_id
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            abort(404, message="Note not found")
        return note

    @blp.arguments(NoteUpdateSchema)
    @blp.response(200, NoteResponseSchema)
    @login_required
    def patch(self, note_data, note_id):
        """Update a note (partial update, only owner)."""
        user_id = request.user_id
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            abort(404, message="Note not found")
        if "title" in note_data:
            note.title = note_data["title"]
        if "content" in note_data:
            note.content = note_data["content"]
        db.session.commit()
        return note

    @login_required
    def delete(self, note_id):
        """Delete a note (only owner)."""
        user_id = request.user_id
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            abort(404, message="Note not found")
        db.session.delete(note)
        db.session.commit()
        return {"message": "Note deleted"}, 200
