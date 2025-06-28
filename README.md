# ABSTRACT

As the demand for wireless communication increases, the efficient use of the limited radio spectrum has become essential. This work presents the design and simulation of a non- cooperative spectrum sharing (NCSS) algorithm utilizing game theory and cognitive radio networks (CRN) to enhance the allocation of spectrum resources in dynamic wireless environments. CRNs provide a framework for secondary users (SUs) to opportunistically access frequency bands primarily designated for licensed or primary users (PUs). The focus of this solution is on the competition between PUs and SUs, with the algorithm simulating a scenario in which PUs are prioritized while SUs seeks for spectrum access in a non- cooperative fashion. We outline the formulation of the game, its execution, and its performance assessment using Jain's Fairness Index in a Python programming language-based simulation. The findings reveal the impact of non-cooperative strategies on spectrum usage and user fairness.

# Keywords:
Non-Cooperative Spectrum Sharing, Game Theory, Fairness, Primary User, Secondary User, Cognitive Radio

# Implementation

Explained to detail, it is divided into two main sections: The non-cooperative spectrum sharing algorithm and the simulation program.

# 1	NCSS algorithm
The implemented algorithm manages spectrum access for primary users (PUs) and secondary users (SUs) in a cognitive radio network (CRN) with limited available channels. The algorithm prioritizes PUs, as they have a higher priority for spectrum access, while SUs opportunistically access the channels when they are free. The algorithm maintains a queue for each type of user and allocates channels based on availability and user priority. Below is a step-by-step breakdown of the algorithm's functioning.
 
# 1.1	Initialization and User Type Check
•	The process begins by checking the type of user requesting channel access, distinguishing between a PU or SU.
•	Depending on the type, different checks and actions are applied to allocate channels while ensuring prioritized access for PUs.

# 1.2	Primary User (PU) Arrival
When a PU arrives, the algorithm checks if there is an available channel.
•	If an available channel is found: The PU occupies it immediately, as PUs have priority in the system. The system then continues to handle subsequent user arrivals.
•	If no channel is available: The algorithm checks if the occupied channel is currently held by a SU.
•	If a SU occupies the channel: The SU’s connection is terminated, and the PU occupies the channel. The SU is then added to the queue, awaiting the next available channel.
•	If all channels are occupied by PUs: The incoming PU must wait or is blocked. A counter is incremented to reflect the blocked PU count. The PU is added to a queue, pending an available channel given the limitation in channels.

This prioritization mechanism ensures that PUs, who are higher-priority users, gain access to the spectrum even at the cost of interrupting an SU’s session.
# 1.3	Secondary User (PU) Arrival
When an SU arrives, the algorithm performs a random check to see if there is an open channel in the spectrum.
•	If an open channel is available: The SU is placed on this available channel, allowing it to use the spectrum opportunistically without disrupting PUs.
•	If no channel is available: The SU must wait or is blocked. A counter for blocked SUs is incremented, and the SU is added to the queue.
Since SUs have a lower priority, they are only allocated channels if no PU requires access. SUs must yield their channels to PUs whenever necessary, aligning with the hierarchy of user types in a CRN.

# 1.4	Connection Termination and Reallocation
•	The algorithm includes periodic checks for the termination of connectivity in channels. If a user completes their usage, the channel becomes available for the next user in the queue.
•	When connectivity is terminated, the process begins again from the start, allowing queued users to access newly available channels in accordance with their priority.

# 1.5	Repeating the Process
This loop of user checks, channel allocation, and reallocation continues iteratively. Each time a channel becomes free, the algorithm revisits the queue to allocate resources based on user
 type, ensuring that PUs are given priority access while SUs utilize the remaining capacity. See figure below showing the flowchart.


![Picture1](https://github.com/user-attachments/assets/9ec78997-b535-4e10-9aef-f4a04971a4d8)


# 2	NCSS Simulation
The simulation is implemented using python programming language as framework, where a plot is considered to depict the spectrum which comprises of channels as central idea. As indicated in the algorithm flowchart, we are dealing with an iterative process therefore it only makes sense that the simulation is of same nature.

As players, spectrum users are added based on the choice selection of the person running the simulation, meaning is an arbitrary process. Given that those players are assumed to be rational there’s a decision that undergoes each time one is added to the spectrum before it can be allocated a channel (explained in previous section). Initially, there are no users in the spectrum hence the host machine user is prompted to do so as wishes as seen in the figure below.

![image](https://github.com/user-attachments/assets/25fa8d0a-f27c-425a-869c-6bd8fbdd9082)

The actual spectrum is depicted using a plot which becomes dynamic given the choices of the host machine user. Such a spectrum is composed of a number of 5 channels, where each can accommodate one user at a time. The blue bars as indicated represent PU’s whereas the green ones SU’s. See figure below, showing 3 users added to spectrum. Needless to mention that there are availabilities in the spectrum hence they could be added.
![image](https://github.com/user-attachments/assets/e6e1795a-6a19-4cb8-b9c2-be75df6695ca)

Figure 7 below shows a well filled spectrum, what’s interesting to highlight is shown in figure 8, where a PU is added to occupy the spectrum. Given those hold priority to occupy channels, a SU is then removed from one channel in this case channel 4 to accommodate the coming of PU4, which is then queued as it waits for availability again as explained in the algorithm.
![image](https://github.com/user-attachments/assets/a27aa0ba-488c-4856-8466-03e971adbc4d)

 
The algorithm is then satisfied when the SU is moved to a queue as it again waits for a chance to opportunistically access the spectrum.
![image](https://github.com/user-attachments/assets/6692bbee-bc9d-4090-bdd9-812a619ddd82)


Through the console, the current statistics of the spectrum are displayed after performing the above-mentioned moves which led to the execution of some strategies by players

<img width="459" alt="image" src="https://github.com/user-attachments/assets/6b23b5b9-8b0a-4015-83e5-e7836618b390" />


It’s also important to note that, a menu is provided in which the host machine user can perform a set of actions for more in depth knowledge of the spectrum. See figure 9 below, in which the simulation was started over.
<img width="459" alt="image" src="https://github.com/user-attachments/assets/081e2859-bf00-4f53-8224-c87141175784" />

 
Let’s have a look at how fairness is evaluated using Jain’s fairness index. For that, there is an amount of time allocated to each user that manages to access the spectrum. Such time is then assigned through a mechanism for calculation period (not real time assignation).

<img width="453" alt="image" src="https://github.com/user-attachments/assets/88b2a8d9-d7d4-4bb0-bddb-87625d1e382c" />


Given these parameters as listed in figure 11, jains index is used as explained in the equation below. Figure 12 is the plot at that time.

![image](https://github.com/user-attachments/assets/fee047ec-ec7d-4ddb-b4f4-357ae6d964c1)


That’s, using equation below we obtain the fairness index of 0.736, what this indicates is that the utilization of the spectrum is of 73.6% if PU1 is active for 8 seconds, the SU1 is active for 6 seconds, PU2 for 3 seconds and finally SU2 for 1 second.

<img width="891" alt="image" src="https://github.com/user-attachments/assets/9e623f7c-1b84-4180-a99d-99fbb9227fa4" />



