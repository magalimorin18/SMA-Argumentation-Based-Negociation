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
        criterion_list = reversed(preference.get_criterion_name_list())
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
        criterion_list = reversed(preference.get_criterion_name_list())
        # attacking_proposal = []
        for criterion_name in criterion_list:
            pref_value = preference.get_value(self.__item, criterion_name)
            if pref_value in [Value.BAD, Value.VERY_BAD]:
                #         attacking_proposal.append(CoupleValue(criterion_name, pref_value))
                # return attacking_proposal
                self.add_premiss_couple_values(
                    criterion_name, preference.get_value(self.__item, criterion_name))
                for better_criterion in criterion_list:
                    if preference.is_preferred_criterion(better_criterion, criterion_name):
                        self.add_premiss_comparison(
                            better_criterion, criterion_name)

    def find_supporting_premisses(self, preference, proposed_item, received_premisses=None):
        self.list_supporting_proposal(preference)
        # In negociations with the other agent
        if received_premisses:
            criterion_preference_order = preference.get_criterion_name_list()
            if isinstance(received_premisses[0], CoupleValue):
                premiss = received_premisses[0]
                # Prefered criterion has high value
                for criterion in criterion_preference_order:
                    if preference.is_preferred_criterion(criterion, premiss.get_criterion_name()) and preference.get_value(proposed_item, premiss.get_criterion_name()) in [Value.GOOD, Value.VERY_GOOD]:
                        better_crit = Comparison(
                            criterion, premiss.get_criterion_name())
                        good_value = CoupleValue(criterion, self.preference.get_value(
                            proposed_item, premiss.get_criterion_name()))
                        self.__add_premiss(good_value)
                        self.__add_premiss(better_crit)
                        return True
                return False

        # In case of ask_why, the agent creates the argument
        else:
            best_coup_val = self.get_premiss_couple_values_list()[0]
            self.__add_premiss(best_coup_val)
            return True

    def find_attacking_premisses(self, preference, proposed_item, received_premisses, item_set):

        self.list_attacking_proposal(preference)
        if isinstance(received_premisses[0], CoupleValue):
            premiss = received_premisses[0]
            criterion_preference_order = preference.get_criterion_name_list()

            # Prefered criterion has low value
            for criterion in criterion_preference_order:
                if preference.is_preferred_criterion(criterion, premiss.get_criterion_name()) and preference.get_value(proposed_item, criterion) in [Value.BAD, Value.VERY_BAD]:

                    better_crit = Comparison(
                        criterion, premiss.get_criterion_name())
                    bad_value = CoupleValue(
                        criterion, preference.get_value(proposed_item, criterion))
                    if (better_crit in self.get_premiss_comparison_list()) and (bad_value in self.get_premiss_couple_values_list()):
                        self.__add_premiss(better_crit)
                        self.__add_premiss(bad_value)
                        return True

            # Other item with better value on the same criterion
            for item in item_set:
                if preference.get_value(item, premiss.get_criterion_name()).value > premiss.get_value().value:
                    other_prop = Argument(True, item)
                    other_prop.list_supporting_proposal(preference)
                    better_value = CoupleValue(premiss.get_criterion_name(), preference.get_value(item, premiss.get_criterion_name()))
                    other_prop.__add_premiss(better_value)
                    return other_prop

            # # Prefered criterion
            # for criterion in criterion_preference_order:
            #     if preference.is_preferred_criterion(criterion, premiss.get_criterion_name()):
            #         comp = Comparison(criterion, premiss.get_criterion_name())
            #         self.__add_premiss(comp)
            #         return True

            # Lower value for the same criterion
            # if preference.get_value(proposed_item, premiss.get_criterion_name()).value < premiss.get_value().value:
            #     coupval = CoupleValue(premiss.get_criterion_name(), preference.get_value(proposed_item, premiss.get_criterion_name()))
            #     self.__add_premiss(coupval)
            #     return True

        return False

    def __add_premiss(self, premiss=None):
        if isinstance(premiss, CoupleValue) and premiss in self.__couple_values_list:
            self.__premisses.append(premiss)
        elif isinstance(premiss, Comparison) and premiss in self.__comparison_list:
            self.__premisses.append(premiss)
        # elif premiss==None:
        #     self.__premisses.append(self.__couple_values_list[0])

        # if len(self.__couple_values_list) > 0:
        #     self.add_premiss(self.__couple_values_list[0])
        # elif len(self.__comparison_list) > 0:
        #     self.add_premiss(self.__comparison_list[0])
        # else:
        #     self.add_premiss(self.__couple_values_list[0])
        # if len(self.__couple_values_list) > 0:
        #     self.add_premiss(self.__couple_values_list[0])
        # elif len(self.__comparison_list) > 0:
        #     self.add_premiss(self.__comparison_list[0])
        # else:
        #     self.add_premiss(self.__couple_values_list[0])
        # if len(self.__couple_values_list) > 0:
        #     self.add_premiss(self.__couple_values_list[0])
        # elif len(self.__comparison_list) > 0:
        #     self.add_premiss(self.__comparison_list[0])
        # else:
        #     self.add_premiss(self.__couple_values_list[0])
        # if len(self.__couple_values_list) > 0:
        #     self.add_premiss(self.__couple_values_list[0])
        # elif

        # if is_couple_value_type and len(self.__couple_values_list) > 0:
        #     self.__premisses.append(self.__couple_values_list[premiss_idx])
        # elif not is_couple_value_type and len(self.__comparison_list) > 0:
        #     self.__premisses.append(self.__comparison_list[premiss_idx])
