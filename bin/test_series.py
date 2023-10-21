from interfaces.iseries import ISeriesVolume
from interfaces.iseries import ISeries
from interfaces.iseries import IEdition
from enums.host_enum import HostEnum
from interfaces.ivolume import IVolume
from src.series.series_enricher import SeriesEnricher

class TestSeries:

    def __init__(self):
        self.s_e = SeriesEnricher(HostEnum.MOCK)

    def run_all(self):
        self.test_adding_new_series()
        self.test_existing_series_new_edition()
        self.test_updating_existing_series()
        self.test_update_existing_series_volume_release_date()
        self.test_multiple_series()
        self.test_one_shot_series()
        
        self.test_edition_name_generic()
        self.test_edition_name_not_in_display_name()
        self.test_edition_name_no_volume()
        self.test_edition_name_manga()
        self.test_edition_name_novel()
        self.test_edition_name_manhwa()
        self.test_edition_name_manhua()
        self.test_edition_name_format_not_in_name()
        self.test_edition_name_no_format()
        self.test_edition_name_special_characters()

    # -------------------------------------------------------------------------------------------------
    # Test Adding New Series
    # -------------------------------------------------------------------------------------------------
    def test_adding_new_series(self):
        try:
            (series_id, series_update, edition_id) = self.s_e.update_series(
                IVolume({
                    'isbn': '9781648274251',
                    'series': 'The Dangers in My Heart',
                    'volume': '3',
                    'format': 'Manga',
                    'release_date': '7/20/2021',
                    'display_name': 'The Dangers in My Heart Manga Volume 3'
                }),
                {}
            )
            series_update = ISeries(series_update)
            edition = IEdition(list(series_update.editions.values())[0])
            print('SUCCESS' if series_update.title == 'The Dangers in My Heart' and
                len(series_update.series_id) > 0 and 
                len(series_update.editions) == 1 and
                edition.edition == 'The Dangers in My Heart' and
                len(edition.edition_id) > 0 and 
                edition.format == 'Manga' and 
                len(edition.volumes) == 1 and
                ISeriesVolume(edition.volumes[0]).isbn == '9781648274251' and
                ISeriesVolume(edition.volumes[0]).volume == '3' and
                ISeriesVolume(edition.volumes[0]).release_date == '7/20/2021' and
                series_id == series_update.series_id and
                edition_id == edition.edition_id else 'FAILED', '- Test Adding New Series')
        except:
            print('FAILED - Test Adding New Series')


    # -------------------------------------------------------------------------------------------------
    # Test Existing Series, New Edition
    # -------------------------------------------------------------------------------------------------
    def test_existing_series_new_edition(self):
        try:
            series = {
                '64326345345': {
                    'title': 'The Dangers in My Heart',
                    'series_id': '64326345345',
                    'editions': {
                        '00000000000000000000000000000000000': {
                            'edition': 'The Dangers in My Heart',
                            'edition_id': '00000000000000000000000000000000000',
                            'format': 'Manga',
                            'volumes': [
                                {'isbn': '9781648274251', 'volume': '1', 'release_date': '1/25/2021'}
                            ]
                        }
                    }
                }
            }
            (series_id, series_update, edition_id) = self.s_e.update_series(
                IVolume({
                    'isbn': '9781648274299',
                    'series': 'The Dangers in My Heart',
                    'volume': '1',
                    'format': 'Manga',
                    'release_date': '7/20/2021',
                    'display_name': 'The Dangers in My Heart Omnibus Manga Volume 1'
                }),
                series
            )
            series_update = ISeries(series_update)
            edition1 = IEdition(list(series_update.editions.values())[0])
            edition2 = IEdition(list(series_update.editions.values())[1])
            print('SUCCESS' if series_update.title == 'The Dangers in My Heart' and
                len(series_update.series_id) > 0 and 
                len(series_update.editions) == 2 and
                edition1.edition == 'The Dangers in My Heart' and
                len(edition1.edition_id) > 0 and 
                edition1.format == 'Manga' and 
                len(edition1.volumes) == 1 and
                ISeriesVolume(edition1.volumes[0]).isbn == '9781648274251' and
                ISeriesVolume(edition1.volumes[0]).volume == '1' and
                ISeriesVolume(edition1.volumes[0]).release_date == '1/25/2021' and
                edition2.edition == 'The Dangers in My Heart Omnibus' and
                len(edition2.edition_id) > 0 and 
                edition2.format == 'Manga' and 
                len(edition2.volumes) == 1 and
                ISeriesVolume(edition2.volumes[0]).isbn == '9781648274299' and
                ISeriesVolume(edition2.volumes[0]).volume == '1' and
                ISeriesVolume(edition2.volumes[0]).release_date == '7/20/2021' and
                series_id == series_update.series_id and
                edition_id == edition2.edition_id else 'FAILED', '- Test Existing Series, New Edition')
        except:
            print('FAILED - Test Existing Series, New Edition')


    # -------------------------------------------------------------------------------------------------
    # Test Existing Series, Different Format
    # -------------------------------------------------------------------------------------------------
    def test_existing_series_different_format(self):
        try:
            series = {
                '64326345345': {
                    'title': 'The Dangers in My Heart',
                    'series_id': '64326345345',
                    'editions': {
                        '00000000000000000000000000000000000': {
                            'edition': 'The Dangers in My Heart',
                            'edition_id': '00000000000000000000000000000000000',
                            'format': 'Manga',
                            'volumes': [
                                {'isbn': '9781648274251', 'volume': '1', 'release_date': '1/25/2021'}
                            ]
                        }
                    }
                }
            }
            (series_id, series_update, edition_id) = self.s_e.update_series(
                IVolume({
                    'isbn': '9781648274299',
                    'series': 'The Dangers in My Heart',
                    'volume': '1',
                    'format': 'Novel',
                    'release_date': '7/20/2021',
                    'display_name': 'The Dangers in My Heart Novel Volume 1'
                }),
                series
            )
            series_update = ISeries(series_update)
            edition1 = IEdition(list(series_update.editions.values())[0])
            edition2 = IEdition(list(series_update.editions.values())[1])
            print('SUCCESS' if series_update.title == 'The Dangers in My Heart' and
                len(series_update.series_id) > 0 and 
                len(series_update.editions) == 2 and
                edition1.edition == 'The Dangers in My Heart' and
                len(edition1.edition_id) > 0 and 
                edition1.format == 'Manga' and 
                len(edition1.volumes) == 1 and
                ISeriesVolume(edition1.volumes[0]).isbn == '9781648274251' and
                ISeriesVolume(edition1.volumes[0]).volume == '1' and
                ISeriesVolume(edition1.volumes[0]).release_date == '1/25/2021' and
                edition2.edition == 'The Dangers in My Heart' and
                len(edition2.edition_id) > 0 and 
                edition2.format == 'Novel' and 
                len(edition2.volumes) == 1 and
                ISeriesVolume(edition2.volumes[0]).isbn == '9781648274299' and
                ISeriesVolume(edition2.volumes[0]).volume == '1' and
                ISeriesVolume(edition2.volumes[0]).release_date == '7/20/2021' and
                series_id == series_update.series_id and
                edition_id == edition2.edition_id else 'FAILED', '- Test Existing Series, New Edition')
        except:
            print('FAILED - Test Existing Series, New Edition')


    # -------------------------------------------------------------------------------------------------
    # Test Updating Existing Series
    # -------------------------------------------------------------------------------------------------
    def test_updating_existing_series(self):
        try:
            series = {
                '64326345345': {
                    'title': 'The Dangers in My Heart',
                    'series_id': '64326345345',
                    'editions': {
                        '00000000000000000000000000000000000': {
                            'edition': 'The Dangers in My Heart',
                            'edition_id': '00000000000000000000000000000000000',
                            'format': 'Manga',
                            'volumes': [
                                {'isbn': '9781648274251', 'volume': '1', 'release_date': '1/25/2021'},
                                {'isbn': '9781685796198', 'volume': '7', 'release_date': '10/24/2022'}
                            ]
                        }
                    }
                }
            }
            (series_id, series_update, edition_id) = self.s_e.update_series(
                IVolume({
                    'isbn': '9781648274299',
                    'series': 'The Dangers in My Heart',
                    'volume': '3',
                    'format': 'Manga',
                    'release_date': '7/20/2021',
                    'display_name': 'The Dangers in My Heart Manga Volume 3'
                }),
                series
            )
            series_update = ISeries(series_update)
            edition = IEdition(list(series_update.editions.values())[0])
            print('SUCCESS' if series_update.title == 'The Dangers in My Heart' and
                series_update.series_id == '64326345345' and 
                len(series_update.editions) == 1 and
                edition.edition == 'The Dangers in My Heart' and
                edition.edition_id == '00000000000000000000000000000000000' and 
                edition.format == 'Manga' and 
                len(edition.volumes) == 3 and
                ISeriesVolume(edition.volumes[0]).isbn == '9781648274251' and
                ISeriesVolume(edition.volumes[0]).volume == '1' and
                ISeriesVolume(edition.volumes[0]).release_date == '1/25/2021' and
                ISeriesVolume(edition.volumes[1]).isbn == '9781648274299' and
                ISeriesVolume(edition.volumes[1]).volume == '3' and
                ISeriesVolume(edition.volumes[1]).release_date == '7/20/2021' and
                ISeriesVolume(edition.volumes[2]).isbn == '9781685796198' and
                ISeriesVolume(edition.volumes[2]).volume == '7' and
                ISeriesVolume(edition.volumes[2]).release_date == '10/24/2022' and
                series_id == series_update.series_id and
                edition_id == edition.edition_id else 'FAILED', '- Test Updating Existing Series')
        except:
            print('FAILED - Test Updating Existing Series')


    # -------------------------------------------------------------------------------------------------
    # Test Update Existing Series/Volume Release Date
    # -------------------------------------------------------------------------------------------------
    def test_update_existing_series_volume_release_date(self):
        try:
            series = {
                '64326345345': {
                    'title': 'The Dangers in My Heart',
                    'series_id': '64326345345',
                    'editions': {
                        '00000000000000000000000000000000000': {
                            'edition': 'The Dangers in My Heart',
                            'edition_id': '00000000000000000000000000000000000', ## should this be made into dict???
                            'format': 'Manga',
                            'volumes': [
                                {'isbn': '9781648274251', 'volume': '1', 'release_date': '1/25/2021'}
                            ]
                        }
                    }
                }
            }
            (series_id, series_update, edition_id) = self.s_e.update_series(
                IVolume({
                    'isbn': '9781648274251',
                    'series': 'The Dangers in My Heart',
                    'volume': '1',
                    'format': 'Manga',
                    'release_date': '7/20/2021',
                    'display_name': 'The Dangers in My Heart Manga Volume 1'
                }),
                series
            )
            series_update = ISeries(series_update)
            edition = IEdition(list(series_update.editions.values())[0])
            print('SUCCESS' if series_update.title == 'The Dangers in My Heart' and
                len(series_update.series_id) > 0 and 
                len(series_update.editions) == 1 and
                edition.edition == 'The Dangers in My Heart' and
                edition.edition_id == '00000000000000000000000000000000000' and 
                edition.format == 'Manga' and 
                len(edition.volumes) == 1 and
                ISeriesVolume(edition.volumes[0]).isbn == '9781648274251' and
                ISeriesVolume(edition.volumes[0]).volume == '1' and
                ISeriesVolume(edition.volumes[0]).release_date == '7/20/2021' and
                series_id == series_update.series_id and
                edition_id == edition.edition_id else 'FAILED', '- Test Update Existing Series/Volume Release Date')
        except:
            print('FAILED - Test Update Existing Series/Volume Release Date')


    # -------------------------------------------------------------------------------------------------
    # Test Multiple Series
    # -------------------------------------------------------------------------------------------------
    def test_multiple_series(self):
        try:
            series = {
                '64326345345': {
                    'title': 'The Dangers in My Heart',
                    'series_id': '64326345345',
                    'editions': {
                        '00000000000000000000000000000000000': {
                            'edition': 'The Dangers in My Heart',
                            'edition_id': '00000000000000000000000000000000000',
                            'format': 'Manga',
                            'volumes': [
                                {'isbn': '9781648274251', 'volume': '1', 'release_date': '1/25/2021'}
                            ]
                        }
                    }
                }
            }
            (series_id, series_update, edition_id) = self.s_e.update_series(
                IVolume({
                    'isbn': '9781648291558',
                    'series': 'Vagabond',
                    'volume': '1',
                    'format': 'Manga',
                    'release_date': '7/20/2021',
                    'display_name': 'Vagabond Manga Omnibus Volume 1'
                }),
                series
            )
            series_update = ISeries(series_update)
            edition = IEdition(list(series_update.editions.values())[0])
            print('SUCCESS' if series_update.title == 'Vagabond' and
                len(series_update.series_id) > 0 and 
                len(series_update.editions) == 1 and
                edition.edition == 'Vagabond' and
                len(edition.edition_id) > 0 and 
                edition.format == 'Manga' and 
                len(edition.volumes) == 1 and
                ISeriesVolume(edition.volumes[0]).isbn == '9781648291558' and
                ISeriesVolume(edition.volumes[0]).volume == '1' and
                ISeriesVolume(edition.volumes[0]).release_date == '7/20/2021' and
                series_id == series_update.series_id and
                edition_id == edition.edition_id else 'FAILED', '- Test Multiple Series')
        except:
            print('FAILED - Test Multiple Series')


    # -------------------------------------------------------------------------------------------------
    # Test One-Shot Series
    # -------------------------------------------------------------------------------------------------
    def test_one_shot_series(self):
        try:
            series = {
                '64326345345': {
                    'title': 'Takane & Hana',
                    'series_id': '64326345345',
                    'editions': {
                        '00000000000000000000000000000000000': {
                            'edition': 'Takane & Hana',
                            'edition_id': '00000000000000000000000000000000000',
                            'format': 'Manga',
                            'volumes': [
                                {'isbn': '9781974723010', 'volume': '18', 'release_date': '12/7/2021'}
                            ]
                        }
                    }
                }
            }
            (series_id, series_update, edition_id) = self.s_e.update_series(
                IVolume({
                    'isbn': '9781974725335',
                    'series': 'Takane & Hana',
                    'volume': None,
                    'format': 'Manga',
                    'release_date': '12/7/2021',
                    'display_name': 'Takane & Hana Limited Edition Manga Volume 18'
                }),
                series
            )
            series_update = ISeries(series_update)
            edition1 = IEdition(list(series_update.editions.values())[0])
            edition2 = IEdition(list(series_update.editions.values())[1])
            print('SUCCESS' if series_update.title == 'Takane & Hana' and
                len(series_update.series_id) > 0 and 
                len(series_update.editions) == 2 and
                edition1.edition == 'Takane & Hana' and
                edition1.edition_id == '00000000000000000000000000000000000' and 
                edition1.format == 'Manga' and 
                len(edition1.volumes) == 1 and
                ISeriesVolume(edition1.volumes[0]).isbn == '9781974723010' and
                ISeriesVolume(edition1.volumes[0]).volume == '18' and
                ISeriesVolume(edition1.volumes[0]).release_date == '12/7/2021' and
                edition2.edition == 'Takane & Hana Limited Edition' and
                len(edition2.edition_id) > 0 and 
                edition2.format == 'Manga' and 
                len(edition2.volumes) == 1 and
                ISeriesVolume(edition2.volumes[0]).isbn == '9781974725335' and
                ISeriesVolume(edition2.volumes[0]).volume == '1' and
                ISeriesVolume(edition2.volumes[0]).release_date == '12/7/2021' and
                series_id == series_update.series_id and
                edition_id == edition2.edition_id else 'FAILED', '- Test One-Shot Series')
        except:
            print('FAILED - Test One-Shot Series')


    # -------------------------------------------------------------------------------------------------
    # Test Edition Name Generic
    # -------------------------------------------------------------------------------------------------
    def test_edition_name_generic(self):
        try:
            series_name = self.s_e.get_edition_name(
                IVolume({
                    'series': 'Takane and Hana',
                    'volume': '18',
                    'format': 'Manga',
                    'display_name': 'Takane and Hana Limited Edition Manga Volume 18'
                })
            )
            print('SUCCESS'
                  if series_name == 'Takane and Hana Limited Edition'
                  else 'FAILED', '- Test Edition Name Generic')
        except:
            print('FAILED - Test Edition Name Generic')

            
    # -------------------------------------------------------------------------------------------------
    # Test Edition Name Not In Display Name
    # -------------------------------------------------------------------------------------------------
    def test_edition_name_not_in_display_name(self):
        try:
            series_name = self.s_e.get_edition_name(
                IVolume({
                    'series': 'Rascal Does Not Dream Of Bunny Girl Senpai',
                    'volume': '1',
                    'format': 'Novel',
                    'display_name': 'Rascal Does Not Dream Of A Dreaming Girl Novel Volume 1'
                })
            )
            print('SUCCESS'
                  if series_name == 'Rascal Does Not Dream Of Bunny Girl Senpai'
                  else 'FAILED', '- Test Edition Name Not In Display Name')
        except:
            print('FAILED - Test Edition Name Not In Display Name')


    # -------------------------------------------------------------------------------------------------
    # Test Edition Name No Volume
    # -------------------------------------------------------------------------------------------------
    def test_edition_name_no_volume(self):
        try:
            series_name = self.s_e.get_edition_name(
                IVolume({
                    'series': 'Takane and Hana',
                    'volume': None,
                    'format': 'Manga',
                    'display_name': 'Takane and Hana Limited Edition Manga'
                })
            )
            print('SUCCESS'
                  if series_name == 'Takane and Hana Limited Edition'
                  else 'FAILED', '- Test Edition Name No Volume')
        except:
            print('FAILED - Test Edition Name No Volume')


    # -------------------------------------------------------------------------------------------------
    # Test Edition Name Manga
    # -------------------------------------------------------------------------------------------------
    def test_edition_name_manga(self):
        try:
            series_name = self.s_e.get_edition_name(
                IVolume({
                    'series': 'Rascal Does Not Dream Of Bunny Girl Senpai',
                    'volume': '1',
                    'format': 'Manga',
                    'display_name': 'Rascal Does Not Dream Of Bunny Girl Senpai Manga Volume 1'
                })
            )
            print('SUCCESS'
                  if series_name == 'Rascal Does Not Dream Of Bunny Girl Senpai'
                  else 'FAILED', '- Test Edition Name Manga')
        except:
            print('FAILED - Test Edition Name Manga')


    # -------------------------------------------------------------------------------------------------
    # Test Edition Name Novel
    # -------------------------------------------------------------------------------------------------
    def test_edition_name_novel(self):
        try:
            series_name = self.s_e.get_edition_name(
                IVolume({
                    'series': 'Rascal Does Not Dream Of Bunny Girl Senpai',
                    'volume': '1',
                    'format': 'Novel',
                    'display_name': 'Rascal Does Not Dream Of Bunny Girl Senpai Novel Volume 1'
                })
            )
            print('SUCCESS'
                  if series_name == 'Rascal Does Not Dream Of Bunny Girl Senpai'
                  else 'FAILED', '- Test Edition Name Novel')
        except:
            print('FAILED - Test Edition Name Novel')


    # -------------------------------------------------------------------------------------------------
    # Test Edition Name Manhwa
    # -------------------------------------------------------------------------------------------------
    def test_edition_name_manhwa(self):
        try:
            series_name = self.s_e.get_edition_name(
                IVolume({
                    'series': 'Rascal Does Not Dream Of Bunny Girl Senpai',
                    'volume': '1',
                    'format': 'Manhwa',
                    'display_name': 'Rascal Does Not Dream Of Bunny Girl Senpai Manhwa Volume 1'
                })
            )
            print('SUCCESS'
                  if series_name == 'Rascal Does Not Dream Of Bunny Girl Senpai'
                  else 'FAILED', '- Test Edition Name Manhwa')
        except:
            print('FAILED - Test Edition Name Manhwa')


    # -------------------------------------------------------------------------------------------------
    # Test Edition Name Manhua
    # -------------------------------------------------------------------------------------------------
    def test_edition_name_manhua(self):
        try:
            series_name = self.s_e.get_edition_name(
                IVolume({
                    'series': 'Rascal Does Not Dream Of Bunny Girl Senpai',
                    'volume': '1',
                    'format': 'Manhua',
                    'display_name': 'Rascal Does Not Dream Of Bunny Girl Senpai Manhua Volume 1'
                })
            )
            print('SUCCESS'
                  if series_name == 'Rascal Does Not Dream Of Bunny Girl Senpai'
                  else 'FAILED', '- Test Edition Name Manhua')
        except:
            print('FAILED - Test Edition Name Manhua')


    # -------------------------------------------------------------------------------------------------
    # Test Edition Name Format Not In Name
    # -------------------------------------------------------------------------------------------------
    def test_edition_name_format_not_in_name(self):
        try:
            series_name = self.s_e.get_edition_name(
                IVolume({
                    'series': 'Takane and Hana',
                    'volume': '18',
                    'format': 'Manga',
                    'display_name': 'Takane and Hana Limited Edition Volume 18'
                })
            )
            print('SUCCESS'
                  if series_name == 'Takane and Hana Limited Edition'
                  else 'FAILED', '- Test Edition Name Format Not In Name')
        except:
            print('FAILED - Test Edition Name Format Not In Name')


    # -------------------------------------------------------------------------------------------------
    # Test Edition Name No Format
    # -------------------------------------------------------------------------------------------------
    def test_edition_name_no_format(self):
        try:
            series_name = self.s_e.get_edition_name(
                IVolume({
                    'series': 'Takane and Hana',
                    'volume': '18',
                    'format': None,
                    'display_name': 'Takane and Hana Limited Edition Volume 18'
                })
            )
            print('SUCCESS'
                  if series_name == 'Takane and Hana Limited Edition'
                  else 'FAILED', '- Test Edition Name No Format')
        except:
            print('FAILED - Test Edition Name No Format')


    # -------------------------------------------------------------------------------------------------
    # Test Edition Name Special Characters
    # -------------------------------------------------------------------------------------------------
    def test_edition_name_special_characters(self):
        try:
            series_name = self.s_e.get_edition_name(
                IVolume({
                    'series': 'Re Zero: Takane & Hana + Gamer',
                    'volume': '18',
                    'format': 'Manga',
                    'display_name': 'Re Zero: Takane & Hana + Gamer Limited Edition Manga Volume 18'
                })
            )
            print('SUCCESS'
                  if series_name == 'Re Zero: Takane & Hana + Gamer Limited Edition'
                  else 'FAILED', '- Test Edition Name Special Characters')
        except:
            print('FAILED - Test Edition Name Special Characters')







test_series = TestSeries()
test_series.run_all()