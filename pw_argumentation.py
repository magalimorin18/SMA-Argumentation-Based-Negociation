from mesa import Model
from mesa.time import RandomActivation
import re

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

    def __init__(self, unique_id, model, name, _item_set):
        super().__init__(unique_id=unique_id, model=model, name=name)
        self.preference = Preferences()
        self.__committed = False
        self.__usedArguments = [{key.get_name(): [] for key in _item_set}, {
            key.get_name(): [] for key in _item_set}]

    def step(self):
        # TODO: Add unit tests
        super().step()
        # print(f"{self.get_name()}'s turn")
        list_messages = self.get_new_messages()
        for message in list_messages:
            print(message)
            if (message.get_performative() == MessagePerformative.PROPOSE):
                if self.preference.is_item_among_top_10_percent(message.get_content(), self.model._item_set):
                    self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(
                    ), message_performative=MessagePerformative.ACCEPT, content=message.get_content()))
                else:
                    self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(
                    ), message_performative=MessagePerformative.ASK_WHY, content=message.get_content()))

            if (message.get_performative() == MessagePerformative.ACCEPT):
                self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(
                ), message_performative=MessagePerformative.COMMIT, content=message.get_content()))
                self.__committed = True

            if (message.get_performative() == MessagePerformative.COMMIT) and (not self.has_committed()):
                self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(
                ), message_performative=MessagePerformative.COMMIT, content=message.get_content()))
                self.__committed = True

            if (message.get_performative() == MessagePerformative.ASK_WHY):
                self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(
                ), message_performative=MessagePerformative.ARGUE, content=self.support_proposal(message.get_content())))

            if message.get_performative() == MessagePerformative.ARGUE:
                argument = message.get_content()
                item_name = re.search('(.+?)←', str(argument)).group(1)
                item_class = self.model.find_item_from_name(item_name)
                (decision, _) = argument.get_conclusion()  # item
                if not decision:
                    response = self.support_proposal(item_class)
                else:
                    response = self.attack_proposal(argument)

                # DONE: Faire en sorte que ça renvoit un attacking ou un supporting en fonction de la décision
                if response:
                    self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(
                    ), message_performative=MessagePerformative.ARGUE, content=response))
                else:
                    self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(
                    ), message_performative=MessagePerformative.ACCEPT, content=argument.get_conclusion()[1]))

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
                    item_criterion_pref = CriterionValue(
                        item, criterion, self.random.choice(list(Value)))
                    self.preference.add_criterion_value(item_criterion_pref)
        else:
            if self.get_name() == "A_1":
                self.preference.set_criterion_name_list(
                    [CriterionName.PRODUCTION_COST, CriterionName.ENVIRONMENT_IMPACT, CriterionName.CONSUMPTION, CriterionName.DURABILITY, CriterionName.NOISE])
                for item in self.model._item_set:
                    if item.get_name() == "ICED":
                        self.preference.add_criterion_value(CriterionValue(
                            item, CriterionName.PRODUCTION_COST, Value.GOOD))
                        self.preference.add_criterion_value(CriterionValue(
                            item, CriterionName.CONSUMPTION, Value.BAD))
                        self.preference.add_criterion_value(CriterionValue(
                            item, CriterionName.DURABILITY, Value.BAD))
                        self.preference.add_criterion_value(CriterionValue(
                            item, CriterionName.ENVIRONMENT_IMPACT, Value.BAD))
                        self.preference.add_criterion_value(
                            CriterionValue(item, CriterionName.NOISE, Value.BAD))
                    elif item.get_name() == "E":
                        self.preference.add_criterion_value(CriterionValue(
                            item, CriterionName.PRODUCTION_COST, Value.GOOD))
                        self.preference.add_criterion_value(CriterionValue(
                            item, CriterionName.CONSUMPTION, Value.VERY_BAD))
                        self.preference.add_criterion_value(CriterionValue(
                            item, CriterionName.DURABILITY, Value.BAD))
                        self.preference.add_criterion_value(CriterionValue(
                            item, CriterionName.ENVIRONMENT_IMPACT, Value.BAD))
                        self.preference.add_criterion_value(CriterionValue(
                            item, CriterionName.NOISE, Value.BAD))
            elif self.get_name() == "A_2":
                self.preference.set_criterion_name_list(
                    [CriterionName.PRODUCTION_COST, CriterionName.ENVIRONMENT_IMPACT, CriterionName.CONSUMPTION, CriterionName.DURABILITY, CriterionName.NOISE])
                for item in self.model._item_set:
                    if item.get_name() == "ICED":
                        self.preference.add_criterion_value(CriterionValue(
                            item, CriterionName.PRODUCTION_COST, Value.VERY_BAD))
                        self.preference.add_criterion_value(CriterionValue(
                            item, CriterionName.CONSUMPTION, Value.GOOD))
                        self.preference.add_criterion_value(CriterionValue(
                            item, CriterionName.DURABILITY, Value.GOOD))
                        self.preference.add_criterion_value(CriterionValue(
                            item, CriterionName.ENVIRONMENT_IMPACT, Value.GOOD))
                        self.preference.add_criterion_value(CriterionValue(
                            item, CriterionName.NOISE, Value.GOOD))
                    elif item.get_name() == "E":
                        self.preference.add_criterion_value(CriterionValue(
                            item, CriterionName.PRODUCTION_COST, Value.VERY_BAD))
                        self.preference.add_criterion_value(CriterionValue(
                            item, CriterionName.CONSUMPTION, Value.GOOD))
                        self.preference.add_criterion_value(CriterionValue(
                            item, CriterionName.DURABILITY, Value.GOOD))
                        self.preference.add_criterion_value(CriterionValue(
                            item, CriterionName.ENVIRONMENT_IMPACT, Value.GOOD))
                        self.preference.add_criterion_value(CriterionValue(
                            item, CriterionName.NOISE, Value.GOOD))
            else:
                self.generate_preferences(self, random_prefs=True)

    def argument_parsing(self, argument):
        """returns the premisses and the decision from recieved message

        Args:
            argument (Argument): the received argument

        Returns:
            premisses: list of premisses
            conclusion: the decision (boolean, item)
        """
        return argument.get_premisses(), argument.get_conclusion()

    def support_proposal(self, item):  # type item : Item
        """
        Used when the agent receives " ASK_WHY " after having proposed an item
        : param item : Item - item of the item which was proposed
        : return : string - the strongest supportive argument
        """
        if self.get_name() == 'A_1':
            usedArguments = self.__usedArguments[0]
        else:
            usedArguments = self.__usedArguments[1]
        print(self.get_name())
        print('used_argument in SUPPORT PROPOSAL', usedArguments)
        argument = Argument(True, item)
        argument.list_supporting_proposal(
            self.preference, usedArguments)
        argument.add_premiss()
        usedArguments[item.get_name()].append(
            str(argument).split('←  ')[1])
        # argument.get_premiss Regarder si y'a besoin de mettre le booleen, dico en clé item et argument les premiss utilisées
        print(usedArguments)
        return argument

    def attack_proposal(self, argument):  # type item : Item
        if self.get_name() == 'A_1':
            usedArguments = self.__usedArguments[0]
        else:
            usedArguments = self.__usedArguments[1]
        print(self.get_name())
        print('used_argument in ATTACK PROPOSAL', usedArguments)
        premisses, (_, proposed_item) = self.argument_parsing(argument)
        criterion_preference_order = self.preference.get_criterion_name_list()
        print('criterion_pref_order', criterion_preference_order)
        attacking_argument = Argument(False, proposed_item)
        print('attacking_arg', attacking_argument)
        attacking_argument.list_attacking_proposal(
            self.preference, usedArguments)
        print('attack_arg_premisses', attacking_argument.get_premisses())

        for premiss in premisses:
            if isinstance(premiss, CoupleValue):
                # Prefered criterion
                for criterion in reversed(criterion_preference_order):
                    if self.preference.is_preferred_criterion(criterion, premiss.get_criterion_name()):
                        comp = Comparison(
                            criterion, premiss.get_criterion_name())
                        attacking_argument.add_premiss(comp)
                        usedArguments[proposed_item.get_name()].append(
                            str(attacking_argument).split('←  ')[1])
                        print('used_argument in ATTACK PROPOSAL', usedArguments)
                        return attacking_argument

                # Lower value for the same criterion
                premiss = CoupleValue(premiss.get_criterion_name(), self.preference.get_value(
                    proposed_item, premiss.get_criterion_name()))
                if self.preference.get_value(proposed_item, premiss.get_criterion_name()).value < premiss.get_value().value:
                    attacking_argument.add_premiss(premiss)
                    usedArguments[proposed_item.get_name()].append(
                        str(attacking_argument).split('←  ')[1])
                    print('used_argument in ATTACK PROPOSAL', usedArguments)
                    return attacking_argument

                # Prefered criterion has low value
                for criterion in reversed(criterion_preference_order):
                    if self.preference.is_preferred_criterion(criterion, premiss.get_criterion_name()) and self.preference.get_value(proposed_item, premiss.get_criterion_name()) in [Value.BAD, Value.VERY_BAD]:
                        better_crit = Comparison(
                            criterion, premiss.get_criterion_name())
                        bad_value = CoupleValue(criterion, self.preference.get_value(
                            proposed_item, premiss.get_criterion_name()))
                        attacking_argument.add_premiss(better_crit)
                        attacking_argument.add_premiss(bad_value)
                        usedArguments[proposed_item.get_name()].append(
                            str(attacking_argument).split('←  ')[1])
                        print('used_argument in ATTACK PROPOSAL', usedArguments)
                        return attacking_argument

                # Other item with better value on the same criterion
                for item in self.model._item_set:
                    if self.preference.get_value(item, premiss.get_criterion_name()).value > premiss.get_value().value:
                        other_prop = Argument(True, item)
                        other_prop.list_supporting_proposal(self.preference)
                        better_value = CoupleValue(premiss.get_criterion_name(
                        ), self.preference.get_value(item, premiss.get_criterion_name()))
                        other_prop.add_premiss(better_value)
                        usedArguments[proposed_item.get_name()].append(
                            str(other_prop).split('←  ')[1])
                        print('used_argument in ATTACKING PROPOSAL',
                              usedArguments)
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
        self.iteration = 0

        # To be completed

        for agent_name in self.__list_agent_names:
            new_id = self.next_id()
            a = ArgumentAgent(new_id, self, agent_name, self._item_set)
            a.generate_preferences(random_prefs=False)
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

    def find_item_from_name(self, item_name):  # type de item_name : str
        for item in self._item_set:
            if item.get_name() == item_name.replace(' ', ''):
                return item

    def step(self):
        # self.argue()
        self.iteration += 1
        if self.iteration > 10:
            self.running = False
        self.__message_service.dispatch_messages()
        self.check_close_argumentation()
        self.schedule.step()


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
