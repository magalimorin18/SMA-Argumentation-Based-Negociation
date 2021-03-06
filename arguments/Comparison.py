#!/usr/bin/env python3


class Comparison:
    """Comparison class.
    This class implements a comparison object used in argument object.

    attr:
        best_criterion_name:
        worst_criterion_name:
    """

    def __init__(self, best_criterion_name, worst_criterion_name):
        """Creates a new comparison.
        """
        self.__best_criterion_name = best_criterion_name
        self.__worst_criterion_name = worst_criterion_name

    def __str__(self):
        return f'{self.__best_criterion_name.name} \u227b {self.__worst_criterion_name.name}'
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Comparison):
            return self.__best_criterion_name == __o.__best_criterion_name and self.__worst_criterion_name == __o.__worst_criterion_name
