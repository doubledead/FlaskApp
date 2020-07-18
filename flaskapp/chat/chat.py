from ..core import db
from flask_security import login_required, current_user
from datetime import datetime
from .models import Chat, ChatSchema, Message, MemberSchema, Member, MessageSchema


def create_chat(party_info):
