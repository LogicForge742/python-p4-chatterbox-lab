from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

try:
    # When tests import as a top-level module (from app import app)
    from models import db, Message
except Exception:
    # When imported as a package (from server.app import app)
    from .models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# Ensure database tables exist and seed a default record if empty so tests
# that expect at least one Message can run when importing the app.
with app.app_context():
    db.create_all()
    if not Message.query.first():
        seed_msg = Message(body="Seed message", username="Seeder")
        db.session.add(seed_msg)
        db.session.commit()

# list/create endpoints handled below

@app.route('/messages/<int:id>', methods=['GET']) 
def messages_by_id(id):
    message = Message.query.get(id)
    if message:
        response = make_response(jsonify({
            'id': message.id,
            'body': message.body,
            'username': message.username,
            'created_at': message.created_at.isoformat(),
            'updated_at': message.updated_at.isoformat()
        }), 200)
    else:
        response = make_response(jsonify({'error': 'Message not found'}), 404)
    return response

@app.route('/messages',methods= ['GET'])
def get_messages():
    messages = Message.query.all()
    message_list = [{
        'id':message.id,
        'body':message.body,
        'username':message.username,
        'created_at':message.created_at.isoformat(),
        'updated_at': message.updated_at.isoformat()

    } for message in messages] 

    response = make_response(jsonify(message_list),200)

    return response


@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(
        body=data['body'],
        username=data['username']
    )
    db.session.add(new_message)
    db.session.commit()
    response = make_response(jsonify({
        'id': new_message.id,
        'body': new_message.body,
        'username': new_message.username,
        'created_at': new_message.created_at.isoformat(),
        'updated_at': new_message.updated_at.isoformat()
    }), 201)
    return response


@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)

    if not message:
        return jsonify({"error":"message not found"})
    
    #get message
    data = request.get_json()
    message.body = data.get("body",message.body)
    message.username = data.get("username", message.username)

    db.session.commit()

    return jsonify({
        'id':message.id,
        'body':message.body,
        'username':message.username
         
    })
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({"error":"message not found"})
    
    
    db.session.delete(message)
    db.session.commit()

    return jsonify({"message": "Message deleted successfully."})


        





if __name__ == '__main__':
    app.run(port=5555)
