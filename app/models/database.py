from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql import func
import enum

db = SQLAlchemy()

class EnumStatus(enum.Enum):
    approved = 'approved'
    submitted_for_evaluation = 'submitted for evaluation'
    require_changes = 'require changes'
    not_approved = 'not approved'

# definisco le tabelle del datadb.Model

class Evaluation_Windows(db.Model):
    __tablename__ = 'evaluation_windows'

    id = db.Column('id', db.Integer, primary_key=True)
    evaluation_windows_from = db.Column('from', db.DateTime)
    evaluation_windows_to = db.Column('to', db.DateTime)

class Document_Types(db.Model):
    __tablename__ = 'document_types'

    id = db.Column('id', db.Integer, primary_key=True)
    nome = db.Column('nome', db.String)
    descrizione = db.Column('descrizione', db.String)

class Documents(db.Model):
    __tablename__ = 'documents'

    id = db.Column('id', db.Integer, primary_key=True)

    file_path = db.Column('file_path', db.String)

    fk_document_type = db.Column('fk_document_type', db.Integer, db.ForeignKey('document_types.id'))
    fk_project = db.Column('fk_project', db.Integer, db.ForeignKey('projects.id'))

class Document_Versions(db.Model):
    __tablename__ = 'document_versions'

    id = db.Column('id', db.Integer, primary_key=True)

    description = db.Column('description', db.String)
    date = db.Column('db.DateTime', TIMESTAMP, default=func.current_timestamp())

    fk_document = db.Column('fk_document', db.Integer, db.ForeignKey('documents.id'))

class Evaluation_Reports(db.Model):
    __tablename__ = 'evaluation_reports'

    id = db.Column('id', db.Integer, primary_key=True)

    comment = db.Column('comment', db.String)
    date = db.Column('db.DateTime', TIMESTAMP, default=func.current_timestamp())
    file_path = db.Column('file_path', db.String)

    fk_document = db.Column('fk_document', db.Integer, db.ForeignKey('documents.id'))

class Evaluators(db.Model, UserMixin):
    __tablename__ = 'evaluators'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String)
    surname = db.Column('surname', db.String)
    email = db.Column('email', db.String)
    password = db.Column('password', db.String)
    profile_picture = db.Column('profile_picture', db.String)

class Evaluators_Evaluation_Reports(db.Model):
    __tablename__ = 'evaluators_evaluation_reports'

    fk_evaluator = db.Column('fk_evaluator', db.Integer, db.ForeignKey('evaluators.id'), primary_key=True)
    fk_evaluation_report = db.Column('fk_evaluation_report', db.Integer, db.ForeignKey('evaluation_reports.id'), primary_key=True)
    
class Projects(db.Model):
    __tablename__ = 'projects'

    id = db.Column('id', db.Integer, primary_key=True)

    title = db.Column('title', db.String)
    status = db.Column('status', db.Enum(EnumStatus))
    description = db.Column('description', db.String)
    date = db.Column('db.DateTime', TIMESTAMP, default=func.current_timestamp())

    fk_evaluation_window = db.Column('fk_evcaluation_window', db.Integer, db.ForeignKey('evaluation_windows.id'))

class Evaluators_Projects(db.Model):
    __tablename__ = 'evaluators_projects'

    fk_evaluators = db.Column('fk_evaluators', db.Integer, db.ForeignKey('evaluators.id'), primary_key=True)
    fk_projects = db.Column('fk_projects', db.Integer, db.ForeignKey('projects.id'), primary_key=True)

class Messages(db.Model):
    __tablename__ = 'messages'

    id = db.Column('id',db.Integer, primary_key=True)

    text = db.Column('text', db.String)
    date = db.Column('db.DateTime', TIMESTAMP, default=func.current_timestamp())

    fk_projects = db.Column('fk_projects', db.Integer, db.ForeignKey('projects.id'))

class Evaluators_Messages(db.Model):
    __tablename__ = 'evaluators_messages'

    fk_evaluators = db.Column('fk_evaluators', db.Integer, db.ForeignKey('evaluators.id'), primary_key=True)
    fk_messages = db.Column('fk_messages', db.Integer, db.ForeignKey('messages.id'), primary_key=True)

class Researchers(db.Model, UserMixin):
    __tablename__ = 'researchers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    profile_picture = db.Column(db.String)
    affiliation = db.Column(db.String)
    
    

class Researchers_Messages(db.Model):
    __tablename__ = 'researchers_messages'

    fk_researchers = db.Column('fk_researchers', db.Integer, db.ForeignKey('researchers.id'), primary_key=True)
    fk_messages = db.Column('fk_messsages', db.Integer, db.ForeignKey('messages.id'), primary_key=True)
    
class Researchers_Projects(db.Model):
    __tablename__ = 'researchers_projects'

    fk_researchers = db.Column('fk_researchers', db.Integer, db.ForeignKey('researchers.id'), primary_key=True)
    fk_projects = db.Column('fk_projects', db.Integer, db.ForeignKey('projects.id'), primary_key=True)

class ProjectsStatusCount(db.Model):
    __tablename__ = 'projects_status_count'

    status = db.Column('status', db.Enum(EnumStatus), primary_key=True)
    count = db.Column('count', db.Integer)
