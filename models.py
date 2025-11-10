from server.models import db, Message

# Re-export `db` and `Message` at the project root so tests importing
# `from models import db, Message` receive the same SQLAlchemy objects
# used by the `server` application.
