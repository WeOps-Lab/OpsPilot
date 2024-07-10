# INNE

## 算法简介

为克服IForest算法在数值型数据上不擅长处理局部相对稀疏点、不适用于特别高维度的数据等问题，适用最近邻集成的基于隔离的异常检测(Isolation‐Based Anomaly Detection Using Nearest‐Neighbor Ensembles, INNE)借鉴孤立机制并结合最近邻距离计算方法，采用多维超球体切割数据空间实现孤立机制，并考虑了数据局部分布特性。

## 使用场景
适用于<font color='red'>低相关性指标数据</font>的异常检测，该算法能够很好适应不同数据集中的异常情况，能够方便处理<font color='red'>高维度数据</font>，捕捉高维空间中局部异常的情况。

## 算法原理
![Excalidraw Image](./img/INNE.png)<br>

在训练阶段，从训练集中随机抽取t个子样本构建一个超球集合，对每个数据点进行最近邻搜索，找到与之距离最近的邻居，并基于邻居的属性计算最小的超球体半径，使得超球体能过够包含当前数据点和其邻居。在测试阶段，将每个测试的数据点放进每个超球体中计算孤立得分，根据所在超球体的相对大小和邻居超球体大小的比值进行计算，然后取平均值作为最终的异常值。

**论文原文链接**：<https://www.researchgate.net/profile/Tharindu-Bandaragoda/publication/322359651_Isolation-based_anomaly_detection_using_nearest-neighbor_ensembles_iNNE/links/5e91651092851c2f5294c5ac/Isolation-based-anomaly-detection-using-nearest-neighbor-ensembles-iNNE.pdf>
