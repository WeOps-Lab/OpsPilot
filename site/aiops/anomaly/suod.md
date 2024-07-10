# Suod

## 算法简介

训练或者用大量无监督模型做预测会面临巨大的开销问题，尤其在高维度、大数据上，很多时候甚至无法收敛，因此提出了SUOD。SUOD是异质无监督模型，通过JL Projection降维解决高维问题，使用近似regressor替代无监督模型加速预测过程，并对模型的训练进行平衡的并行调度从而提高系统运行性能。

## 使用场景

本算法适用于数据维度较高,对处理速度有一定要求的情况

## 算法原理
![Excalidraw Image](./img/SUOD.png)

简单来说，当输入x_train训练数据后首先会对高维的训练数据进行降维操作，然后再并行训练多个基础model并得到每个model的权重，保存训练得到的y_train。再用x_train和y_train训练近似model（默认用随机森林），若近似的model比基础model性能好将会对基础模型进行替换。当输入x_text对数据已经异常检测时，则会调用训练好的近似model/基础model对每个sample进行异常分数计算，加权得到最终的集成异常分数，再将异常分数与阙值进行比较。

**论文链接**：<https://www.andrew.cmu.edu/user/yuezhao2/papers/21-mlsys-suod.pdf>