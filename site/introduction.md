# Introduction 
 
OpsPilot is an open source intelligent operation and maintenance assistant based on cutting-edge artificial intelligence technology from the WeOps team. It uses advanced machine learning, deep learning and cutting-edge large model capabilities as AI capabilities, and supports rich operation and maintenance integration capabilities to provide intelligent operation and maintenance services 
 
![architecture diagram](https://static.cwoa.net/01adc49936ae41d68dded993461a7dd0.jpg) 
 
OpsPilot includes three main capabilities: 
 
> * Powerful private domain knowledge Q&A 
> * Efficient ChatOps 
> * Insightful intelligent guidance 
 
Product highlights: 
 
> * Multi-channel connection with users 
> * Rich AIOPS model 
> * Comprehensive data integration capabilities 
 
## Core concept 
 
In OpsPilot, there are the following core concepts: 
 
* **Robot** : Every robot is a Pilot. The Pilot is scheduled by K8S to contact the user through the channel 
* **AI model** : AI model provides AI skills for the Pilot, it can be simply said that the expansion pack tells the Pilot what actions can be done, AI model provides magic for actions 😁. AI models can also provide services directly to the outside world 
Integration: Integration is how Pilot interacts with external systems, including K8S, Jenkins, Gitlab, WeOps Lite, and more 
* **Channel** : Channel is the channel for Pilot to connect with users, including Dingding, Web, enterprise wechat 
* **Knowledge Base** : Knowledge base provides RAG support for robots, so that robots can recover private domain knowledge 
 
## Explicit knowledge & Implicit knowledge 
 
**Explicit knowledge** : We believe that in the operation and maintenance system, all directly expressed, such as CMDB asset association, alarm information, indicator information, etc., are explicit knowledge 

**Tacit knowledge**: We believe that in the operation and maintenance system, everything that needs to be obtained through reasoning, calculation, prediction and other ways, such as root cause analysis, predictive alarm, etc., through the AIOPS algorithm to extract and analyze the explicit knowledge, uniformly called tacit knowledge 
 
## Intelligent guidance 
 
OpsPilot has not yet positioned itself as a Virtual SRE, and we believe that at this stage, the reliability of letting large models play too much subjective initiative in the field of operation and maintenance is not high. Therefore, we are more inclined to combine the advantages of task-based robots and conversational robots to guide users to complete operation and maintenance tasks step by step, or analyze the root causes of alarms