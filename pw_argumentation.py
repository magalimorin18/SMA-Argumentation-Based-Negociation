from os import name
from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.preferences.Preferences import Preferences
from communication.preferences.Item import Item
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.CriterionName import CriterionName
from communication.preferences.Value import Value

class ArgumentAgent(CommunicatingAgent):
    """ArgumentAgent which inherits from CommunicatingAgent"""
    
    def __init__(self, unique_id, model, name):
        super().__init__(unique_id=unique_id, model=model, name=name)
        self.preference = Preferences()
    
    def step(self):
        super().step()
    
    def get_preference(self):
        return self.preference
    
    def generate_preferences(self):
        # see question 3
        # To be completed
        
        # Random criterion priorities
        criterion_list = list(CriterionName)
        self.random.shuffle(criterion_list)
        self.preference.set_criterion_name_list(criterion_list)
        
        # Random generation of preferences for all criteria
        for item in self.model.items_list:
            for criterion in self.preference.get_criterion_name_list():
                item_criterion_pref = CriterionValue(item, criterion, self.random.choice(list(Value)))
                self.preference.add_criterion_value(item_criterion_pref)
    
class ArgumentModel(Model):
    """ArgumentModel which inherits from Model"""
    
    def __init__(self, items_list, list_agent_names):
        super().__init__(self)
        self.schedule = RandomActivation(self)
        self.__message_service = MessageService(self.schedule)
        self.items_list = items_list
        self.__list_agent_names = list_agent_names
        
        # To be completed
        
        for agent_name in self.__list_agent_names:

            a = ArgumentAgent(self.next_id(), self, agent_name)
            a.generate_preferences()
            self.schedule.add(a)

        self.running = True
        
    def step(self):
        self.__message_service.dispatch_messages()
        self.schedule.step()
        
if __name__ == "__main__":
    # To be completed
    items_list = [Item("ICED", "Diesel"), Item("E", "Electric")]
    agents_name = ["A_1", "A_2"]
    model = ArgumentModel(items_list=items_list, list_agent_names=agents_name)
    model.step()
    