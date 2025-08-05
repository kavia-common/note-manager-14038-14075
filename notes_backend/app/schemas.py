from marshmallow import Schema, fields

# PUBLIC_INTERFACE
class UserRegisterSchema(Schema):
    """Schema for registering a new user."""
    username = fields.String(required=True, validate=lambda s: 3 <= len(s) <= 80, description="Unique username (3-80 chars).")
    password = fields.String(required=True, load_only=True, validate=lambda s: len(s) >= 6, description="Password, minimum 6 characters.")

# PUBLIC_INTERFACE
class UserLoginSchema(Schema):
    """Schema for user login."""
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)

# PUBLIC_INTERFACE
class NoteCreateSchema(Schema):
    """Schema for creating a note."""
    title = fields.String(required=True, validate=lambda s: 1 <= len(s) <= 120, description="Note title (1-120 chars).")
    content = fields.String(required=True, description="Content of the note.")

# PUBLIC_INTERFACE
class NoteUpdateSchema(Schema):
    """Schema for updating a note."""
    title = fields.String(validate=lambda s: 1 <= len(s) <= 120)
    content = fields.String()

# PUBLIC_INTERFACE
class NoteResponseSchema(Schema):
    """Schema for returning note details."""
    id = fields.Integer()
    title = fields.String()
    content = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    user_id = fields.Integer()
