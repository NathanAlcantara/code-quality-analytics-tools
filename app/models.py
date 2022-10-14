import getpass
from datetime import datetime
from enum import unique

from flask_sqlalchemy import SQLAlchemy, event

db = SQLAlchemy()


class AuditColumns:
    """Mapeamento padrão sobre a informação de criação e atualização do objeto"""

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow(), nullable=False)
    created_by = db.Column(db.String(64), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow(),
        nullable=False,
        onupdate=datetime.utcnow(),
    )
    updated_by = db.Column(db.String(64), nullable=False)

    @event.listens_for(db.mapper, "before_insert")
    @staticmethod
    def before_insert(mapper, connection, target):
        username = getpass.getuser()
        target.created_at = datetime.utcnow()
        target.created_by = username

        target.updated_at = datetime.utcnow()
        target.updated_by = username

    @event.listens_for(db.mapper, "before_update")
    @staticmethod
    def before_update(mapper, connection, target):
        username = getpass.getuser()
        target.updated_at = datetime.utcnow()
        target.updated_by = username


class GitlabGroup(db.Model, AuditColumns):
    name = db.Column(db.String(128), nullable=False)

    gitlab_projects = db.relationship(
        "GitlabProject", backref='gitlab_group', lazy=True, cascade="all, delete")


class HierarchyGroup(db.Model, AuditColumns):
    product = db.Column(db.String(128), nullable=False)
    module = db.Column(db.String(128), nullable=False)
    manager = db.Column(db.String(128), nullable=False)

    gitlab_projects = db.relationship("GitlabProject", cascade="all, delete")
    sonar_projects = db.relationship("SonarProject", cascade="all, delete")

    __table_args__ = (
        db.UniqueConstraint('product', 'module',
                            'manager', name='unique_group'),
    )


class GitlabProject(db.Model, AuditColumns):
    name = db.Column(db.String(128), nullable=False)
    web_url = db.Column(db.String(128), nullable=False)

    gitlab_group_id = db.Column(
        db.Integer, db.ForeignKey("gitlab_group.id"), nullable=False)
    gitlab_group = db.relationship(
        "GitlabGroup", back_populates="gitlab_projects")

    hierarchy_group_id = db.Column(
        db.Integer, db.ForeignKey("hierarchy_group.id"), nullable=False)
    hierarchy_group = db.relationship(
        "HierarchyGroup", back_populates="gitlab_projects")

    sonar_project = db.relationship(
        "SonarProject", back_populates="gitlab_project", uselist=False)


class SonarProject(db.Model, AuditColumns):
    sonar_id = db.Column(db.String(30), nullable=False, unique=True)
    key = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128), nullable=False)

    gitlab_project_id = db.Column(
        db.Integer, db.ForeignKey("gitlab_project.id"), unique=True, nullable=False)
    gitlab_project = db.relationship(
        "GitlabProject", back_populates="sonar_project")

    hierarchy_group_id = db.Column(
        db.Integer, db.ForeignKey("hierarchy_group.id"), nullable=False)
    hierarchy_group = db.relationship(
        "HierarchyGroup", back_populates="sonar_projects")


@event.listens_for(SonarProject, "before_insert")
@staticmethod
def before_insert(mapper, connection, target):
    target.hierarchy_group = target.gitlab_project.hierarchy_group
