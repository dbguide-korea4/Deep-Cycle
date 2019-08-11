# coding: utf-8
from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, Table, Text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


# t_sqlite_sequence = db.Table(
#     'sqlite_sequence',
#     db.Column('name', db.NullType),
#     db.Column('seq', db.NullType)
# )


class UserFile(db.Model):
    __tablename__ = 'user_file'

    file_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user_table.id'), nullable=False)
    file_name = db.Column(db.Text, nullable=False)
    output = db.Column(db.Text, nullable=False)
    point = db.Column(db.Integer, nullable=False,
                      server_default=db.FetchedValue())
    date = db.Column(db.DateTime, nullable=False,
                     server_default=db.FetchedValue())

    user = db.relationship(
        'UserTable', primaryjoin='UserFile.user_id == UserTable.id', backref='user_files')


class UserTable(db.Model):
    __tablename__ = 'user_table'
    __table_args__ = (
        db.CheckConstraint("email like '%@%'"),
    )

    id = db.Column(db.Text, primary_key=True)
    pw = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    join_date = db.Column(db.DateTime, server_default=db.FetchedValue())
    last_access_date = db.Column(db.DateTime, server_default=db.FetchedValue())
    total_point = db.Column(db.Integer, server_default=db.FetchedValue())
