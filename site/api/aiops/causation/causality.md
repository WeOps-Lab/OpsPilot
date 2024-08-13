# causality 
 
## Algorithm introduction 
 
A probabilistic causal model is a framework for dealing with causality that uses probability distributions to describe the causal relationship between variables. The causality library used in this paper implements the Inductive Causation with latent variables (IC) algorithm, which is an inference method based on directed graph. The causal relationship between variables is inferred by observing the conditional independence relationship between them. The IC algorithm constructs a graph model by testing the conditional independence of the raw data, where each node represents a variable and the directed edge represents the causal relationship between the variables. The algorithm first constructs a complete directed graph, then gradually reduces unnecessary edges through a series of recursive rules, and finally gets a reasonable causal graph model. 
 
## Use scenario 
 
This algorithm is suitable for causal inference of 'discrete' data 
 
## Algorithm principle 
 
The core idea of the algorithm is to use the conditional independence relation to infer causality through the statistical characteristics of the observed data. It can deal with issues such as latent variables and selective omissions, and is able to make inferences in complex networks of causation. The specific process is as follows: 
 
(1) Data preparation: discrete data, such as four nodes A, B, C and D, node A appears as 1, and node a does not appear as 0; 
 
(2) Build a complete graph: Build a directed complete graph where each node has a directed edge link with other nodes; 
 
(3) Conditional independence test: For each pair of variables in the figure, conditional independence test is carried out to determine whether causality exists; 
 
(4) Recursion: Based on the results of the conditional independence test, a series of recursive rules are applied to gradually reduce the edges in the graph. Recursive rules include: (1) If variable A and variable B are conditionally independent, and variable B is conditionally independent from variable C, then it can be inferred that there is no direct causal relationship between variable A and variable C, and the edge between A and C is removed; (2) If variable A is conditionally independent of variable B, and variable C is A common neighbor of A and B (that is, has an edge connection with both A and B), then A common causal relationship between variables A and B can be inferred, and an edge is added between A and B; 
 
(5) Determine the direction of the directed edge: Determine the direction of the directed edge by observing the order in which the variable is operated during the recursive rule process. If an edge is added to a variable and then removed or replaced multiple times, then the edge can confirm the direction; 
 
(6) Get the final causal graph: After processing by recursive rules, the resulting graph is the final causal graph, representing the causal relationship between variables.