
"""Unit tests """
from communication.preferences.Preferences import Preferences
from communication.preferences.Preferences import Item
from communication.preferences.Preferences import Value
from communication.preferences.Preferences import CriterionValue
from communication.preferences.Preferences import CriterionName


def test_most_preferred():
    agent_pref = Preferences()
    item_list = []
    for i in range(0, 2):
        item_list.append(Item(f'car{i}', f'description of car{i}'))
    agent_pref.add_criterion_value(CriterionValue(item_list[0], CriterionName.PRODUCTION_COST,
                                                  Value.VERY_GOOD))
    agent_pref.add_criterion_value(CriterionValue(item_list[1], CriterionName.PRODUCTION_COST,
                                                  Value.VERY_BAD))

    assert agent_pref.most_preferred(item_list) == item_list[0]


def test_most_preferred_two_equal_items():
    agent_pref = Preferences()
    item_list = []
    for i in range(0, 2):
        item_list.append(Item(f'car{i}', f'description of car{i}'))
    agent_pref.add_criterion_value(CriterionValue(item_list[0], CriterionName.PRODUCTION_COST,
                                                  Value.VERY_GOOD))
    agent_pref.add_criterion_value(CriterionValue(item_list[1], CriterionName.PRODUCTION_COST,
                                                  Value.VERY_GOOD))

    assert agent_pref.most_preferred(item_list) == item_list[0]


def test_most_preferred_0_items():
    agent_pref = Preferences()
    item_list = []
    assert agent_pref.most_preferred(item_list) == None


def test_is_item_among_top_10_percent_2_items():
    agent_pref = Preferences()
    item_list = []
    for i in range(0, 2):
        item_list.append(Item(f'car{i}', f'description of car{i}'))
    agent_pref.add_criterion_value(CriterionValue(item_list[0], CriterionName.PRODUCTION_COST,
                                                  Value.VERY_GOOD))
    agent_pref.add_criterion_value(CriterionValue(item_list[1], CriterionName.PRODUCTION_COST,
                                                  Value.VERY_BAD))

    assert agent_pref.is_item_among_top_10_percent(
        item_list[0], item_list) == True
    assert agent_pref.is_item_among_top_10_percent(
        item_list[1], item_list) == False


def test_is_item_among_top_10_percent_15_items():
    agent_pref = Preferences()
    item_list = []
    for i in range(0, 15):
        item_list.append(Item(f'car{i}', f'description of car{i}'))

    for i in range(1, 15):
        agent_pref.add_criterion_value(CriterionValue(item_list[i], CriterionName.PRODUCTION_COST,
                                                      Value.VERY_BAD))
    agent_pref.add_criterion_value(CriterionValue(item_list[0], CriterionName.PRODUCTION_COST,
                                                  Value.VERY_GOOD))
    assert agent_pref.is_item_among_top_10_percent(
        item_list[0], item_list) == True
    for i in range(1, 15):
        assert agent_pref.is_item_among_top_10_percent(
            item_list[i], item_list) == False


def test_is_item_among_top_20_percent_20_items():
    agent_pref = Preferences()
    item_list = []
    for i in range(0, 20):
        item_list.append(Item(f'car{i}', f'description of car{i}'))
    for i in range(0, 2):
        agent_pref.add_criterion_value(CriterionValue(item_list[i], CriterionName.PRODUCTION_COST,
                                                      Value.VERY_GOOD))
    for i in range(2, 20):
        agent_pref.add_criterion_value(CriterionValue(item_list[i], CriterionName.PRODUCTION_COST,
                                                      Value.VERY_BAD))
    for i in range(0, 2):
        assert agent_pref.is_item_among_top_10_percent(
            item_list[i], item_list) == True
    for i in range(3, 15):
        assert agent_pref.is_item_among_top_10_percent(
            item_list[i], item_list) == False
