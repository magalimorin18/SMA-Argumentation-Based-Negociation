#!/usr/bin/env python3

from ast import arg
from click import argument
from communication.preferences.Value import Value
from arguments.CoupleValue import CoupleValue
from arguments.Comparison import Comparison
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
        self.__item = item
        self.__comparison_list = []
        self.__couple_values_list = []
        self.__premisses = []

    def __str__(self) -> str:
        return f'{"" if self.__decision else "not"} {self.__item.get_name()} \u2190  {(", ").join([str(el) for el in self.__premisses])}'

    def add_premiss_comparison(self, criterion_name_1, criterion_name_2):
        """Adds a premiss comparison in the comparison list.
        """
        self.__comparison_list.append(
            Comparison(criterion_name_1, criterion_name_2))

    def add_premiss_couple_values(self, criterion_name, value):
        """Add a premiss couple values in the couple values list.
        """
        self.__couple_values_list.append(CoupleValue(criterion_name, value))
    
    def get_premiss_couple_values_list(self):
        """Returns the premiss couple values list.
        """
        return self.__couple_values_list
    
    def get_premiss_comparison_list(self):
        """Returns the premiss comparison list.
        """
        return self.__comparison_list
    
    def get_premisses(self):
        return self.__premisses
    
    def get_conclusion(self):
        return self.__decision, self.__item

    def list_supporting_proposal(self, preference):
        """ Generate a list of premisses which can be used to support an item
            : param item : Item - name of the item
            : return : list of all premisses PRO an item ( sorted by order of importance
                based on agent's preferences )
        """
        criterion_list = preference.get_criterion_name_list()
        # supporting_proposal = []
        for criterion_name in criterion_list:
            pref_value = preference.get_value(self.__item, criterion_name)
            if pref_value in [Value.GOOD, Value.VERY_GOOD]:
        #         supporting_proposal.append(CoupleValue(criterion_name, pref_value))
        # return supporting_proposal
                self.add_premiss_couple_values(
                    criterion_name, preference.get_value(self.__item, criterion_name))
                # for worse_criterion_name in criterion_list:
                #     if preference.is_preferred_criterion(criterion_name, worse_criterion_name):
                #         self.add_premiss_comparison(
                #             criterion_name, worse_criterion_name)

    def list_attacking_proposal(self, preference):
        """ Generate a list of premisses which can be used to attack an item
            : param item : Item - name of the item
            : return : list of all premisses CON an item ( sorted by order of importance
            based on preferences )
        """
        criterion_list = preference.get_criterion_name_list()
        # attacking_proposal = []
        for criterion_name in criterion_list:
            pref_value = preference.get_value(self.__item, criterion_name)
            if pref_value in [Value.BAD, Value.VERY_BAD]:
        #         attacking_proposal.append(CoupleValue(criterion_name, pref_value))
        # return attacking_proposal
                self.add_premiss_couple_values(
                    criterion_name, preference.get_value(self.__item, criterion_name))
                # for worse_criterion_name in criterion_list:
                #     if preference.is_preferred_criterion(criterion_name, worse_criterion_name):
                #         self.add_premiss_comparison(
                #             criterion_name, worse_criterion_name)

    def best_premiss(self):
        if len(self.__couple_values_list) > 0:
            self.__premisses.append(self.__couple_values_list[0])