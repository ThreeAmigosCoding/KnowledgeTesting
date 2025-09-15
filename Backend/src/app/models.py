from .database import db
from sqlalchemy.orm import relationship
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.Enum('teacher', 'student', name="user_roles"), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    tests_created = relationship('Test', back_populates='author')
    test_results = relationship('Result', back_populates='student')


class Test(db.Model):
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    graph_id = db.Column(db.Integer, db.ForeignKey('graphs.id'), nullable=True)

    author = relationship('User', back_populates='tests_created')
    questions = relationship('Question', back_populates='test')
    graph = relationship('Graph')


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    is_multichoice = db.Column(db.Boolean, default=False)
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'), nullable=True)

    test = relationship('Test', back_populates='questions')
    answers = relationship('Answer', back_populates='question')
    node = relationship('Node')


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)

    question = relationship('Question', back_populates='answers')


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    test = relationship('Test')
    student = relationship('User', back_populates='test_results')
    student_answers = relationship('StudentAnswer', back_populates='result')


class StudentAnswer(db.Model):
    __tablename__ = 'student_answers'

    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey('results.id'), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'), nullable=False)

    result = relationship('Result', back_populates='student_answers')
    answer = relationship('Answer')


class Graph(db.Model):
    __tablename__ = 'graphs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    related_graph_id = db.Column(db.Integer, db.ForeignKey('graphs.id'), nullable=True)

    nodes = relationship('Node', back_populates='graph')
    edges = relationship('Edge', back_populates='graph')


class Node(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    graph_id = db.Column(db.Integer, db.ForeignKey('graphs.id'), nullable=False)

    graph = relationship('Graph', back_populates='nodes')


class Edge(db.Model):
    __tablename__ = 'edges'
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, db.ForeignKey('nodes.id'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('nodes.id'), nullable=False)
    graph_id = db.Column(db.Integer, db.ForeignKey('graphs.id'), nullable=False)

    source = relationship('Node', foreign_keys=[source_id])
    target = relationship('Node', foreign_keys=[target_id])
    graph = relationship('Graph')
