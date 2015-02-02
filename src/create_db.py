import os

import xlrd
from files import __data__


__author__ = 'Borja'

from api.persistence.services import *
from api.persistence.domain import *


def _add_agreement_roles():
    agreement_role_service = AgreementRoleService()
    agreement_role_service.insert(AgreementRole('AS', 'Assignor',
                                                'The entitled party who is assigning the rights to a musical work within an agreement'))
    agreement_role_service.insert(AgreementRole('AC', 'Acquirer',
                                                'The entitled party who is acquiring the rights to a musical work within an agreement'))


def _add_agreement_types():
    agreement_type_service = AgreementTypeService()
    agreement_type_service.insert(AgreementType('OS', 'Original Specific',
                                                'Agreement between the songwriter and original publisher covering a list of specific work(s)'))
    agreement_type_service.insert(AgreementType('PS', 'Subpublishing Specific',
                                                'Agreement between two publishers covering a list of specific work(s)'))
    agreement_type_service.insert(AgreementType('PG', 'Subpublishing General',
                                                'Agreement between two publishers covering all works in a catalogue'))
    agreement_type_service.insert(AgreementType('OG', 'Original General',
                                                'Agreement between the songwriter and original publisher covering all works in a catalogue'))


def _add_composite_types():
    composite_types_service = CompositeTypeService()
    composite_types_service.insert(CompositeType('COS', 'Composite of Samples',
                                                 'A composite work containing new material and one or more samples of pre-existing recorded works'))
    composite_types_service.insert(CompositeType('MED', 'Medley',
                                                 'A continuous and sequential combination of existing works or excerpts'))
    composite_types_service.insert(CompositeType('POT', 'Porpourri',
                                                 'A composite work with the addition of original material which have been combined to form a new work, that has been published and printed'))
    composite_types_service.insert(CompositeType('UCO', 'Unspecified Composite',
                                                 'Works known to be a composite but where the type of composite is unknown'))


def _add_distribution_categories():
    distribution_service = DistributionCategoryService()
    distribution_service.insert(DistributionCategory('JAZ', 'Jazz',
                                                     'Music originating in black America from the early 20th century, incorporating strands of Euro-American and African music and frequently containing improvisation'))
    distribution_service.insert(DistributionCategory('POP', 'Popular',
                                                     'The musical mainstream, usually song-based and melody-orientated, created for mass consumption'))
    distribution_service.insert(DistributionCategory('SER', 'Serious',
                                                     'Classical or art music'))
    distribution_service.insert(DistributionCategory('UNC', 'Unclassified Distribution Category',
                                                     'The catch-all for societies who do not track genres; all works are paid the same regardless of genre'))


def _add_excerpt_types():
    excerpt_types_service = ExcerptTypeService()
    excerpt_types_service.insert(ExcerptType('MOV', 'Movement', 'A principal division of a musical work'))
    excerpt_types_service.insert(ExcerptType('UEX', 'Unspecified Excerpt',
                                             'A work that is known to be an excerpt from another work, however the type of excerpt is unknown'))


def _add_lyric_adaptations():
    lyric_adaptations_service = LyricAdaptationService()
    lyric_adaptations_service.insert(LyricAdaptation('NEW', 'New',
                                                     'New lyrics added to the existing lyrics'))
    lyric_adaptations_service.insert(LyricAdaptation('MOD', 'Modification',
                                                     'Lyrics modified in the original language'))
    lyric_adaptations_service.insert(LyricAdaptation('NON', 'None', 'No lyrics have been included in the work'))
    lyric_adaptations_service.insert(LyricAdaptation('ORI', 'Original', 'Lyrics have been used in the original form'))
    lyric_adaptations_service.insert(LyricAdaptation('REP', 'Replacement', 'Lyrics have been totally replaced'))
    lyric_adaptations_service.insert(LyricAdaptation('ADL', 'Addition',
                                                     'Lyrics added to a pre-existing instrumental work'))
    lyric_adaptations_service.insert(LyricAdaptation('UNS', 'Unspecified',
                                                     'Details of the lyric adaptation are not known at this time'))
    lyric_adaptations_service.insert(LyricAdaptation('TRA', 'Translation',
                                                     'Lyrics translated into another language'))


def _add_music_arrangements():
    music_arrangements_service = MusicArrangementService()
    music_arrangements_service.insert(MusicArrangement('NEW', 'New',
                                                       'New music added to existing music'))
    music_arrangements_service.insert(MusicArrangement('ARR', 'Arrangement',
                                                       'A version of a work in which musical elements have been modified'))
    music_arrangements_service.insert(MusicArrangement('ADM', 'Addition',
                                                       'Music added to a pre-existing text'))
    music_arrangements_service.insert(MusicArrangement('UNS', 'Unspecified Arrangement',
                                                       'To be used when it is known the work is an arrangement, but no further details are available'))
    music_arrangements_service.insert(MusicArrangement('ORI', 'Original',
                                                       'Music used in its original form'))


def _add_societies():
    society_service = SocietyService()

    workbook = xlrd.open_workbook(
        os.path.join(__data__.path(), os.path.basename('SG12-1020_CISAC_Societies_Codes_2014-06-09_EN.xls')))
    worksheet = workbook.sheet_by_name('CISAC Societies Codes listing')

    for curr_row in range(1, worksheet.nrows):
        society = Society(int(worksheet.cell_value(curr_row, 0)),
                          worksheet.cell_value(curr_row, 1),
                          worksheet.cell_value(curr_row, 2))
        society_service.insert(society)


def _add_territories():
    territory_service = TerritoryService()

    workbook = xlrd.open_workbook(
        os.path.join(__data__.path(), os.path.basename('TIS09-1540a_Territories_2009-08-27_EN.xls')))
    worksheet = workbook.sheet_by_name('en')

    for curr_row in range(1, worksheet.nrows):
        territory_service.insert(Territory(int(worksheet.cell_value(curr_row, 0)),
                                           worksheet.cell_value(curr_row, 5),
                                           worksheet.cell_value(curr_row, 3),
                                           worksheet.cell_value(curr_row, 9).capitalize(),
                                           worksheet.cell_value(curr_row, 10).capitalize()))


def _add_text_music_relationships():
    text_music_service = TextMusicRelationshipService()
    text_music_service.insert(TextMusicRelationship('MUS', 'Music', 'Music only'))
    text_music_service.insert(TextMusicRelationship('MTX', 'Music and Text', 'Music and text combined'))
    text_music_service.insert(TextMusicRelationship('TXT', 'Text', ''))


def _add_version_types():
    version_type_service = VersionTypeService()
    version_type_service.insert(VersionType('MOD', 'Modified version of a musical work',
                                            'A work resulting from the modification of a musical work'))
    version_type_service.insert(VersionType('ORI', 'Original work',
                                            'The first established form of a work'))


def _add_work_types():
    work_types_service = WorkTypeService()
    work_types_service.insert(WorkType('TA', 'Triple A'))
    work_types_service.insert(WorkType('AC', 'Adult Contemporary'))
    work_types_service.insert(WorkType('AR', 'Album Oriented Rock'))
    work_types_service.insert(WorkType('AL', 'Alternative Music'))
    work_types_service.insert(WorkType('AM', 'Americana'))
    work_types_service.insert(WorkType('BD', 'Band'))
    work_types_service.insert(WorkType('BL', 'Bluegrass Music'))
    work_types_service.insert(WorkType('CD', 'Childrens Music'))
    work_types_service.insert(WorkType('CL', 'Classical Music'))
    work_types_service.insert(WorkType('CC', 'Contemporary Christian'))
    work_types_service.insert(WorkType('CT', 'Country Music'))
    work_types_service.insert(WorkType('DN', 'Dance'))
    work_types_service.insert(WorkType('FM', 'Film/ Television Music'))
    work_types_service.insert(WorkType('FK', 'Folk Music'))
    work_types_service.insert(WorkType('BG', 'Black Gospel'))
    work_types_service.insert(WorkType('SG', 'Southern Gospel'))
    work_types_service.insert(WorkType('JZ', 'Jazz Music'))
    work_types_service.insert(WorkType('JG', 'Jingles'))
    work_types_service.insert(WorkType('LN', 'Latin'))
    work_types_service.insert(WorkType('LA', 'Latina'))
    work_types_service.insert(WorkType('NA', 'New Age'))
    work_types_service.insert(WorkType('OP', 'Opera'))
    work_types_service.insert(WorkType('PK', 'Polka Music'))
    work_types_service.insert(WorkType('PP', 'Pop Music'))
    work_types_service.insert(WorkType('RP', 'Rap Music'))
    work_types_service.insert(WorkType('RK', 'Rock Music'))
    work_types_service.insert(WorkType('RB', 'Rhythm and Blues'))
    work_types_service.insert(WorkType('SD', 'Sacred'))
    work_types_service.insert(WorkType('SY', 'Symphonic'))


def _initialize_database():
    _add_agreement_roles()
    _add_agreement_types()
    _add_composite_types()
    _add_distribution_categories()
    _add_excerpt_types()
    _add_lyric_adaptations()
    _add_music_arrangements()
    _add_societies()
    _add_territories()
    _add_text_music_relationships()
    _add_version_types()
    _add_work_types()

if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    _initialize_database()
