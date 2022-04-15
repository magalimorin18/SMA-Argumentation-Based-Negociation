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

# Our environment setup

We have set up the environment and the agent according to the guidelines of the project. Basically, we have 2 agents $A_1$ and $A_2$ and 2 cars E (Electric) and ICED (Diesel).

Their preferences are detailed in the guidelines and incites the agent $A_1$ to propose the ICED whereas the agent $A_2$ is more into the Electric car.

