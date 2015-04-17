import logging

from sqlalchemy.exc import IntegrityError

from cwr.validator.api.persistence.domain import *


logging.basicConfig(filename='cwr.log', level=logging.DEBUG)


class DAO(object):
    """
    Generic DAO for all classes, only the class is needed
    """

    def __init__(self, cls):
        """
        Constructor for DAO

        :param cls: class to use in the dao
        """
        self.cls = cls
        self.session = None

    def set_session(self, session):
        """
        Method to set the database to use

        :param session: session of the database used
        """
        self.session = session

    def get_all(self):
        """
        Method that returns all countries in the database

        :return: a collection of all elements
        """
        return self.session.query(self.cls).all()

    def get_by_code(self, code):
        """
        Method that returns a element by its given code

        :param code: id of the element requested
        :return: element with the given id
        """
        return self.session.query(self.cls).filter_by(id=code).first()

    def insert(self, element):
        """
        Method that inserts a new element

        :param element: element to be inserted
        """
        try:
            self.session.add(element)
            self.session.flush()
        except IntegrityError as detail:
            logging.warning(detail)
            self.session.rollback()

    def delete(self, code):
        """
        Method to delete an existing element by its code

        :param code: id of the object to be deleted
        """
        element = self.get_by_code(code)
        self.session.delete(element)

    def update(self, element):
        """
        Method to update an existing element, its code will not be changed

        :param element: object to be updated, with updated attributes
        """
        persisted_object = self.get_by_code(element.id)
        update_object_attributes(persisted_object, element)

    def paginate(self, page_number):
        elements = self.session.query(self.cls).limit(10).offset(page_number * 10).all()

        return elements


class AgreementTypeDAO(DAO):
    def __init__(self):
        super(AgreementTypeDAO, self).__init__(AgreementType)


class AgreementRoleDAO(DAO):
    def __init__(self):
        super(AgreementRoleDAO, self).__init__(AgreementRole)


class CompositeTypeDAO(DAO):
    def __init__(self):
        super(CompositeTypeDAO, self).__init__(CompositeType)


class DistributionCategoryDAO(DAO):
    def __init__(self):
        super(DistributionCategoryDAO, self).__init__(DistributionCategory)


class ExcerptTypeDAO(DAO):
    def __init__(self):
        super(ExcerptTypeDAO, self).__init__(ExcerptType)


class LyricAdaptationDAO(DAO):
    def __init__(self):
        super(LyricAdaptationDAO, self).__init__(LyricAdaptation)


class MusicArrangementDAO(DAO):
    def __init__(self):
        super(MusicArrangementDAO, self).__init__(MusicArrangement)


class SocietyDAO(DAO):
    def __init__(self):
        super(SocietyDAO, self).__init__(SocietyDAO)


class TerritoryDAO(DAO):
    def __init__(self):
        super(TerritoryDAO, self).__init__(Territory)

    def get_by_code(self, code):
        """
        Method that returns a element by its given code

        :param code: id of the element requested
        :return: element with the given id
        """
        return self.session.query(self.cls).filter_by(tis=code).first()

    def get_by_iso2(self, iso2):
        return self.session.query(self.cls).filter_by(iso2=iso2).first()


class TextMusicRelationshipDAO(DAO):
    def __init__(self):
        super(TextMusicRelationshipDAO, self).__init__(TextMusicRelationship)


class VersionTypeDAO(DAO):
    def __init__(self):
        super(VersionTypeDAO, self).__init__(VersionType)


class WorkTypeDAO(DAO):
    def __init__(self):
        super(WorkTypeDAO, self).__init__(WorkType)


def update_object_attributes(object_to_update, object_with_new_attributes):
    """
    Updates all the attributes of an object with other object values
    all attributes beginning with '_' will not be updated

    :param object_to_update: object to be updated
    :param object_with_new_attributes: object with the new values
    """
    for attr in dir(object_to_update):
        if hasattr(object_with_new_attributes, attr) and attr[0] is not "_":
            setattr(object_to_update, attr, getattr(object_with_new_attributes, attr))