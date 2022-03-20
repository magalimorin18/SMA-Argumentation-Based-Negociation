from os import name
from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.preferences.Preferences import Preferences
from communication.preferences.Item import Item
from communication.preferences.CriterionValue import CriterionValue
from communication.preferences.CriterionName import CriterionName

class ArgumentAgent(CommunicatingAgent):
    """ArgumentAgent which inherits from CommunicatingAgent"""
    
    def __init__(self, unique_id, model, name):
        super().__init__(unique_id=unique_id, model=model, name=name)
        self.preference = None
    
    def step(self):
        super().step()
    
    def get_preference(self):
        return self.preference
    
    def generate_preferences(self, list_items):
        # see question 3
        # To be completed
        pass
    
class ArgumentModel(Model):
    """ArgumentModel which inherits from Model"""
    
    def __init__(self, items_list, list_agent_names):
        self.schedule = RandomActivation(self)
        self.__message_service = MessageService(self.schedule)
        self.items_list = items_list
        self.list_agent_names = list_agent_names
        
        # To be completed
        
        for agent_name in self.list_agent_names:

            a = ArgumentAgent(0, agent_name)
            a.generate_preference(self.items_list)
            self.schedule.add(a)

        self.running = True
        
    def step(self):
        self.__message_service.dispatch_messages()
        self.schedule.step()
        
if __name__ == "__main__":
    argument_model = ArgumentModel()
    
    # To be completed
    items_list = [Item("ICED", "Diesel"), Item("E", "Electric")]
    agents_name = ["A_1", "A_2"]
    model = ArgumentModel(items_list=items_list, list_agent_names=agents_name)
    