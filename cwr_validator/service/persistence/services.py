from cwr_validator.validator.service.persistence.daos import *


class GenericService(object):
    """
    Generic Service, it provides all default methods that could be used
    with the majority of the daos
    """
    dao = None

    def __init__(self):
        """
        Constructor for generic service
        """
        self.tm = TransactionManager()

    def get_all(self):
        """
        Method that returns all elements given by the dao

        :return: collection of elements
        """
        return self.tm.execute(self.dao, self.dao.get_all)

    def get_by_code(self, code):
        """
        Method that returns element given by the dao

        :param code: usually the id
        :return: element that owns the given id
        """
        return self.tm.execute(self.dao, self.dao.get_by_code, code)

    def insert(self, element):
        """
        Method that inserts a element calling the dao

        :param element: element to be persisted
        """
        self.tm.execute(self.dao, self.dao.insert, element)

    def delete(self, code):
        """
        Method that deletes the element by its given code calling the dao

        :param code: id of the element to be deleted
        """
        self.tm.execute(self.dao, self.dao.delete, code)

    def update(self, element):
        """
        Method that updates the element by calling the dao

        :param element: element to be updated with updated attributes
        """
        self.tm.execute(self.dao, self.dao.update, element)

    def delete_all(self):
        """
        Method that deletes all elements by calling the dao
        """

        elements = self.tm.execute(self.dao, self.dao.get_all)
        for element in elements:
            self.tm.execute(self.dao, self.dao.delete, element.id)

    def update_all(self, elements):
        """
        Method that updates all the elements given by calling the dao

        :params elements: list of objects to be updated with updated attributes
        """

        for element in elements:
            self.tm.execute(self.dao, self.dao.update, element)

    def paginate(self, page_number):

        return self.tm.execute(self.dao, self.dao.paginate, page_number)


class AgreementTypeService(GenericService):
    """
    Service for agreement type dao
    """

    def __init__(self):
        """
        Constructor for indicator service
        """
        super(AgreementTypeService, self).__init__()
        self.dao = AgreementTypeDAO()


class AgreementRoleService(GenericService):
    """
    Service for agreement type dao
    """

    def __init__(self):
        """
        Constructor for indicator service
        """
        super(AgreementRoleService, self).__init__()
        self.dao = AgreementRoleDAO()


class CompositeTypeService(GenericService):
    def __init__(self):
        super(CompositeTypeService, self).__init__()
        self.dao = CompositeTypeDAO()


class DistributionCategoryService(GenericService):
    def __init__(self):
        super(DistributionCategoryService, self).__init__()
        self.dao = DistributionCategoryDAO()


class ExcerptTypeService(GenericService):
    def __init__(self):
        super(ExcerptTypeService, self).__init__()
        self.dao = ExcerptTypeDAO()


class LyricAdaptationService(GenericService):
    def __init__(self):
        super(LyricAdaptationService, self).__init__()
        self.dao = LyricAdaptationDAO()


class MusicArrangementService(GenericService):
    def __init__(self):
        super(MusicArrangementService, self).__init__()
        self.dao = MusicArrangementDAO()


class SocietyService(GenericService):
    def __init__(self):
        super(SocietyService, self).__init__()
        self.dao = SocietyDAO()


class TerritoryService(GenericService):
    """
    Service for agreement type dao
    """

    def __init__(self):
        """
        Constructor for indicator service
        """
        super(TerritoryService, self).__init__()
        self.dao = TerritoryDAO()

    def get_by_iso2(self, iso2):
        return self.tm.execute(self.dao, self.dao.get_by_iso2, iso2)


class TextMusicRelationshipService(GenericService):
    def __init__(self):
        super(TextMusicRelationshipService, self).__init__()
        self.dao = TextMusicRelationshipDAO()


class VersionTypeService(GenericService):
    def __init__(self):
        super(VersionTypeService, self).__init__()
        self.dao = VersionTypeDAO()


class WorkTypeService(GenericService):
    def __init__(self):
        super(WorkTypeService, self).__init__()
        self.dao = WorkTypeDAO()


class TransactionManager(object):
    """
    Transaction manager that helps to abstract from the execution
    """

    @staticmethod
    def execute(dao, function, *args):
        """
        Abstraction for all calls to the dao methods, like command executor
        """
        session = db.session
        getattr(dao, 'set_session')(session)
        result = function(*args)
        session.commit()
        return result
