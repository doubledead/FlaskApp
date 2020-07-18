from flask import Blueprint, render_template
# from flask import request, redirect, url_for, json, current_app
from ..core import db, mail
from flask_security import login_required, current_user
from datetime import datetime
# from sqlalchemy import exc
# from ..utils import representsint
from .models import Chat, ChatSchema, Message, MemberSchema, Member, MessageSchema

chat = Blueprint('chat', __name__, template_folder='templates')


@chat.route('/', methods=['GET', 'POST'])
def index():
    return render_template('/chat/chat.html')
