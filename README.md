# SMA-Argumentation-Based-Negociation

**WARNING:** Always run scripts from project root directory!

# Run the code

Set up the environment:

1. Go to the root directory
2. Install requirements
3. run the `pw_argumentation.py` script

# Goal of the project

The project aims at creating an environment and agents who are able to negotiate on a purchase decision (for example for cars) using an argumentation based approach. The agents use their own evaluation on car features to build their argumentation.

# Argumentation principle

The first step for both agent is to propose an item (each agent propose a different item).

If the item is the prefered one for the other, then it accepts it then commits are done.

Otherwise, the agent asks why this item has been proposed.

Then the first agent supports its proposal using the least important criterion with a high value (e.g. Production cost is very good).

After that, the second agent argues by attaking the proposal based on the received argument. It tries to find a better criterion with lower value, or another item with a better value on this criterion.

Then the supporter finds another counter-argument to support its proposal.

And so on until one of the agents runs out of arguments and accept or decide to propose another item.

We stored all the arguments in a dictionnary in understand the argumentation. This dictionnary is also used to not repeat the same argument twice. 

# Our environment setup

We have set up the environment and the agent according to the guidelines of the project. Basically, we have 2 agents $A_1$ and $A_2$ and 2 cars E (Electric) and ICED (Diesel).

Their preferences are detailed in the guidelines and incites the agent $A_1$ to propose the ICED whereas the agent $A_2$ is more into the Electric car.

# Progress of the project
- Before we implemented the dictionary that kept a history of the arguments used, our two agents debated endlessly, always putting forward the same argument.
![Capture d’écran (308)](https://user-images.githubusercontent.com/51906903/163631985-7c8884ae-1fc4-47f4-a2ce-c956078e83b5.png)

- Here is an example of an argumentation between the two agents.
![Capture d’écran (309)](https://user-images.githubusercontent.com/51906903/163631996-45713100-2d31-421c-835c-5757f67e68cc.png)

