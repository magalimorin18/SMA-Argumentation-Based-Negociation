#!/usr/bin/env python3


class CoupleValue:
    """CoupleValue class.
    This class implements a couple value used in argument object.

    attr:
        criterion_name:
        value:
    """

    def __init__(self, criterion_name, value):
        """Creates a new couple value.
        """
        self.__criterion_name = criterion_name
        self.__value = value
    
    def get_criterion_name(self):
        """Returns the criterion name.
        """
        return self.__criterion_name
    
    def get_value(self):
        """Returns the value.
        """
        return self.__value

    def __str__(self):
        return f'{self.__criterion_name.name} = {self.__value.name}'

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, CoupleValue):
            return self.__criterion_name == __o.__criterion_name and self.__value == __o.__value