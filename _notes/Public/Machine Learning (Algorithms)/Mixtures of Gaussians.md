---
title: Mixtures of Gaussians
---
# Mixtures of Gaussians

| Type       |
| ---------- |
| Clustering |

# The Concept of Latent Variables
Unlike standard [[k-Means]], which assigns each point to exactly one cluster, a Mixture of Gaussians assumes that the data is generated from a combination of several Gaussian distributions.
- **Latent Variable ($z$):** A hidden variable that represents which Gaussian component a data point belongs to.
- **Generative Process:** To generate a point, you first pick a cluster $k$ with probability $\pi_k$ (the mixing coefficient), and then draw a sample from that specific Gaussian $N(\mu_k, \Sigma_k)$.

---

# Hard vs. Soft Clustering
The most significant difference between K-Means and MoG is the type of assignment:
- **K-Means (Hard):** Every point belongs to exactly one cluster. This can be problematic for points located right between two clusters.
- **MoG (Soft):** Every point has a "responsibility" weight. A point might be $70\%$ likely to belong to Cluster A and $30\%$ likely to belong to Cluster B. This is expressed as the posterior probability $P(z_k | x)$.

---

# The EM Algorithm (Expectation-Maximization)
Since we don't know which point belongs to which cluster (the latent variables are hidden), we cannot use standard Maximum Likelihood Estimation. Instead, we use the **EM Algorithm**, an iterative process:
### E-Step (Expectation)
Calculate the responsibility ($\gamma$) that each component $k$ has for each data point $i$. This is based on the current parameters of the Gaussians:

$$\gamma(z_{ik}) = \frac{\pi_k \mathcal{N}(x_i | \mu_k, \Sigma_k)}{\sum_{j=1}^{K} \pi_j \mathcal{N}(x_i | \mu_j, \Sigma_j)}$$

### M-Step (Maximization)
Update the parameters ($\mu, \Sigma, \pi$) to better fit the data, weighted by the responsibilities calculated in the E-step:
- **New Mean ($\mu_k$):** The weighted average of all points.
- **New Covariance ($\Sigma_k$):** The weighted covariance of the points.
- **New Mixing Coefficient ($\pi_k$):** The average responsibility assigned to component $k$.

---

# Key Advantages and Comparison
- **Flexibility:** While K-Means assumes clusters are spherical (circular), MoG can handle **elliptical clusters** of different sizes and orientations by adjusting the covariance matrix $\Sigma$.
- **Overlapping Clusters:** MoG handles overlapping data much more gracefully than K-Means due to its probabilistic "soft" assignments.
- **Density Estimation:** MoG provides a full probability density function for the entire dataset, not just cluster centers.

|**Feature**|**K-Means**|**Mixture of Gaussians (MoG)**|
|---|---|---|
|**Assignment**|Hard (0 or 1)|Soft (Probabilistic)|
|**Cluster Shape**|Spherical|Elliptical (Flexible)|
|**Optimization**|Minimize Inertia|Maximize Likelihood (via EM)|
|**Complexity**|Low / Fast|Moderate / Slower|
