'''CommonHelper class to get timezone now'''
from datetime import datetime
from pytz import timezone

class CommonHelper:
    '''
    A class used to get the current time in a specific timezone.
    
    ...
    
    Methods
    -------
    get_timezone_now(format=str)
        Gets the current time in a specific timezone.
    '''

    def get_timezone_now(self, date_format='%Y-%m-%d %H:%M:%S'):
        '''
        Gets the current time in a specific timezone.
        
        Parameters:
        - format (str): The format to return the time in.
        
        Returns:
        - str: The current time in the specified timezone.
        '''
        return datetime.now(timezone('US/Eastern')).strftime(date_format)
