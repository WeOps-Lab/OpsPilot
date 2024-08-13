# KPCA


Algorithm Overview

Kernel Principal Component Analysis (KPCA) is a nonlinear extension method of Principal Component Analysis (PCA). Since operational data often contains complex temporal dependencies, trends, etc., the distribution of operational data is usually nonlinear, so KPCA is more suitable for anomaly detection than PCA. KPCA maps the training data to an infinite-dimensional feature space and extracts the principal components of the data distribution from this space. It reconstructs the data using the principal components and indicates the degree of anomaly by calculating the reconstruction error.

## Usage Scenarios

It is suitable for <font color='red'>nonlinear data distribution, with complex data structures</font> for anomaly detection, and traditional linear methods such as PCA cannot accurately capture the underlying patterns in the data. If the data structure is complex, KPCA can handle complex data better by using kernel functions and an infinite-dimensional feature space.

#### 3. Algorithm Principle

![Excalidraw Image](./img/KPCA.png)

(1) Data preprocessing: Cleaning, standardizing, or normalizing the input data;

(2) Data mapping: Using selected kernel functions to map the data to an infinite-dimensional feature space. Common kernel functions include Gaussian kernel functions and polynomial kernel functions;

(3) Feature extraction: Applying KPCA to extract the principal components of the data in the mapped feature space. This can be achieved through steps such as calculating the similarity matrix, centering the Gram matrix, and extracting feature vectors;

(4) Calculating the reconstruction error: Reconstruct the data using the extracted principal components and calculate the reconstruction error (i.e. the gap between the original data and the reconstructed data);

(5) Anomaly detection: Use the reconstruction error as an anomaly measure and classify the data into normal or anomalous by setting a threshold.

**Paper original link**: [https://www.heikohoffmann.de/documents/hoffmann_kpca_preprint.pdf](https://www.heikohoffmann.de/documents/hoffmann_kpca_preprint.pdf)