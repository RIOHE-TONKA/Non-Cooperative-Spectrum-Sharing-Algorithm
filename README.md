# ABSTRACT

As the demand for wireless communication increases, the efficient use of the limited radio spectrum has become essential. This work presents the design and simulation of a non- cooperative spectrum sharing (NCSS) algorithm utilizing game theory and cognitive radio networks (CRN) to enhance the allocation of spectrum resources in dynamic wireless environments. CRNs provide a framework for secondary users (SUs) to opportunistically access frequency bands primarily designated for licensed or primary users (PUs). The focus of this solution is on the competition between PUs and SUs, with the algorithm simulating a scenario in which PUs are prioritized while SUs seeks for spectrum access in a non- cooperative fashion. We outline the formulation of the game, its execution, and its performance assessment using Jain's Fairness Index in a Python programming language-based simulation. The findings reveal the impact of non-cooperative strategies on spectrum usage and user fairness.

# Keywords:
Non-Cooperative Spectrum Sharing, Game Theory, Fairness, Primary User, Secondary User, Cognitive Radio

# Implementation

The implemented algorithm manages spectrum access for primary users (PUs) and secondary users (SUs) in a cognitive radio network (CRN) with limited available channels. The algorithm prioritizes PUs, as they have a higher priority for spectrum access, while SUs opportunistically access the channels when they are free. The algorithm maintains a queue for each type of user and allocates channels based on availability and user priority. Below is a step-by-step breakdown of the algorithm's functioning.
 
# 1	Initialization and User Type Check
•	The process begins by checking the type of user requesting channel access, distinguishing between a PU or SU.
•	Depending on the type, different checks and actions are applied to allocate channels while ensuring prioritized access for PUs.

# 2	Primary User (PU) Arrival
When a PU arrives, the algorithm checks if there is an available channel.
•	If an available channel is found: The PU occupies it immediately, as PUs have priority in the system. The system then continues to handle subsequent user arrivals.
•	If no channel is available: The algorithm checks if the occupied channel is currently held by a SU.
•	If a SU occupies the channel: The SU’s connection is terminated, and the PU occupies the channel. The SU is then added to the queue, awaiting the next available channel.
•	If all channels are occupied by PUs: The incoming PU must wait or is blocked. A counter is incremented to reflect the blocked PU count. The PU is added to a queue, pending an available channel given the limitation in channels.

This prioritization mechanism ensures that PUs, who are higher-priority users, gain access to the spectrum even at the cost of interrupting an SU’s session.
# 3	Secondary User (PU) Arrival
When an SU arrives, the algorithm performs a random check to see if there is an open channel in the spectrum.
•	If an open channel is available: The SU is placed on this available channel, allowing it to use the spectrum opportunistically without disrupting PUs.
•	If no channel is available: The SU must wait or is blocked. A counter for blocked SUs is incremented, and the SU is added to the queue.
Since SUs have a lower priority, they are only allocated channels if no PU requires access. SUs must yield their channels to PUs whenever necessary, aligning with the hierarchy of user types in a CRN.

# 4	Connection Termination and Reallocation
•	The algorithm includes periodic checks for the termination of connectivity in channels. If a user completes their usage, the channel becomes available for the next user in the queue.
•	When connectivity is terminated, the process begins again from the start, allowing queued users to access newly available channels in accordance with their priority.

# 5	Repeating the Process
This loop of user checks, channel allocation, and reallocation continues iteratively. Each time a channel becomes free, the algorithm revisits the queue to allocate resources based on user
 type, ensuring that PUs are given priority access while SUs utilize the remaining capacity. See figure below showing the flowchart.


![Picture1](https://github.com/user-attachments/assets/9ec78997-b535-4e10-9aef-f4a04971a4d8)




