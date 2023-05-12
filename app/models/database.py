from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum, TIMESTAMP, Date, UUID
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import enum  # mi serve per i tipi enumerativi (status)
import os

load_dotenv()  # carico le variabili d'ambiente

engine = create_engine(os.getenv("DB_URI"))  # creo il motore del database
Session = sessionmaker(bind=engine)  # creo la sessione
db_session = Session()  # creo l'istanza della sessione

Base = declarative_base()  # creo la base per le classi

# definisco il tipo enumerativo all'interno di SQLAlchemy
enum_status = Enum('approved', 'submitted for evaluation', 'require changes', 'not approved')

# definisco le tabelle del database
class Evaluation_Windows(Base):
    __tablename__ = 'evaluation_windows'

    id = Column('id', Integer, primary_key=True)
    evaluation_windows_from = Column('from', Date)
    evaluation_windows_to = Column('to', Date)

    def __init__(self, id, evaluation_windows_from, evaluation_windows_to):
        self.id = id
        self.evaluation_windows_from = evaluation_windows_from
        self.evaluation_windows_to = evaluation_windows_to

    def __repr__(self):
        return f"evaluation_windows('{self.id}', '{self.evaluation_windows_from}', '{self.evaluation_windows_to}')"

class Document_Types(Base):
    __tablename__ = 'document_types'

    id = Column('id', Integer, primary_key=True)
    nome = Column('nome', String)
    descrizione = Column('descrizione', String)

    def __init__(self, id, nome, descrizione):
        self.id = id
        self.nome = nome
        self.descrizione = descrizione

    def __repr__(self):
        return f"document_types('{self.id}', '{self.nome}', '{self.descrizione}')"

class Documents(Base):
    __tablename__ = 'documents'

    id = Column('id', Integer, primary_key=True)

    file_path = Column('file_path', String)

    fk_document_type = Column('fk_document_type', Integer, ForeignKey('document_types.id'))
    fk_project = Column('fk_project', Integer, ForeignKey('projects.id'))

    def __init__(self, id, file_path, fk_document_type, fk_project):
        self.id = id
        self.file_path = file_path
        self.fk_document_type = fk_document_type
        self.fk_project = fk_project

    def __repr__(self):
        return f"documents('{self.id}', '{self.file_path}', '{self.fk_document_type}', '{self.fk_project}')"

class Document_Versions(Base):
    __tablename__ = 'document_versions'

    id = Column('id', Integer, primary_key=True)

    description = Column('description', String)
    date = Column('date', TIMESTAMP)

    fk_document = Column('fk_document', Integer, ForeignKey('documents.id'))

    def __init__(self, id, description, date, fk_document):
        self.id = id
        self.description = description
        self.date = date
        self.fk_document = fk_document

    def __repr__(self):
        return f"document_versions('{self.id}', '{self.description}', '{self.date}', '{self.fk_document}')"

class Evaluation_Reports(Base):
    __tablename__ = 'evaluation_reports'

    id = Column('id', Integer, primary_key=True)

    comment = Column('comment', String)
    date = Column('date', TIMESTAMP)
    file_path = Column('file_path', String)

    fk_document = Column('fk_document', Integer, ForeignKey('documents.id'))

    def __init__(self, id, comment, date, file_path, fk_document):
        self.id = id
        self.comment = comment
        self.date = date
        self.file_path = file_path
        self.fk_document = fk_document

    def __repr__(self):
        return f"evaluation_reports('{self.id}', '{self.comment}', '{self.date}', '{self.file_path}', '{self.fk_document}')"

class Evaluators(Base):
    __tablename__ = 'evaluators'

    id = Column('id', Integer, primary_key=True)

    name = Column('name', String)
    surname = Column('surname', String)
    email = Column('email', String)
    password = Column('password', String)
    profile_picture = Column('profile_picture', String)

    def __init__(self, id, name, surname, email, password, p_p):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.profile_picture = p_p

    def __repr__(self):
        return f"evaluators('{self.id}', '{self.name}', '{self.surname}', '{self.email}', '{self.password}')"

class Evaluators_Evaluation_Reports(Base):
    __tablename__ = 'evaluators_evaluation_reports'

    fk_evaluator = Column('fk_evaluator', Integer, ForeignKey('evaluators.id'), primary_key=True)
    fk_evaluation_report = Column('fk_evaluation_report', Integer, ForeignKey('evaluation_reports.id'), primary_key=True)

    def __init__(self, fk_evaluator, fk_evaluation_report):
        self.fk_evaluator = fk_evaluator
        self.fk_evaluation_report = fk_evaluation_report

    def __repr__(self):
        return f"evaluators_evaluation_reports('{self.fk_evaluator}', '{self.fk_evaluation_report}')"
    
class Projects(Base):
    __tablename__ = 'projects'

    id = Column('id', Integer, primary_key=True)

    title = Column('title', String)
    status = Column('status', enum_status)
    description = Column('description', String)
    date = Column('date', TIMESTAMP)

    fk_evaluation_window = Column('fk_evcaluation_window', Integer, ForeignKey('evaluation_windows.id'))

    def __init__(self, id, title, status, description, date, fk_evaluation_window):
        self.id = id
        self.title = title
        self.status = status
        self.description = description
        self.date = date
        self.fk_evaluation_window = fk_evaluation_window

    def __repr__(self):
        return f"projects('{self.id}', '{self.title}', '{self.status}', '{self.description}', '{self.date}', '{self.fk_evaluation_window}')"

class Evaluators_Projects(Base):
    __tablename__ = 'evaluators_projects'

    fk_evaluators = Column('fk_evaluators', Integer, ForeignKey('evaluators.id'), primary_key=True)
    fk_projects = Column('fk_projects', Integer, ForeignKey('projects.id'), primary_key=True)

    def __init__(self, fk_evaluators, fk_projects):
        self.fk_evaluators = fk_evaluators
        self.fk_projects = fk_projects

    def __repr__(self):
        return f"evaluators_projects('{self.fk_evaluators}', '{self.fk_projects}')"

class Messages(Base):
    __tablename__ = 'messages'

    id = Column('id',Integer, primary_key=True)

    text = Column('text', String)
    date = Column('date', TIMESTAMP)

    fk_projects = Column('fk_projects', Integer, ForeignKey('projects.id'))

    def __init__(self, id, text, date, fk_projects):
        self.id = id
        self.text = text
        self.date = date
        self.fk_projects = fk_projects

    def __repr__(self):
        return f"messages('{self.id}', '{self.text}', '{self.date}', '{self.fk_projects}')"

class Evaluators_Messages(Base):
    __tablename__ = 'evaluators_messages'

    fk_evaluators = Column('fk_evaluators', Integer, ForeignKey('evaluators.id'), primary_key=True)
    fk_messages = Column('fk_messages', Integer, ForeignKey('messages.id'), primary_key=True)

    def __init__(self, fk_evaluators, fk_messages):
        self.fk_evaluators = fk_evaluators
        self.fk_messages = fk_messages

    def __repr__(self):
        return f"evaluators_messages('{self.fk_evaluators}', '{self.fk_messages}')"

class Researchers(Base):
    __tablename__ = 'researchers'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    surname = Column('surname', String)
    email = Column('email', String)
    password = Column('password', UUID)
    affiliation = Column('affiliation', String)
    profile_picture = Column('profile_picture', String)

    def __init__(self, id, name, surname, email, password, affiliation, p_p):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.affiliation = affiliation
        self.profile_picture = p_p

    def __repr__(self):
        return f"researchers('{self.id}', '{self.name}', '{self.surname}', '{self.email}', '{self.password}', '{self.affiliation}')"

class Researchers_Messages(Base):
    __tablename__ = 'researchers_messages'

    fk_researchers = Column('fk_researchers', Integer, ForeignKey('researchers.id'), primary_key=True)
    fk_messages = Column('fk_messsages', Integer, ForeignKey('messages.id'), primary_key=True)

    def __init__(self, fk_researchers, fk_messages):
        self.fk_researchers = fk_researchers
        self.fk_messages = fk_messages

    def __repr__(self):
        return f"researchers_messages('{self.fk_researchers}', '{self.fk_messages}')"

class Researchers_Projects(Base):
    __tablename__ = 'researchers_projects'

    fk_researchers = Column('fk_researchers', Integer, ForeignKey('researchers.id'), primary_key=True)
    fk_projects = Column('fk_projects', Integer, ForeignKey('projects.id'), primary_key=True)

    def __init__(self, fk_researchers, fk_projects):
        self.fk_researchers = fk_researchers
        self.fk_projects = fk_projects

    def __repr__(self):
        return f"researchers_projects('{self.fk_researchers}', '{self.fk_projects}')"
