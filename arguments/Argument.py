#!/usr/bin/env python3

from ast import arg
from click import argument
from communication.preferences.Item import Item
from communication.preferences.Preferences import Preferences
from communication.preferences.CriterionName import CriterionName
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.Value import Value


from communication.arguments.CoupleValue import CoupleValue
from communication.arguments.Comparison import Comparison
from pip import main
import sys
sys.append('..')


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

    def __str__(self) -> str:
        return(f'{" " if self.__decision else "\u00ac"} {self.__item} "\u2190"' +
               f'{self.__comparison_list.join(" ")} {self.__couple_values_list.join(" ")}')

    def add_premiss_comparison(self, criterion_name_1, criterion_name_2):
        """Adds a premiss comparison in the comparison list.
        """
        self.__comparison_list.append(
            Comparison(criterion_name_1, criterion_name_2))

    def add_premiss_couple_values(self, criterion_name, value):
        """Add a premiss couple values in the couple values list.
        """
        self.__couple_values_list.append(CoupleValue(criterion_name, value))

    def support_proposal(self, item):
        """Checks if the argument supports the proposal.
        Used when the agent receives " ASK_WHY " after having proposed an item
        : param item : str - name of the item which was proposed
        : return : string - the strongest supportive argument
        """


if __name__ == "__main__":
    electric_engine = Item("Electric Engine", "A very quiet engine")
    agent_pref = Preferences()
    agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.PRODUCTION_COST,
                                                  Value.BAD))
    agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.CONSUMPTION,
                                                  Value.VERY_BAD))
    agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.DURABILITY,
                                                  Value.GOOD))
    agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.ENVIRONMENT_IMPACT,
                                                  Value.VERY_GOOD))
    agent_pref.add_criterion_value(CriterionValue(electric_engine, CriterionName.NOISE,
                                                  Value.VERY_GOOD))

    argument = Argument(True, electric_engine)
    argument.add_premiss_comparison()
