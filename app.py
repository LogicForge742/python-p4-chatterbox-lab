from server.app import app

# Expose `app` at the project root so tests importing `from app import app`
# get the same Flask application instance used in the `server` package.
