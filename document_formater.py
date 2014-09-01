__author__ = 'Borja'


class DocumentFormatter(object):

    def __init__(self, document):
        self._document = document

    def get_agreements(self):
        elements = []

        for agreement in self._document._groups[self._document._group_types['AGR']].transactions.values():

            if not agreement.rejected:
                element = {'agreement': agreement.attr_dict, 'territories': [], 'interested_parties': []}

                for territory in agreement._records['TER']:
                    if not territory.rejected:
                        element['territories'].append(territory.attr_dict)

                for interested_party in agreement._records['IPA']:
                    if not interested_party.rejected:
                        element['interested_parties'].append(interested_party.attr_dict)

                elements.append(element)

        return elements

    def get_works(self):
        elements = []

        for work in self._document._groups[self._document._group_types['NWR']].transactions.values():
            if not work.rejected:
                elements.append(work)

        return elements