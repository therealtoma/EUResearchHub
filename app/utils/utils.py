from re import match
from sqlalchemy import text
from flask import Blueprint, jsonify
from app.models.database import db, Documents, Document_Types
api = Blueprint('api', __name__)

def check_email(s):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return match(pattern, s)

@api.route('/get_doc_types', methods=['POST'])
def get_doc_types():
    d = Document_Types.query.all()
    doc_types = []
    for type in d:
        doc_types.append({
            'id': type.id,
            'name': type.nome
        })

    return jsonify(doc_types)