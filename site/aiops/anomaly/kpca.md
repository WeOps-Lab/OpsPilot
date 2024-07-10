# KPCA


## 算法简介

核主成分分析(Kernel Principal Component Analysis, KPCA)是主成分分析(Principal Component Analysis, PCA)的一种非线性扩展方法。由于运维数据往往包含复杂的时间依赖性、趋势等这些因素使得运维数据的分布通常是非线性的，因此采用KPCA进行异常检测比PCA更为合适。KPCA通过将训练数据映射到一个无线维的特征空间中，从该空间中提取数据分布的主成分，使用主成分对数据进行重构，通过计算重构误差指示数据的离群程度。

## 使用场景

适用于<font color='red'>非线性数据分布、具有复杂数据结构</font>的异常检测，传统的线性方法如PCA无法准确捕捉数据中的一场模式，如果数据结构较复杂，KPCA能过够通过核函数和无线维特征空间更好处理复杂的数据。

#### 3. 算法原理

![Excalidraw Image](./img/KPCA.png)

(1) 数据预处理：对输入数据进行清洗、标准化或归一化；

(2) 数据映射：使用选择的核函数将数据映射到一个无限维的特征空间中。常用的核函数包括高斯核函数核多项式核函数；

(3) 特征提取：在映射后的特征空间中应用KPCA提取数据的主成分。可以通过计算相似度矩阵、去中心化的Gram矩阵和特征向量等步骤实现；

(4) 计算重构误差：使用提取的主成分对数据进行重构，并计算重构误差（即原始数据与重构数据之间的差距）；

(5) 异常检测：利用重构误差作为异常度量，通过设定阈值将数据分类为正常或异常。

**论文原文链接**：[https://www.heikohoffmann.de/documents/hoffmann_kpca_preprint.pdf](https://www.heikohoffmann.de/documents/hoffmann_kpca_preprint.pdf)
