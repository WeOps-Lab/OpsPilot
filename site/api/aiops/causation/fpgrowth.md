# FP-Growth 
 
## Algorithm introduction 
 
Frequent pattern growth (fp-growth) algorithm is a data mining algorithm for mining frequent item sets. Based on the prefix tree data structure (called FP tree), it can efficiently discover frequent item sets by using the local properties of frequent items and the compression technique of prefix tree. The main idea of FP-growth algorithm is to construct FP tree first, and then discover frequent item sets by traversing FP tree and constructing conditional pattern basis 
 
## Use scenario 
 
This algorithm is suitable for processing large-scale and high-dimensional data, and it is also an unsupervised learning method, which is suitable for the case of no labels 
 
## Algorithm principle 
 
The advantage of the FP-growth algorithm is that it only needs to scan the data set twice, so it is more efficient than Apriori. In addition, the FP-growth algorithm uses compression techniques to reduce the need for storage space and can handle large data sets. With the FP-growth algorithm, we can find frequent item sets, that is, sets of items that often appear together. The specific steps of the algorithm are as follows: 
 
(1) Traverse the data set, calculate the support degree of each item, and sort according to the support degree in descending order; 
 
(2) Construct FP tree: traverse the data set, sort each transaction according to the support degree of frequent items in descending order, and insert the sorted transactions into the FP tree; 
 
(3) The conditional schema base (constructed by the prefix path of the node) of each node in the FP tree is recursively mined for frequent item sets; 
 
(4) The conditional pattern tree is constructed according to the conditional pattern base, and then the conditional pattern tree is recursively mined; 
 
(5) Repeat steps 3 and 4 until there are no more frequent item sets to mine.