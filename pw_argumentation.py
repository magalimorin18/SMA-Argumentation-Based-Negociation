from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.preferences.Preferences import Preferences
from communication.preferences.Item import Item
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.CriterionName import CriterionName
from communication.preferences.Value import Value
from communication.message.Message import Message
from communication.message.MessagePerformative import MessagePerformative

class ArgumentAgent(CommunicatingAgent):
    """ArgumentAgent which inherits from CommunicatingAgent"""

    def __init__(self, unique_id, model, name, item_set):
        super().__init__(unique_id=unique_id, model=model, name=name)
        self.preference = Preferences()
        self._item_set = item_set.copy()
        self.__committed = False

    def step(self):
        #TODO: Add unit tests
        super().step()
        # print(f"{self.get_name()}'s turn")
        list_messages = self.get_new_messages()
        for message in list_messages:
            print(message)
            # print(f"Agent {self.get_name()} has right performative: {message.get_performative() in [MessagePerformative.ACCEPT, MessagePerformative.COMMIT]}")
            # print(f"Agent {self.get_name()} has item in set: {message.get_content() in self._item_set}")
            # print(f"Agent {self.get_name()} has item set: {self._item_set}")
            if (message.get_performative() == MessagePerformative.PROPOSE) and (message.get_content() in self._item_set):
                if self.preference.is_item_among_top_10_percent(message.get_content(), self._item_set):
                    self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ACCEPT, content=message.get_content()))
                else:
                    self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.ASK_WHY, content=message.get_content()))
                    self.__committed = True
            if (message.get_performative() == MessagePerformative.ACCEPT) and (message.get_content() in self._item_set):
                # print(f"Got through that condition for {self.get_name()}")
                self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.COMMIT, content=message.get_content()))
                self._item_set.remove(message.get_content())
            if (message.get_performative() == MessagePerformative.COMMIT):
                self.__committed = True
                if message.get_content() in self._item_set:
                    self.send_message(Message(from_agent=self.get_name(), to_agent=message.get_exp(), message_performative=MessagePerformative.COMMIT, content=message.get_content()))
                    self._item_set.remove(message.get_content())
                    
            if (message.get_performative() == MessagePerformative.ASK_WHY) and (message.get_content() in self._item_set):
                self.__committed = True

    def get_preference(self):
        return self.preference
    
    def has_committed(self):
        return self.__committed

    def generate_preferences(self):
        # see question 3
        # To be completed
        # TODO: Add a csv filename argument to generate preferences (need to discuss about the formatting)

        # Random criterion priorities
        criterion_list = list(CriterionName)
        self.random.shuffle(criterion_list)
        self.preference.set_criterion_name_list(criterion_list)

        # Random generation of preferences for all criteria
        for item in self._item_set:
            for criterion in self.preference.get_criterion_name_list():
                item_criterion_pref = CriterionValue(item, criterion, self.random.choice(list(Value)))
                self.preference.add_criterion_value(item_criterion_pref)

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
            a = ArgumentAgent(new_id, self, agent_name, self._item_set)
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
        
    def step(self):
        # self.argue()
        self.__message_service.dispatch_messages()
        self.schedule.step()
        self.check_close_argumentation()
            

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
