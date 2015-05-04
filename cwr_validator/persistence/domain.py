# -*- coding: utf-8 -*-

__author__ = 'Borja'

from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from cwr_validator.validator.service import db


class AgreementRole(db.Model):
    __tablename__ = 'agreementRoles'
    id = Column(String(2), primary_key=True, autoincrement=False)
    name = Column(String(20))
    description = Column(String(200))

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description


class AgreementType(db.Model):
    __tablename__ = 'agreementTypes'
    id = Column(String(2), primary_key=True, autoincrement=False)
    name = Column(String(32))
    description = Column(String(500))

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description


class CompositeType(db.Model):
    __tablename__ = 'compositeTypes'
    id = Column(String(3), primary_key=True, autoincrement=False)
    name = Column(String(50))
    description = Column(String(500))

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description


class DistributionCategory(db.Model):
    __tablename__ = 'distributionCategories'
    id = Column(String(3), primary_key=True, autoincrement=False)
    name = Column(String(50))
    description = Column(String(500))

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description


class ExcerptType(db.Model):
    __tablename__ = 'excerptTypes'
    id = Column(String(3), primary_key=True, autoincrement=False)
    name = Column(String(50))
    description = Column(String(500))

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description


class LyricAdaptation(db.Model):
    __tablename__ = 'lyricAdaptations'
    id = Column(String(3), primary_key=True, autoincrement=False)
    name = Column(String(50))
    description = Column(String(500))

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description


class MusicArrangement(db.Model):
    __tablename__ = 'musicArrangements'
    id = Column(String(3), primary_key=True, autoincrement=False)
    name = Column(String(50))
    description = Column(String(500))

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description


class Society(db.Model):
    __tablename__ = 'societies'
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(32), nullable=False)
    former_name = Column(String(32))

    def __init__(self, code, name, former_name):
        self.id = code
        self.name = name
        self.former_name = former_name


class Territory(db.Model):
    __tablename__ = 'territories'
    tis = Column(Integer, primary_key=True, autoincrement=False)
    iso2 = Column(String(2), unique=True)
    type = Column(String(20), nullable=False)
    name = Column(String(50), nullable=False, unique=True)
    official_name = Column(String(50))

    def __init__(self, tis, iso2=None, territory_type=None, name=None, official_name=None):
        self.tis = tis
        self.iso2 = iso2
        self.type = territory_type
        self.name = name
        self.official_name = official_name


class TextMusicRelationship(db.Model):
    __tablename__ = 'textMusicRelationships'
    id = Column(String(3), primary_key=True, autoincrement=False)
    name = Column(String(50))
    description = Column(String(500))

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description


class VersionType(db.Model):
    __tablename__ = 'versionTypes'
    id = Column(String(3), primary_key=True, autoincrement=False)
    name = Column(String(50))
    description = Column(String(500))

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description


class WorkType(db.Model):
    __tablename__ = 'workTypes'
    id = Column(String(2), primary_key=True, autoincrement=False)
    name = Column(String(50))

    def __init__(self, id, name):
        self.id = id
        self.name = name