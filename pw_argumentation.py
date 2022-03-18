from click import argument
from mesa import Model
from mesa.time import RandomActivation
from zmq import Message
from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService

class ArgumentAgent(CommunicatingAgent):
    """ArgumentAgent which inherits from CommunicatingAgent"""
    
    def __init__(self, unique_id, model, name):
        super().__init__(unique_id=unique_id, model=model, name=name)
        self.preference = None
    
    def step(self):
        super().step()
    
    def get_preference(self):
        return self.preference
    
    def generate_preferences(self, preferences):
        # see question 3
        # To be completed
        pass
    
class ArgumentModel(Model):
    """ArgumentModel which inherits from Model"""
    
    def __init__(self):
        self.schedule = RandomActivation(self)
        self.__message_service = MessageService(self.schedule)
        
        # To be completed
        #
        # a = ArgumentAgent(id, "agent_name")
        # a.generate_preference(preferences)
        # self.schedule.add(a)
        # ...
        
        self.running = True
        
    def step(self):
        self.__message_service.dispatch_messages()
        self.schedule.step()
        
if __name__ == "__main__":
    argument_model = ArgumentModel()
    
    # To be completed
    