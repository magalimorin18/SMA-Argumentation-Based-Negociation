#!/usr/bin/env python3

from communication.arguments.Comparison import Comparison
from communication.arguments.CoupleValue import CoupleValue
from communication.preferences.Value import Value


class Argument:
    """Argument class.
    This class implements an argument used in the negotiation.

    attr:
        decision:
        item:
        comparison_list:
        couple_values_list:
    """

    def __init__(self, boolean_decision, item):
        """Creates a new Argument.
        """
        self.__decision = boolean_decision
        self.__item = item.get_name()
        self.__comparison_list = []
        self.__couple_values_list = []

    def add_premiss_comparison(self, criterion_name_1, criterion_name_2):
        """Adds a premiss comparison in the comparison list.
        """
        self.__comparison_list.append(Comparison(criterion_name_1, criterion_name_2))

    def add_premiss_couple_values(self, criterion_name, value):
        """Add a premiss couple values in the couple values list.
        """
        self.__couple_values_list.append(CoupleValue(criterion_name, value))

    def list_supporting_proposal(self, item, preference):
        """Returns the list of supporting proposal.
        """
        criterion_list = preference.get_criterion_name_list()
        for i, criterion_name in enumerate(criterion_list):
            if preference.get_value(item, criterion_name) in [Value.GOOD, Value.VERY_GOOD]:
                self.add_premiss_couple_values(criterion_name, preference.get_value(item, criterion_name))
                for worse_criterion_name in criterion_list[i+1:]:
                    self.add_premiss_comparison(criterion_name, worse_criterion_name)

    
    def list_attacking_proposal(self, item, preference):
        """Returns the list of attacking proposal.
        """
        criterion_list = preference.get_criterion_name_list()
        for i, criterion_name in enumerate(criterion_list):
            if preference.get_value(item, criterion_name) in [Value.BAD, Value.VERY_BAD]:
                self.add_premiss_couple_values(criterion_name, preference.get_value(item, criterion_name))
                for worse_criterion_name in criterion_list[i+1:]:
                    self.add_premiss_comparison(criterion_name, worse_criterion_name)