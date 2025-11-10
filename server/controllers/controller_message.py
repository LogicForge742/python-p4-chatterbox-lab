from models import Message,MessageType
from models import db


def create_message(id: int, body: str, username: str, created_at: str, updated_at: str) -> MessageType:

    """Create a new message and add it to the database.
    Args:
        id (int): The ID of the message.
        body (str): The body of the message.
        username (str): The username of the message sender.
        created_at (str): The creation timestamp of the message.
        updated_at (str): The last updated timestamp of the message.
    Returns:
        MessageType: The created message object.
    
    """

    message = Message(id=id, body=body, username=username, created_at=created_at, updated_at=updated_at)
    db.session.add(message)
    db.session.commit()
    return message


def get_message_by_id(message_id: int) -> MessageType | None:

    """Retrieve a message by its ID.
    Args:
        message_id (int): The ID of the message to retrieve.
    Returns:
        MessageType | None: The message object if found, otherwise None.
    
    """
    message = Message.query.get(message_id)
    if message:
        return MessageType(
            id=message.id,
            body=message.body,
            username=message.username,
            created_at=message.created_at,
            updated_at=message.updated_at
        )
    return None

def get_all_messages() -> list[MessageType]:
    """Retrieve all messages from the database.
    Returns:
        list[MessageType]: A list of all message objects.
    
    """
    messages = Message.query.all() # Select all messages from the database
    return [MessageType( id = message.id,
                        body = message.body,
                        username = message.username,
                        created_at = message.created_at,
                        updated_at = message.updated_at) for message in messages]     


def update_message(message_id: int, body: str, username: str) -> MessageType | None:
    """Update a message by its ID.
    Args:
        message_id (int): The ID of the message to update.
        body (str): The new body of the message.
        username (str): The new username of the message sender.
    Returns:
        MessageType | None: The updated message object if found, otherwise None.
    
    """
    message = Message.query.get(message_id)
    if message:
        message.body = body
        message.username = username
        db.session.commit()
        return MessageType(
            id=message.id,
            body=message.body,
            username=message.username,
            created_at=message.created_at,
            updated_at=message.updated_at
        )
    return None


def delete_message(message_id: int) -> bool:
    """Delete a message by its ID.
    Args:
        message_id (int): The ID of the message to delete.
    Returns:
        bool: True if the message was deleted, otherwise False.
    
    """
    message = Message.query.get(message_id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return True
    return False


