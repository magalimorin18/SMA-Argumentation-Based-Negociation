
"""Unit tests """
from communication.preferences.Preferences import Preferences
from communication.preferences.Preferences import Item
from communication.preferences.Preferences import Value
from communication.preferences.Preferences import CriterionValue
from communication.preferences.Preferences import CriterionName

agent_pref = Preferences()

car1 = Item("car1", "car1")
agent_pref.add_criterion_value(CriterionValue(car1, CriterionName.PRODUCTION_COST,
                                              Value.VERY_GOOD))
agent_pref.add_criterion_value(CriterionValue(car1, CriterionName.CONSUMPTION,
                                              Value.VERY_GOOD))
agent_pref.add_criterion_value(CriterionValue(car1, CriterionName.DURABILITY,
                                              Value.VERY_GOOD))
agent_pref.add_criterion_value(CriterionValue(car1, CriterionName.ENVIRONMENT_IMPACT,
                                              Value.VERY_GOOD))
agent_pref.add_criterion_value(CriterionValue(car1, CriterionName.NOISE,
                                              Value.VERY_GOOD))

car2 = Item("car2", "car2")
agent_pref.add_criterion_value(CriterionValue(car2, CriterionName.PRODUCTION_COST,
                                              Value.GOOD))
agent_pref.add_criterion_value(CriterionValue(car2, CriterionName.CONSUMPTION,
                                              Value.GOOD))
agent_pref.add_criterion_value(CriterionValue(car2, CriterionName.DURABILITY,
                                              Value.GOOD))
agent_pref.add_criterion_value(CriterionValue(car2, CriterionName.ENVIRONMENT_IMPACT,
                                              Value.GOOD))
agent_pref.add_criterion_value(CriterionValue(car2, CriterionName.NOISE,
                                              Value.GOOD))

car3 = Item("car3", "car3")
agent_pref.add_criterion_value(CriterionValue(car3, CriterionName.PRODUCTION_COST,
                                              Value.AVERAGE))
agent_pref.add_criterion_value(CriterionValue(car3, CriterionName.CONSUMPTION,
                                              Value.AVERAGE))
agent_pref.add_criterion_value(CriterionValue(car3, CriterionName.DURABILITY,
                                              Value.AVERAGE))
agent_pref.add_criterion_value(CriterionValue(car3, CriterionName.ENVIRONMENT_IMPACT,
                                              Value.AVERAGE))
agent_pref.add_criterion_value(CriterionValue(car3, CriterionName.NOISE,
                                              Value.AVERAGE))

car4 = Item("car4", "car4")
agent_pref.add_criterion_value(CriterionValue(car4, CriterionName.PRODUCTION_COST,
                                              Value.BAD))
agent_pref.add_criterion_value(CriterionValue(car4, CriterionName.CONSUMPTION,
                                              Value.BAD))
agent_pref.add_criterion_value(CriterionValue(car4, CriterionName.DURABILITY,
                                              Value.BAD))
agent_pref.add_criterion_value(CriterionValue(car4, CriterionName.ENVIRONMENT_IMPACT,
                                              Value.BAD))
agent_pref.add_criterion_value(CriterionValue(car4, CriterionName.NOISE,
                                              Value.BAD))

car5 = Item("car5", "car5")
agent_pref.add_criterion_value(CriterionValue(car5, CriterionName.PRODUCTION_COST,
                                              Value.BAD))
agent_pref.add_criterion_value(CriterionValue(car5, CriterionName.CONSUMPTION,
                                              Value.AVERAGE))
agent_pref.add_criterion_value(CriterionValue(car5, CriterionName.DURABILITY,
                                              Value.AVERAGE))
agent_pref.add_criterion_value(CriterionValue(car5, CriterionName.ENVIRONMENT_IMPACT,
                                              Value.AVERAGE))
agent_pref.add_criterion_value(CriterionValue(car5, CriterionName.NOISE,
                                              Value.AVERAGE))

car6 = Item("car6", "car6")
agent_pref.add_criterion_value(CriterionValue(car6, CriterionName.PRODUCTION_COST,
                                              Value.VERY_BAD))
agent_pref.add_criterion_value(CriterionValue(car6, CriterionName.CONSUMPTION,
                                              Value.VERY_BAD))
agent_pref.add_criterion_value(CriterionValue(car6, CriterionName.DURABILITY,
                                              Value.AVERAGE))
agent_pref.add_criterion_value(CriterionValue(car6, CriterionName.ENVIRONMENT_IMPACT,
                                              Value.AVERAGE))
agent_pref.add_criterion_value(CriterionValue(car6, CriterionName.NOISE,
                                              Value.AVERAGE))

car7 = Item("car7", "car7")
agent_pref.add_criterion_value(CriterionValue(car7, CriterionName.PRODUCTION_COST,
                                              Value.VERY_BAD))
agent_pref.add_criterion_value(CriterionValue(car7, CriterionName.CONSUMPTION,
                                              Value.VERY_BAD))
agent_pref.add_criterion_value(CriterionValue(car7, CriterionName.DURABILITY,
                                              Value.VERY_BAD))
agent_pref.add_criterion_value(CriterionValue(car7, CriterionName.ENVIRONMENT_IMPACT,
                                              Value.AVERAGE))
agent_pref.add_criterion_value(CriterionValue(car7, CriterionName.NOISE,
                                              Value.AVERAGE))
car8 = Item("car8", "car8")
agent_pref.add_criterion_value(CriterionValue(car8, CriterionName.PRODUCTION_COST,
                                              Value.VERY_BAD))
agent_pref.add_criterion_value(CriterionValue(car8, CriterionName.CONSUMPTION,
                                              Value.VERY_BAD))
agent_pref.add_criterion_value(CriterionValue(car8, CriterionName.DURABILITY,
                                              Value.VERY_BAD))
agent_pref.add_criterion_value(CriterionValue(car8, CriterionName.ENVIRONMENT_IMPACT,
                                              Value.VERY_BAD))
agent_pref.add_criterion_value(CriterionValue(car8, CriterionName.NOISE,
                                              Value.AVERAGE))
car9 = Item("car9", "car9")
agent_pref.add_criterion_value(CriterionValue(car9, CriterionName.PRODUCTION_COST,
                                              Value.VERY_BAD))
agent_pref.add_criterion_value(CriterionValue(car9, CriterionName.CONSUMPTION,
                                              Value.AVERAGE))
agent_pref.add_criterion_value(CriterionValue(car9, CriterionName.DURABILITY,
                                              Value.AVERAGE))
agent_pref.add_criterion_value(CriterionValue(car9, CriterionName.ENVIRONMENT_IMPACT,
                                              Value.AVERAGE))
agent_pref.add_criterion_value(CriterionValue(car9, CriterionName.NOISE,
                                              Value.AVERAGE))
car10 = Item("car10", "car10")
agent_pref.add_criterion_value(CriterionValue(car10, CriterionName.PRODUCTION_COST,
                                              Value.VERY_BAD))
agent_pref.add_criterion_value(CriterionValue(car10, CriterionName.CONSUMPTION,
                                              Value.VERY_BAD))
agent_pref.add_criterion_value(CriterionValue(car10, CriterionName.DURABILITY,
                                              Value.VERY_BAD))
agent_pref.add_criterion_value(CriterionValue(car10, CriterionName.ENVIRONMENT_IMPACT,
                                              Value.VERY_BAD))
agent_pref.add_criterion_value(CriterionValue(car10, CriterionName.NOISE,
                                              Value.VERY_BAD))
item_list = [car1, car2, car3, car4, car5, car6, car7, car8, car9, car10]


def test_most_preferred():
    assert agent_pref.most_preferred(item_list) == car1


def test_is_item_among_top_10_percent():
    assert agent_pref.is_item_among_top_10_percent(car1, item_list) == True
