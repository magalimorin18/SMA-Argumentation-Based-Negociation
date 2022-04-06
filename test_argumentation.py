#!/usr/bin/env python3
"""
Testing all the functionalities of the communication package.
"""

from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.mailbox.Mailbox import Mailbox
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative
from communication.message.MessageService import MessageService

from communication.preferences.Preferences import Preferences
from communication.preferences.Preferences import Item
from communication.preferences.Preferences import Value
from communication.preferences.Preferences import CriterionValue
from communication.preferences.Preferences import CriterionName
from pw_argumentation import ArgumentAgent


class TestAgent(ArgumentAgent):
    """ TestAgent which inherit from CommunicatingAgent to test these functionalities.
    """

    def __init__(self, unique_id, model, name):
        super().__init__(unique_id, model, name)

    def step(self):
        super().step()


class TestModel(Model):
    """ TestModel which inherit from Model to test CommunicatingAgent and MessageService.
    """

    def __init__(self):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        for i in range(2):
            a = TestAgent(i, self, "Agent" + str(i))
            self.schedule.add(a)
        self.running = True

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()


def agent_preference():
    agent_pref = Preferences()
    item_list = []
    for i in range(0, 2):
        item_list.append(Item(f'car{i}', f'description of car{i}'))
    agent_pref.add_criterion_value(CriterionValue(item_list[0], CriterionName.PRODUCTION_COST,
                                                  Value.VERY_GOOD))
    agent_pref.add_criterion_value(CriterionValue(item_list[1], CriterionName.PRODUCTION_COST,
                                                  Value.VERY_BAD))
    return [agent_pref, item_list]


if __name__ == "__main__":

    mailbox = Mailbox()
    communicating_model = TestModel()

    assert(len(communicating_model.schedule.agents) == 2)
    print("*     get the number of CommunicatingAgent => OK")

    agent0 = communicating_model.schedule.agents[0]
    agent1 = communicating_model.schedule.agents[1]

    assert(agent0.get_name() == "Agent0")
    assert(agent1.get_name() == "Agent1")
    print("*     get_name() => OK")

    agent0_pref = agent_preference()[0]
    item_list = agent_preference()[1]
    # agent0_pref.most_preferred(item_list) === car0 (description of car0)
    item_list = agent_preference()[1]
    # item_list === [<communication.preferences.Item.Item object at 0x000001E9C4F20AC0>, ..]
    m1 = Message("Agent0", "Agent1", MessagePerformative.PROPOSE,
                 agent0_pref.most_preferred(item_list))
    m2 = Message("Agent1", "Agent0", MessagePerformative.ASK_WHY,
                 agent0_pref.most_preferred(item_list))
    m3 = Message("Agent0", "Agent1", MessagePerformative.ARGUE,
                 agent0.support_proposal(item_list[0]))

    agent0.send_message(m1)
    MessageService.get_instance().set_instant_delivery(False)
    communicating_model.step()
    agent1.receive_message(m1)
    agent1.send_message(m2)
    communicating_model.step()
    agent0.receive_message(m2)
    agent0.send_message(m3)
