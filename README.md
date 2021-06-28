# PAMELA-DEV
PAMELA is a novel generic collaborative open-source MAS framework that aims at being light, beginner-friendly, and that allows for fast prototyping through assisted scenario generation and powerful configuration. The tool can work with or without (for faster simulations) the integrated graphical user interface (designed for both testing and visualization). To make is more attractive to new programmers and to enable an easier interfacing with trending machine learning frameworks, PAMELA is entirely written in Python and only relies on standard libraries. 

## Instalation
1. Clone this repository
2. In terminal install depence : "pip -r requirment.txt"
3. run pamela.py after adapt configuration

## prerequisites
Using pamela is very simple. The "Agent" class can be specified or you can use the generic "StandardAgent" class.
You must know the basics of multi-agent systems : https://en.wikipedia.org/wiki/Multi-agent_system

## Scenario and setup.
Pamela has a configuration wizard. 

![alt text](https://github.com/BDafflon/PAMELA-DEV/blob/master/doc/conf2-1.png)
That open new window :
![alt text](https://github.com/BDafflon/PAMELA-DEV/blob/master/doc/conf2.png)


However, if you are comfortable with json files, it will be easier to use the files proposed in the scenario folder. It is structured as :

![alt text](https://github.com/BDafflon/PAMELA-DEV/blob/master/doc/file.png)

You can launch the scenarios at the start of the simulation or intervene according to your needs
![alt text](https://github.com/BDafflon/PAMELA-DEV/blob/master/doc/Pamela2.gif)


## Simulation examples:
### SIR simulation :
The global health crisis of the Covid-19 Coronavirus has demonstrated the role of modelling in political and health decision making. A classic model in the literature for decision support is the "Compartmental models" such as the SIR model

![alt text](https://github.com/BDafflon/PAMELA-DEV/blob/master/doc/sim1.png)

### Taxis optimisation
Mobility-on-Demand (MoD) systems offer a flexible mobility alternative to classical public transportation services in urban areas. However, a significant part of MoD vehicles operating time can be spent waiting empty or driving to reach new potential ride re-quests.


