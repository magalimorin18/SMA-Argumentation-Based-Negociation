#!/usr/bin/env python3
import operator
from communication.preferences.Value import Value
from communication.preferences.Item import Item
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.CriterionName import CriterionName
import os
import sys
sys.path.append(os.getcwd())

# When running the file test_unitaire uncomment


class Preferences:
    """Preferences class.
    This class implements the preferences of an agent.

    attr:
        criterion_name_list: the list of criterion name (ordered by importance)
        criterion_value_list: the list of criterion value
    """

    def __init__(self):
        """Creates a new Preferences object.
        """
        self.__criterion_name_list = []
        self.__criterion_value_list = []

    def get_criterion_name_list(self):
        """Returns the list of criterion name.
        """
        return self.__criterion_name_list

    def get_criterion_value_list(self):
        """Returns the list of criterion value.
        """
        return self.__criterion_value_list

    def set_criterion_name_list(self, criterion_name_list):
        """Sets the list of criterion name.
        """
        self.__criterion_name_list = criterion_name_list

    def add_criterion_value(self, criterion_value):
        """Adds a criterion value in the list.
        """
        self.__criterion_value_list.append(criterion_value)

    def get_value(self, item, criterion_name):
        """Gets the value for a given item and a given criterion name.
        """
        for value in self.__criterion_value_list:
            if value.get_item() == item and value.get_criterion_name() == criterion_name:
                return value.get_value()
        return None

    def is_preferred_criterion(self, criterion_name_1, criterion_name_2):
        """Returns if a criterion 1 is preferred to the criterion 2.
        """
        for criterion_name in self.__criterion_name_list:
            if criterion_name == criterion_name_1:
                return True
            if criterion_name == criterion_name_2:
                return False

    def is_preferred_item(self, item_1, item_2):
        """Returns if the item 1 is preferred to the item 2.
        """
        return item_1.get_score(self) > item_2.get_score(self)

    def most_preferred(self, item_list):
        """Returns the most preferred item from a list.
        """
        if len(item_list) != 0:
            score_items = {}
            for item in item_list:
                score_items[item] = item.get_score(self)
            best_item = max(score_items.items(), key=operator.itemgetter(1))[0]
            return best_item

    def is_item_among_top_10_percent(self, item, item_list):
        """
        Return whether a given item is among the top 10 percent of the preferred items.

        :return: a boolean, True means that the item is among the favourite ones
        """
        score_items = {}
        for each_item in item_list:
            score_items[each_item] = each_item.get_score(self)
        score_items_order = {k: v for k, v in sorted(
            score_items.items(), key=lambda item: item[1])}
        item_list_ordered = list(score_items_order.keys())
        number_value_to_get = len(item_list_ordered)//10
        if number_value_to_get == 0:
            best_item = self.most_preferred(item_list)
            is_top_item = (best_item == item)
        else:
            item_list_cropped = item_list_ordered[:number_value_to_get]
            is_top_item = (item in item_list_cropped)
        return(is_top_item)


if __name__ == '__main__':
    """Testing the Preferences class.
    """
    agent_pref = Preferences()
    agent_pref.set_criterion_name_list([CriterionName.PRODUCTION_COST, CriterionName.ENVIRONMENT_IMPACT,
                                        CriterionName.CONSUMPTION, CriterionName.DURABILITY,
                                        CriterionName.NOISE])

    diesel_engine = Item("Diesel Engine", "A super cool diesel engine")
    agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.PRODUCTION_COST,
                                                  Value.VERY_GOOD))
    agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.CONSUMPTION,
                                                  Value.GOOD))
    agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.DURABILITY,
                                                  Value.VERY_GOOD))
    agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.ENVIRONMENT_IMPACT,
                                                  Value.VERY_BAD))
    agent_pref.add_criterion_value(CriterionValue(diesel_engine, CriterionName.NOISE,
                                                  Value.VERY_BAD))

    electric_engine = Item("Electric Engine", "A very quiet engine")
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

    """test list of preferences"""
    print(diesel_engine)
    print(electric_engine)
    print(diesel_engine.get_value(agent_pref, CriterionName.PRODUCTION_COST))
    print(agent_pref.is_preferred_criterion(
        CriterionName.CONSUMPTION, CriterionName.NOISE))
    print('Electric Engine > Diesel Engine : {}'.format(
        agent_pref.is_preferred_item(electric_engine, diesel_engine)))
    print('Diesel Engine > Electric Engine : {}'.format(
        agent_pref.is_preferred_item(diesel_engine, electric_engine)))
    print('Electric Engine (for agent 1) = {}'.format(
        electric_engine.get_score(agent_pref)))
    print('Diesel Engine (for agent 1) = {}'.format(
        diesel_engine.get_score(agent_pref)))
    print('Most preferred item is : {}'.format(
        agent_pref.most_preferred([diesel_engine, electric_engine]).get_name()))

    print(agent_pref.is_preferred_item(diesel_engine, electric_engine))
    item_list_ = [diesel_engine, electric_engine]
    print(type(agent_pref.most_preferred(item_list_).get_name()))
