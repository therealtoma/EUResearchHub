from re import match
from sqlalchemy import text
from flask import Blueprint, jsonify
from app.models.database import db, Documents, Document_Types
api = Blueprint('api', __name__)

def check_email(s):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return match(pattern, s)

@api.route('/get_doc_types/<int:project_id>', methods=['POST'])
def get_doc_types(project_id):
    documents = Documents.query.filter_by(fk_project=project_id).all()
    doc_types = []
    for type in documents:
        d = Document_Types.query.filter_by(id=type.fk_document_type).first()
        doc_types.append({
            'id': d.id,
            'name': d.nome
        })

    return jsonify(doc_types)