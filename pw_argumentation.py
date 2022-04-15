from mesa import Model
from mesa.time import RandomActivation
import time

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.preferences.Preferences import Preferences
from communication.preferences.Item import Item
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.CriterionName import CriterionName
from communication.preferences.Value import Value
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative
from arguments.Argument import Argument
from arguments.Comparison import Comparison
from arguments.CoupleValue import CoupleValue


class ArgumentAgent(CommunicatingAgent):
    """ArgumentAgent which inherits from CommunicatingAgent"""

    def __init__(self, unique_id, model, name):
        super().__init__(unique_id=unique_id, model=model, name=name)
        self.preference = Preferences()
        self.__committed = False

    def step(self):
        # TODO: Add unit tests
        super().step()
        # print(f"{self.get_name()}'s turn")
        list_messages = self.get_new_messages()
        for message in list_messages:
            print(message)
            # print(f"Agent {self.get_name()} has right performative: {message.get_performative() in [MessagePerformative.ACCEPT, MessagePerformative.COMMIT]}")
            # print(f"Agent {self.get_name()} has item in set: {message.get_content() in self._item_set}")
            # print(f"Agent {self.get_name()} has item set: {self._item_set}")
            if (message.get_performative() == MessagePerformative.PROPOSE):
                if self.preference.is_item_among_top_10_percent(message.get_content(), self.model._item_set):
                    self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(
                    ), message_performative=MessagePerformative.ACCEPT, content=message.get_content()))
                else:
                    self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(
                    ), message_performative=MessagePerformative.ASK_WHY, content=message.get_content()))

            if (message.get_performative() == MessagePerformative.ACCEPT):
                # print(f"Got through that condition for {self.get_name()}")
                self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(
                ), message_performative=MessagePerformative.COMMIT, content=message.get_content()))
                self.__committed = True

            if (message.get_performative() == MessagePerformative.COMMIT) and (not self.has_committed()):
                self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(
                ), message_performative=MessagePerformative.COMMIT, content=message.get_content()))
                self.__committed = True

            if (message.get_performative() == MessagePerformative.ASK_WHY):
                new_argument = Argument(True, message.get_content())
                self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(
                ), message_performative=MessagePerformative.ARGUE, content=self.support_proposal(new_argument)))

            if message.get_performative() == MessagePerformative.ARGUE:
                received_argument = message.get_content()

                # If attacker
                if received_argument.get_conclusion()[0]:
                    attack_argument = self.attack_proposal(received_argument)
                    if attack_argument:
                        self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ARGUE, content=attack_argument))
                    else:
                        self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ACCEPT, content=received_argument.get_conclusion()[1]))
                # If supporter
                else:
                    support_argument = self.support_proposal(received_argument)
                    if support_argument:
                        self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ARGUE, content=support_argument))
                    else:
                        other_item = self.select_other_item(self.argument_parsing(received_argument)[1][1])
                        if other_item:
                            self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.PROPOSE, content=other_item))
                        else:
                            print("WARNING: No other item to propose")
                    
    def select_other_item(self, item):
        """selects an item from the item set which is not the item received

        Args:
            item (Item): the item received

        Returns:
            Item: the item selected
        """
        other_item_set = [i for i in self.model._item_set if i != item]
        if len(other_item_set)>0:
            other_item = self.model.random.choice(other_item_set)
            return other_item
        else:
            return False

    def get_preference(self):
        return self.preference

    def has_committed(self):
        return self.__committed

    def generate_preferences(self, random_prefs=False):
        # see question 3
        # To be completed
        # TODO: Add a csv filename argument to generate preferences (need to discuss about the formatting)

        if random_prefs:
            # Random criterion priorities
            criterion_list = list(CriterionName)
            self.random.shuffle(criterion_list)
            self.preference.set_criterion_name_list(criterion_list)

            # Random generation of preferences for all criteria
            for item in self.model._item_set:
                for criterion in self.preference.get_criterion_name_list():
                    item_criterion_pref = CriterionValue(item, criterion, self.random.choice(list(Value)))
                    self.preference.add_criterion_value(item_criterion_pref)
        else:
            if self.get_name() == "A_1":
                self.preference.set_criterion_name_list([CriterionName.PRODUCTION_COST, CriterionName.ENVIRONMENT_IMPACT, CriterionName.CONSUMPTION, CriterionName.DURABILITY, CriterionName.NOISE])
                for item in self.model._item_set:
                    if item.get_name() == "ICED":
                        self.preference.add_criterion_value(CriterionValue(item, CriterionName.PRODUCTION_COST, Value.VERY_GOOD))
                        self.preference.add_criterion_value(CriterionValue(item, CriterionName.CONSUMPTION, Value.GOOD))
                        self.preference.add_criterion_value(CriterionValue(item, CriterionName.DURABILITY, Value.VERY_GOOD))
                        self.preference.add_criterion_value(CriterionValue(item, CriterionName.ENVIRONMENT_IMPACT, Value.VERY_BAD))
                        self.preference.add_criterion_value(CriterionValue(item, CriterionName.NOISE, Value.BAD))
                    elif item.get_name() == "E":
                        self.preference.add_criterion_value(CriterionValue(item, CriterionName.PRODUCTION_COST, Value.BAD))
                        self.preference.add_criterion_value(CriterionValue(item, CriterionName.CONSUMPTION, Value.VERY_BAD))
                        self.preference.add_criterion_value(CriterionValue(item, CriterionName.DURABILITY, Value.GOOD))
                        self.preference.add_criterion_value(CriterionValue(item, CriterionName.ENVIRONMENT_IMPACT, Value.VERY_GOOD))
                        self.preference.add_criterion_value(CriterionValue(item, CriterionName.NOISE, Value.VERY_GOOD))
            elif self.get_name() == "A_2":
                self.preference.set_criterion_name_list([CriterionName.ENVIRONMENT_IMPACT, CriterionName.NOISE, CriterionName.PRODUCTION_COST, CriterionName.CONSUMPTION, CriterionName.DURABILITY])
                for item in self.model._item_set:
                    if item.get_name() == "ICED":
                        self.preference.add_criterion_value(CriterionValue(item, CriterionName.PRODUCTION_COST, Value.GOOD))
                        self.preference.add_criterion_value(CriterionValue(item, CriterionName.CONSUMPTION, Value.BAD))
                        self.preference.add_criterion_value(CriterionValue(item, CriterionName.DURABILITY, Value.VERY_GOOD))
                        self.preference.add_criterion_value(CriterionValue(item, CriterionName.ENVIRONMENT_IMPACT, Value.VERY_BAD))
                        self.preference.add_criterion_value(CriterionValue(item, CriterionName.NOISE, Value.VERY_BAD))
                    elif item.get_name() == "E":
                        self.preference.add_criterion_value(CriterionValue(item, CriterionName.PRODUCTION_COST, Value.GOOD))
                        self.preference.add_criterion_value(CriterionValue(item, CriterionName.CONSUMPTION, Value.BAD))
                        self.preference.add_criterion_value(CriterionValue(item, CriterionName.DURABILITY, Value.BAD))
                        self.preference.add_criterion_value(CriterionValue(item, CriterionName.ENVIRONMENT_IMPACT, Value.VERY_GOOD))
                        self.preference.add_criterion_value(CriterionValue(item, CriterionName.NOISE, Value.VERY_GOOD))
            else:
                self.generate_preferences(self, random_prefs=True)

    def support_proposal(self, received_argument = None):
        """
        Used when the agent receives " ASK_WHY " after having proposed an item
        : param item_name : str - name of the item which was proposed
        : return : string - the strongest supportive argument
        """
        # item = self.model.find_item_from_name(item_name)
        premisses, (decision, proposed_item) = self.argument_parsing(received_argument)

        # In case of ask_why, the agent creates the argument
        if decision:
            received_argument.list_supporting_proposal(self.preference)
            received_argument.add_premiss()
            return received_argument
        
        # Otherwise, negociating with the other agent
        else:
            criterion_preference_order = self.preference.get_criterion_name_list()
            supporting_argument = Argument(True, proposed_item)
            if isinstance(premisses[0], CoupleValue):
                premiss = premisses[0]
                # Prefered criterion has high value
                for criterion in criterion_preference_order:
                    if self.preference.is_preferred_criterion(criterion, premiss.get_criterion_name()) and self.preference.get_value(proposed_item, premiss.get_criterion_name()) in [Value.GOOD, Value.VERY_GOOD]:
                        better_crit = Comparison(criterion, premiss.get_criterion_name())
                        good_value = CoupleValue(criterion, self.preference.get_value(proposed_item, premiss.get_criterion_name()))
                        supporting_argument.add_premiss(better_crit)
                        supporting_argument.add_premiss(good_value)
                        return supporting_argument
                return False
    
    def argument_parsing(self, argument):
        """returns the premisses and the decision from recieved message

        Args:
            argument (Argument): the received argument

        Returns:
            premisses: list of premisses
            conclusion: the decision (boolean, item)
        """
        return argument.get_premisses(), argument.get_conclusion()         

    def attack_proposal(self, received_argument):
        premisses, (received_decision, proposed_item) = self.argument_parsing(received_argument)
        assert received_decision == True
        criterion_preference_order = self.preference.get_criterion_name_list()
        attacking_argument = Argument(False, proposed_item)
        attacking_argument.list_attacking_proposal(self.preference)
        if isinstance(premisses[0], CoupleValue):
            premiss = premisses[0]
            # Prefered criterion
            for criterion in criterion_preference_order:
                if self.preference.is_preferred_criterion(criterion, premiss.get_criterion_name()):
                    comp = Comparison(criterion, premiss.get_criterion_name())
                    attacking_argument.add_premiss(comp)
                    return attacking_argument
            
            # Lower value for the same criterion
            if self.preference.get_value(proposed_item, premiss.get_criterion_name()).value < premiss.get_value().value:
                premiss = CoupleValue(premiss.get_criterion_name(), self.preference.get_value(proposed_item, premiss.get_criterion_name()))
                attacking_argument.add_premiss(premiss)
                return attacking_argument
            
            # Prefered criterion has low value
            for criterion in criterion_preference_order:
                if self.preference.is_preferred_criterion(criterion, premiss.get_criterion_name()) and self.preference.get_value(proposed_item, premiss.get_criterion_name()) in [Value.BAD, Value.VERY_BAD]:
                    better_crit = Comparison(criterion, premiss.get_criterion_name())
                    bad_value = CoupleValue(criterion, self.preference.get_value(proposed_item, premiss.get_criterion_name()))
                    attacking_argument.add_premiss(better_crit)
                    attacking_argument.add_premiss(bad_value)
                    return attacking_argument
            
            # Other item with better value on the same criterion
            for item in self.model._item_set:
                if self.preference.get_value(item, premiss.get_criterion_name()).value > premiss.get_value().value:
                    other_prop = Argument(True, item)
                    other_prop.list_supporting_proposal(self.preference)
                    better_value = CoupleValue(premiss.get_criterion_name(), self.preference.get_value(item, premiss.get_criterion_name()))
                    other_prop.add_premiss(better_value)
                    return other_prop

        return False

class ArgumentModel(Model):
    """ArgumentModel which inherits from Model"""

    def __init__(self, item_set, list_agent_names):
        super().__init__(self)
        self.schedule = RandomActivation(self)
        self.__message_service = MessageService(self.schedule)
        self._item_set = item_set.copy()
        self.__list_agent_names = list_agent_names.copy()
        self._name_to_id = {}
        
        
        # To be completed

        for agent_name in self.__list_agent_names:
            new_id = self.next_id()
            a = ArgumentAgent(new_id, self, agent_name)
            a.generate_preferences()
            self.schedule.add(a)
            self._name_to_id[agent_name] = new_id

        self.running = True

    # Attempt at handling negociation using model step
    # def argue(self):
    #     a_1_agent = self.schedule._agents[self._name_to_id["A_1"]]
    #     a_1_agent.send_message(
    #         Message(from_agent=a_1_agent.get_name(),
    #                 to_agent="A_2",
    #                 message_performative=MessagePerformative.PROPOSE,
    #                 content=self.random.choice(self.items_list)))

    def check_close_argumentation(self):
        """If all agents have committed, the model ends"""
        for agent in self.schedule.agents:
            if not agent.has_committed():
                return
        self.running = False
    
    def find_item_from_name(self, item_name):
        for item in self._item_set:
            if item.get_name() == item_name:
                return item

    def step(self):
        # self.argue()
        self.__message_service.dispatch_messages()
        self.check_close_argumentation()
        self.schedule.step()
        time.sleep(1)
        


if __name__ == "__main__":
    # To be completed
    items_list = [Item("ICED", "Diesel"), Item("E", "Electric")]
    agents_name = ["A_1", "A_2"]
    model = ArgumentModel(item_set=items_list, list_agent_names=agents_name)

    a_1_agent = model.schedule._agents[model._name_to_id["A_1"]]
    a_1_agent.send_message(
        Message(from_agent=a_1_agent.get_name(),
                to_agent="A_2",
                message_performative=MessagePerformative.PROPOSE,
                content=model.random.choice(model._item_set)))

    model.run_model()
