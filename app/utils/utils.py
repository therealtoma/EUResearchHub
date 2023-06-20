from re import match
from flask import Blueprint, jsonify, render_template, redirect, url_for, request
from flask_login import login_required
from app.models.database import db, Documents, Document_Types, Document_Versions, Evaluation_Reports, Evaluation_Windows
from sqlalchemy.sql import exists
from datetime import datetime, timedelta
import os
api = Blueprint('api', __name__)

def check_email(s):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return match(pattern, s)

@api.route('/get_doc_types/<int:project_id>', methods=['POST'])
@login_required
def get_doc_types(project_id):
    '''
    restituire solo i doc type che non sono ancora stati caricati in quel progetto
    la query da eseguire è questa:

    SELECT dt.id, dt.nome
    FROM document_types dt LEFT JOIN documents d ON dt.id = d.fk_document_type ADN d.fk_project = project_id
    WHERE d.fk_document_type IS NULL;

    '''

    unused_types = db.session.query(Document_Types).filter(
        ~exists().where((Documents.fk_document_type == Document_Types.id) & (Documents.fk_project == project_id))
    ).all()
    doc_types = []
    for type in unused_types:
        doc_types.append({
            'id': type.id,
            'name': type.nome
        })

    return jsonify(doc_types)

@api.route('/upload_document/<int:project_id>', methods=['POST'])
@login_required
def upload_document(project_id):
    '''
    il pdf va dentro la cartella del progetto
    nella cartella del progetto tante cartelle con l'id del doc_type
    all'interno di quelle cartelle tanti pdf con l'id del doc version
    '''
    # caricare il file nella cartella specifica
    if request.files.get('document'):
        docType = request.form.get('docType')
        currentDirectory = os.path.dirname(os.path.realpath(__file__))
        folderPath = os.path.join(currentDirectory, '../static/uploads/projects/' + str(project_id) + '/' + docType + '/')
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
        document = request.files.get('document')

        # aggiungo il documento al database
        docDB = Documents(file_path=os.path.join(str(project_id), '/', docType), fk_document_type=docType, fk_project=project_id)
        db.session.add(docDB)
        db.session.commit()

        # aggiungo la version al database
        docVersion = Document_Versions(title='First commit', description=None, fk_document=docDB.id)
        db.session.add(docVersion)
        db.session.commit()

        # salvo il file
        document.save(os.path.join(folderPath, str(docVersion.id) + '.pdf'))

    return redirect(url_for('views.project', project_id=project_id))

@api.route('/upload_version/<int:project_id>/<int:document_id>', methods=['POST'])
@login_required
def upload_version(project_id, document_id):
    '''
    il pdf della versione va dentro alla cartella del progetto
    nella cartella del progetto, ho le cartelle con gli id dei vari document type
    nella cartella dei document types ci sono tanti pdf quante le versioni nominati con l'id della versione
    '''
    if request.files.get('docVersion'):
        description = request.form.get('description')
        title = request.form.get('title')
        currentDirectory = os.path.dirname(os.path.realpath(__file__))
        folderPath = os.path.join(currentDirectory, '../static/uploads/projects/' + str(project_id) + '/' + str(document_id) + '/')
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
        document = request.files.get('docVersion')

        docId = Documents.query.filter_by(fk_document_type=document_id, fk_project=project_id).first().id

        # aggiungo la versione all'interno del database
        docVersion = Document_Versions(title=title, description=description, fk_document=docId)
        db.session.add(docVersion)
        db.session.commit()
        # salvo il file nella cartella
        document.save(os.path.join(folderPath, str(docVersion.id) + '.pdf'))

    return redirect(url_for('views.project', project_id=project_id))

@api.route('/upload_report/<int:project_id>/<int:document_id>', methods=['POST'])
@login_required
def upload_report(project_id, document_id):
    '''
    ricevo un pdf che rappresenta l'evaluation report
    salvo il pdf all'interno della cartella del documento relativo a quel progetto
    '''
    if request.files.get('report'):
        comment = request.form.get('comment')
        currentDirectory = os.path.dirname(os.path.realpath(__file__))
        folderPath = os.path.join(currentDirectory, '../static/uploads/projects/' + str(project_id) + '/' + str(document_id) + '/')
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
        report = request.files.get('report')

        # document_id è l'id del doc_type. Io ho bisogni dell'id del documento. Posso ottenerlo combinando project_id e doctype.document_id
        docId = Documents.query.filter_by(fk_document_type = document_id, fk_project = project_id).first().id

        # aggiungo il report all'interno del database
        evReport = Evaluation_Reports(comment=comment, fk_document=docId, file_path=str(project_id) + '/' + str(document_id))
        db.session.add(evReport)
        db.session.commit()

        # salvo il file nella cartella
        report.save(os.path.join(folderPath, 'evaluation_report.pdf'))

        return redirect(url_for('views.project', project_id=project_id))


def scheduled_ev_win():
    ev_win = Evaluation_Windows(evaluation_windows_from=datetime.now(),
                               evaluation_windows_to=datetime.now() + timedelta(days=30))
    db.session.add(ev_win)
    db.session.commit()
