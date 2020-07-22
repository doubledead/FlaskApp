from flask import Blueprint, current_app, json, redirect, render_template, request, session, url_for
from flask_security import login_required, current_user
from flask_socketio import emit, join_room, leave_room, send
from ..core import db, mail, socketio
from datetime import datetime
from sqlalchemy import exc
# from ..utils import representsint
from ..models import Chat, ChatSchema, member_schema, Member, Message, message_schema, User

chat = Blueprint('chat', __name__, template_folder='templates')


@chat.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('/chat/index.html')


@chat.route('/<chat_id>', methods=['GET', 'POST'])
@login_required
def view(chat_id):
    c = Chat.query.filter_by(id=chat_id).first_or_404()

    for m in c.members:
        if current_user.email == m.email:
            name = m.email
            room = c.name

            chat_messages = []
            for chat_message in c.messages:
                c_member = get_chat_member(chat_message.member_id)
                chat_message = {
                    'id': chat_message.id,
                    'created_at': chat_message.created_at,
                    'name': c_member.name,
                    'status_code': chat_message.status_code,
                    'text': chat_message.text
                }
                chat_messages.append(chat_message)

            return render_template('/chat/chat.html', chat_messages=chat_messages, name=name, room=room)

# TODO: add host_view() with all Chat data


@chat.route('/get_chat_payload', methods=['GET', 'POST'])
@login_required
def get_chat_payload():
    if request.method == "POST":
        try:
            data = request.get_json()
            print(data)
            print('Test')
            param_id = data["paramId"]
            c = get_chat(param_id)

            messages = []
            for m in c.members:
                if get_current_user_email() == m.email:
                    for me in c.messages:
                        # append to Python list
                        mes = {
                            'created_at': me.created_at,
                            'text': me.text,
                            'username': get_user_email(me.user_id)
                        }
                        messages.append(mes)

            payload = {"messages": messages}
            current_app.logger.info('sending payload')
            print(payload)

            # return dictionary as JSON object
            return json.dumps(payload)
        except exc.SQLAlchemyError as e:
            current_app.logger.error(e)
            return json.dumps({'status': 'Error'})
    else:
        return render_template("errors/404.html")


# SocketIO Events
@socketio.on('joined')
def joined(m):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    c_id = m['paramId']
    c = get_chat(c_id)

    c_user_email = get_current_user_email()

    # only Chat Members allowed to join chat
    for m in c.members:
        if c_user_email == m.email:

            # TODO: update member status to 1, online
            # TODO: add username to Member and Message model

            room = get_room(c_id)
            join_room(room)

            emit('status', {'msg': m.name + ' has entered the room.'}, room=room)


@socketio.on('text')
def text(message):
    c_id = message['paramId']
    c = get_chat(c_id)

    # member_email = ''
    c_user_email = get_current_user_email()

    for chat_member in c.members:
        if c_user_email == chat_member.email:

            room = get_room(c_id)

            chat_message = Message(chat_id=c.id, status_code=1, text=str(message['msg']), member_id=chat_member.id)

            c.messages.append(chat_message)

            emit('message', {'msg': chat_member.name + ': ' + message['msg']}, room=room)
    try:
        db.session.add(c)
        db.session.commit()
        return json.dumps({'status': 'OK'})
    except exc.SQLAlchemyError as e:
        current_app.logger.error(e)
        return json.dumps({'status': 'Error'})


@socketio.on('left')
def left(message):
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)


def get_room(c_id):
    return '/chat/' + c_id


def get_chat(c_id):
    c = Chat.query.filter_by(id=c_id).first_or_404()
    return c


def get_user_email(u_id):
    u = User.query.filter_by(id=u_id).first_or_404()
    return u.email


def get_current_user_email():
    return current_user.email


def get_chat_member(m_id):
    m = Member.query.filter_by(id=m_id).first_or_404()
    return m
