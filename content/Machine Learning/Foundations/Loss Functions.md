---
title: Loss Functions
tags:
  - machine-learning
  - model-evaluation
  - auto-captured
draft: false
---
In machine learning, **loss functions** (or cost functions) are mathematical formulas used to measure the difference between a model's predicted output and the actual target values. The model uses this error metric during training to update its weights and improve its accuracy. 

The choice of loss function depends primarily on the type of task: **Regression** or **Classification**.

## 1. Regression Loss Functions
Used when the goal is to predict a continuous numerical value (e.g., price, temperature).

- **Mean Squared Error (MSE / L2 Loss):** 
  - **What it is:** The average of the squared differences between predicted and actual values.
  - **Pros/Cons:** It penalizes larger errors more heavily because of the squaring. It is very common but highly sensitive to outliers.
- **Mean Absolute Error (MAE / L1 Loss):** 
  - **What it is:** The average of the absolute differences between predicted and actual values.
  - **Pros/Cons:** Generally more robust to outliers than MSE.
- **Huber Loss:** 
  - **What it is:** A combination of MSE and MAE. It acts like MSE when errors are small and like MAE when errors are large.
  - **Pros/Cons:** Less sensitive to outliers than MSE while remaining differentiable at zero.

## 2. Classification Loss Functions
Used when the goal is to categorize data points into discrete classes (e.g., spam vs. not spam).

- **Cross-Entropy Loss (Log Loss):** 
  - **What it is:** The most common loss function for classification models that output probability values between 0 and 1.
  - **Variants:** **Binary Cross-Entropy** for two classes, and **Categorical Cross-Entropy** for multi-class problems. See [[#3. Cross-Entropy in Depth]] below.
- **Hinge Loss:** 
  - **What it is:** Designed for "maximum margin" classification, primarily used with [[Support Vector Machines]] (SVMs).
  - **Pros/Cons:** Penalizes predictions that fall on the wrong side of the decision boundary or within the margin.
- **Kullback-Leibler (KL) Divergence:** 
  - **What it is:** Measures how one probability distribution differs from a reference probability distribution. Often used in specific neural network architectures.

## 3. Cross-Entropy in Depth

### The Intuition
Cross-entropy compares two probability distributions: the **true distribution** $p$ (the labels) and the **predicted distribution** $q$ (the model's output). It measures how many "nats" (or bits, with $\log_2$) of surprise the model experiences when the true outcome occurs.

$$H(p, q) = -\sum_{x} p(x)\,\log q(x)$$

- A confident, correct prediction gives a loss near **0**.
- A confident, wrong prediction gives a very large loss, since $-\log q \to \infty$ as $q \to 0$.
- It is tied to KL divergence: $H(p, q) = H(p) + D_{KL}(p \,\|\, q)$. Because the label entropy $H(p)$ is constant, minimizing cross-entropy is the same as minimizing KL divergence, which equals maximum likelihood estimation.

| Predicted probability of the true class | Loss $-\ln q$ | Reading             |
| --------------------------------------- | ------------- | ------------------- |
| 0.99                                    | 0.010         | Confident and right |
| 0.90                                    | 0.105         | Good                |
| 0.50                                    | 0.693         | Coin flip           |
| 0.10                                    | 2.303         | Bad                 |
| 0.01                                    | 4.605         | Confident and wrong |
|                                         |               |                     |

### Binary Cross-Entropy (BCE / Log Loss)
Used when there are **two classes** and the model outputs a single probability $\hat{y} = P(y=1)$, usually through a **sigmoid** $\sigma(z) = \frac{1}{1+e^{-z}}$.

$$L = -\big[\,y\,\ln(\hat{y}) + (1-y)\,\ln(1-\hat{y})\,\big]$$

Since $y$ is either 0 or 1, only one term is ever active:

$$L = \begin{cases} -\ln(\hat{y}) & \text{if } y = 1 \\ -\ln(1-\hat{y}) & \text{if } y = 0 \end{cases}$$

Averaged over a batch of $N$ samples:

$$J = -\frac{1}{N}\sum_{i=1}^{N}\big[\,y_i\ln(\hat{y}_i) + (1-y_i)\ln(1-\hat{y}_i)\,\big]$$

**Worked example (spam detection).** Three emails, label 1 = spam:

| Email | True $y$ | Predicted $\hat{y}$ | Loss |
|---|---|---|---|
| A | 1 | 0.9 | $-\ln 0.9 = 0.105$ |
| B | 0 | 0.2 | $-\ln 0.8 = 0.223$ |
| C | 1 | 0.6 | $-\ln 0.6 = 0.511$ |

Batch loss: $\frac{0.105 + 0.223 + 0.511}{3} \approx 0.280$. Email C is the least certain, so it contributes the most.

**Where it is used:** [[Logistic Regression]], binary classifiers (fraud, churn, disease present or absent), GAN discriminators, and **multi-label** classification, where each label gets its own sigmoid and its own BCE term (a movie can be both "comedy" and "romance").

### Categorical Cross-Entropy (Multi-Class)
Used when there are $C$ **mutually exclusive classes**. The model outputs raw scores (**logits**) $z$, which a **softmax** turns into a probability distribution:

$$\hat{y}_c = \text{softmax}(z)_c = \frac{e^{z_c}}{\sum_{j=1}^{C} e^{z_j}}$$

The label is a **one-hot** vector $y$ (1 for the true class, 0 elsewhere), so the sum collapses to a single term:

$$L = -\sum_{c=1}^{C} y_c \ln(\hat{y}_c) = -\ln(\hat{y}_{\text{true}})$$

Averaged over a batch:

$$J = -\frac{1}{N}\sum_{i=1}^{N}\sum_{c=1}^{C} y_{i,c}\ln(\hat{y}_{i,c})$$

**Worked example (image classification).** Classes: cat, dog, bird. The true class is **dog**, so $y = [0, 1, 0]$. The network outputs logits $z = [1.0,\ 2.0,\ 0.1]$.

1. Exponentiate: $[e^{1.0}, e^{2.0}, e^{0.1}] = [2.718,\ 7.389,\ 1.105]$, sum $= 11.212$
2. Softmax: $\hat{y} = [0.242,\ 0.659,\ 0.099]$
3. Loss: $L = -\ln(0.659) \approx 0.417$

Had the model instead predicted $[0.7,\ 0.2,\ 0.1]$ (confident in cat), the loss would be $-\ln(0.2) \approx 1.609$, nearly 4 times larger.

**Gradient:** softmax combined with cross-entropy has a very clean gradient with respect to the logits, $\frac{\partial L}{\partial z_c} = \hat{y}_c - y_c$. For the example above that is $[0.242,\ -0.341,\ 0.099]$: push the dog logit up and the others down. This is a big reason the pair is so common, and why gradients stay healthy even when predictions are badly wrong.

### Choosing the Right Variant

| Task | Output layer | Loss | Label format |
|---|---|---|---|
| Binary (spam or not) | 1 unit, sigmoid | Binary cross-entropy | 0 or 1 |
| Multi-class, one label per sample | $C$ units, softmax | Categorical cross-entropy | One-hot, e.g. `[0, 1, 0]` |
| Multi-class, integer labels | $C$ units, softmax | Sparse categorical cross-entropy | Class index, e.g. `1` |
| Multi-label (several can be true) | $C$ units, sigmoid each | Binary cross-entropy per class | Multi-hot, e.g. `[1, 0, 1]` |

*Sparse* categorical cross-entropy computes the same value as the one-hot version; it only saves memory by storing the class index.

### In Practice
- **Use logits, not probabilities, with the fused loss.** In PyTorch, `nn.CrossEntropyLoss` expects raw logits and applies log-softmax internally; `nn.BCEWithLogitsLoss` does the same for sigmoid. This is more numerically stable than computing softmax or sigmoid first and then taking the log.
- **Avoid $\log(0)$.** Libraries clip probabilities to a small epsilon, such as $10^{-7}$, when you pass in probabilities directly.
- **Class imbalance:** pass per-class weights (`weight=` or `pos_weight=` in PyTorch), or use focal loss, which down-weights easy examples.
- **Label smoothing:** replace the hard one-hot target with something like $[0.05,\ 0.9,\ 0.05]$ to reduce overconfidence.

```python
import torch, torch.nn as nn

# Multi-class: logits for (cat, dog, bird), true class = dog (index 1)
logits = torch.tensor([[1.0, 2.0, 0.1]])
target = torch.tensor([1])
print(nn.CrossEntropyLoss()(logits, target))   # tensor(0.4170)

# Binary: one logit per sample, target is 0.0 or 1.0
logit = torch.tensor([2.1972])                 # sigmoid -> 0.9
print(nn.BCEWithLogitsLoss()(logit, torch.tensor([1.0])))  # tensor(0.1054)
```

### References for Cross-Entropy
- Goodfellow, Bengio and Courville, [Deep Learning, Chapter 6: Deep Feedforward Networks](https://www.deeplearningbook.org/contents/mlp.html): cross-entropy as negative log-likelihood, and softmax output units.
- Wikipedia, [Cross-entropy](https://en.wikipedia.org/wiki/Cross-entropy): the identity $H(p,q) = H(p) + D_{KL}(p\|q)$, the link to maximum likelihood, and the logistic regression loss.
- Stanford CS231n, [Linear classification: Softmax classifier](https://cs231n.github.io/linear-classify/): softmax and cross-entropy walkthrough with numeric examples.
- PyTorch, [CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html): expects unnormalized logits; supports `weight` and `label_smoothing`.
- PyTorch, [BCEWithLogitsLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.BCEWithLogitsLoss.html): sigmoid and BCE fused for numerical stability; supports `pos_weight`.

## 4. Other Loss Functions Worth Knowing

The losses above handle plain regression and classification. Many tasks need a loss shaped to the problem: imbalanced classes, similarity rather than labels, sequences without alignment, or generative models.

| Loss                        | Used for                                      | Core idea                                                      |
| --------------------------- | --------------------------------------------- | -------------------------------------------------------------- |
| **Focal loss**              | Object detection with extreme class imbalance | Down-weight easy examples so hard ones dominate                |
| **Dice loss**               | Segmentation                                  | Optimize overlap directly, robust to small foreground          |
| **IoU / GIoU loss**         | Bounding-box regression                       | Optimize the box overlap, not coordinate distance              |
| **Quantile (pinball) loss** | Predicting a quantile or interval             | Asymmetric penalty for over- and under-prediction              |
| **Contrastive loss**        | Similarity learning with pairs                | Pull similar pairs together, push dissimilar apart by a margin |
| **Triplet loss**            | Embeddings (face recognition, retrieval)      | Anchor closer to positive than to negative by a margin         |
| **InfoNCE**                 | Self-supervised and multimodal learning       | Pick the true match out of many negatives                      |
| **Perceptual loss**         | Image generation and style transfer           | Compare deep features instead of pixels                        |
| **CTC loss**                | Speech and handwriting recognition            | Sum over all alignments of labels to input frames              |
| **Adversarial (GAN) loss**  | Generative models                             | A discriminator supplies the training signal                   |
| **ELBO / KL term**          | Variational autoencoders                      | Reconstruction plus a KL regularizer                           |

### Focal loss: ignore the easy examples

In a detector, a handful of positions contain objects and thousands are easy background. Plain cross-entropy gives every easy background position a small loss, but thousands of them add up and drown out the few hard cases. **Focal loss** (Lin et al., 2017) multiplies the cross-entropy by a factor that shrinks for well-classified examples:

$$\text{FL}(p_t) = -\alpha_t\,(1 - p_t)^{\gamma}\,\log p_t$$

Here $p_t$ is the probability the model gives to the **true** class, and $\gamma \ge 0$ controls the focus. With $\gamma = 2$, which is a typical setting:

| Model confidence in true class $p_t$ | Weight $(1 - p_t)^2$ | Effect |
| ------------------------------------ | -------------------- | ------ |
| 0.9 (easy) | 0.01 | Loss cut to 1% |
| 0.5 | 0.25 | Cut to 25% |
| 0.1 (hard) | 0.81 | Almost unchanged |

Setting $\gamma = 0$ recovers ordinary cross-entropy. The paper's point is that this removes most of the accuracy gap between one-stage and two-stage detectors.

### Dice and IoU losses: optimize overlap directly

For segmentation, the foreground (a tumor, a road) often covers a small share of the pixels, so an all-background prediction already scores well on pixel accuracy. The **Dice coefficient** measures overlap between prediction $P$ and ground truth $G$, and the loss is one minus it. Using probabilities $p_i$ and labels $g_i$ makes it differentiable:

$$\mathcal{L}_{\text{Dice}} = 1 - \frac{2\sum_i p_i g_i}{\sum_i p_i + \sum_i g_i}$$

It was used as the training objective in V-Net for volumetric medical segmentation, where foreground voxels are strongly outnumbered by background. For boxes, **IoU loss** is $1 - \text{IoU}$, and **GIoU** adds a penalty based on the smallest box enclosing both boxes, so it still gives a gradient when the boxes do not overlap.

### Quantile (pinball) loss: predicting a range

MSE and MAE predict the mean or median. To predict a **quantile** $\tau$ (for example the 90th percentile), penalize the two kinds of error differently:

$$L_\tau(y, \hat y) = \max\big(\tau\,(y - \hat y),\ (\tau - 1)\,(y - \hat y)\big)$$

At $\tau = 0.5$ this is half the absolute error, which gives the median. At $\tau = 0.9$ under-predicting costs 9 times as much as over-predicting, so the model learns an upper bound. Training two quantiles gives a prediction interval.

### Metric learning: contrastive, triplet and InfoNCE

Sometimes there are no class labels, only a notion of "similar". These losses train an **embedding** where distance means similarity ([[Word2Vec]] is an early example of the idea in NLP).

- **Contrastive loss** works on pairs with distance $D$ between their embeddings and $Y = 0$ for similar, $Y = 1$ for dissimilar:

$$L = (1 - Y)\,\tfrac12 D^2 + Y\,\tfrac12 \max(0,\ m - D)^2$$

Similar pairs are pulled together, and dissimilar pairs are pushed apart only until they are $m$ away (the **margin**).

- **Triplet loss** uses an **anchor** $a$, a **positive** $p$ (same identity) and a **negative** $n$ (different identity):

$$L = \max\big(0,\ d(a, p) - d(a, n) + m\big)$$

The anchor must be closer to the positive than to the negative by at least $m$, otherwise the loss is zero. FaceNet used it to learn a compact embedding where distance reflects face similarity (128 bytes per face), with online mining of informative triplets, since most random triplets are already satisfied and contribute nothing.

- **InfoNCE** (from contrastive predictive coding) treats the problem as classification: given a query $q$, pick its true partner $k^+$ out of $K$ candidates,

$$L = -\log \frac{\exp(\text{sim}(q, k^+)/\tau)}{\sum_{k=1}^{K} \exp(\text{sim}(q, k)/\tau)}$$

It is cross-entropy over similarities with a temperature $\tau$. Larger batches supply more negatives. Variants of this form train many self-supervised and image-text models.

### CTC: sequences without alignment

In speech or handwriting recognition the input has many more frames than the output has characters, and nobody labelled which frame belongs to which character. **Connectionist temporal classification (CTC)** adds a blank symbol and defines the loss as the negative log of the **total probability of all alignments** that collapse to the correct text (repeats merged, blanks removed). A dynamic-programming recursion computes the sum efficiently.

### Perceptual loss: compare features, not pixels

A pixel-wise MSE between two images punishes a tiny shift heavily and favours blurry outputs. A **perceptual loss** (Johnson et al., 2016) feeds both images through a pretrained network and compares their **feature maps**, so images that look alike to the network score as close. It is widely used in super-resolution and style transfer.

### Adversarial and variational losses

- **GAN loss:** a discriminator $D$ learns to tell real from generated samples, and the generator is trained to fool it, in the original formulation $\min_G \max_D\ \mathbb E[\log D(x)] + \mathbb E[\log(1 - D(G(z)))]$. The loss is a moving target set by the opponent ([[Generative Adversarial Networks]]). The **Wasserstein** variant replaces it with a distance between distributions that gives smoother gradients.
- **ELBO:** a variational autoencoder minimizes a **reconstruction loss** plus a **KL divergence** that keeps the latent distribution close to a prior ([[Variational Autoencoders]]). This is the KL divergence from section 2 used as a regularizer.

### Losses vs. training tricks

Some things that look like losses are really modifications: **label smoothing** (soften one-hot targets, for example 0.9 and 0.1 instead of 1 and 0), **class weights** (scale each class's loss), and **regularization** terms added to any loss ([[Regularization]]). Ranking tasks use pairwise or listwise losses ([[Learning To Rank]]).

### Sources for this section

- Lin et al., [Focal Loss for Dense Object Detection](https://arxiv.org/abs/1708.02002): the class-imbalance problem and the down-weighting of easy examples.
- Schroff, Kalenichenko and Philbin, [FaceNet](https://arxiv.org/abs/1503.03832): triplets of matching and non-matching face patches, online triplet mining, 128 bytes per face.
- van den Oord, Li and Vinyals, [Representation Learning with Contrastive Predictive Coding](https://arxiv.org/abs/1807.03748): a probabilistic contrastive loss with negative sampling (the abstract does not use the name InfoNCE, which comes from the paper's body).
- Milletari, Navab and Ahmadi, [V-Net](https://arxiv.org/abs/1606.04797): the Dice-coefficient objective for strongly imbalanced foreground and background.
- Formulas for quantile, contrastive, CTC, perceptual, GAN and ELBO losses, the focal-loss setting $\gamma = 2$, and the IoU and GIoU remarks are from my own knowledge and were not checked against the papers (Hadsell et al., 2006; Graves et al., 2006; Johnson et al., 2016; Goodfellow et al., 2014).

---
*Source: Synthesized from [BuiltIn](https://builtin.com/machine-learning/common-loss-functions), [DataCamp](https://www.datacamp.com), and [IBM](https://www.ibm.com) technical documentation.*
