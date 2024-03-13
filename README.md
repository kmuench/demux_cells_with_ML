# demux_cells_with_ML
<<<<<<< HEAD
Applying machine learning to demultiplex scRNA-Seq data and gain insights into developmental neurobiology
=======
Demultiplexing single cell RNA-Seq data using data science + biology

Problem:
- In order to improve statistical power to detect differences between conditions, I need to maximize the number of samples I can run, given a fixed budget. The bottleneck for sample cost was the cost of the 10X chip, so I wanted to know: can I multiplex samples on a single chip using their gene expression signatures?


How can this be used?
- Demultiplexing to reduce the per-sample cost of 10x experiments. Others may be able to use this method to also increase the N of their sequencing experiment.
    - To facilitate the above, generation of a web tool where users can input cell profile and a sex is predicted
- Investigation of programs of gene expression that assist in M vs. F sample identification
- Improve representation of female mice in data collection, since there is a bias towards collecting data from male samples ( [Mamlouk 2020](https://www.sciencedirect.com/science/article/pii/S0091302220300261?casa_token=J99EnQaWI4EAAAAA:1guIwA5Xa77U4x1vCOiRe7FB3g-9impuCdwXoWkekqcmvbKXTv3dLQz3RKjK3_i8mfcalNEr_Q) ), [Plevkova 2020](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8603716/) )



# # 

# Description of Project

## Introduction
In this project, I will demonstrate that transcriptomic profiles can be used to distinguish male and female cells in scRNA-Seq. I will show that single-gene thresholding works remarkably well for identifying female cells, but that machine learning methods can be used to further improve cell sex classification.

This project was born of a budgetary constraint I faced in grad school. In order to improve statistical power to detect differences between conditions, I need to maximize the number of samples I could run. However, I was in the sad and common situation of designing a biology experiment with a very tight budget. The biggest contribution to the pricetag was the cost of the 10X chip, which at that time could run 8 samples and collect about 10,000 cells per sample. There were plenty of situations when I would much rather run double the number of samples and collect fewer cells.

I wanted to know: can I multiplex samples on a single chip using their gene expression signatures?

Although (at the time) a few multiplexing kits for scRNA-Seq existed, these added further costs; they were time-intensive to troubleshoot; and they added further steps to a protocol that I already worried was stressful to the delicate brain cells of my sample. However, I wondered: could we use inherent, well-characterized differences in cell expression to distinguish male from female cells? It is known that sex genes are differentially expressed during brain development ( [Shi 2016](https://www.nature.com/articles/srep21181) ) - would any of these be expressed in the early developing mouse brain in sufficient abundance for scRNA-Seq to detect it, and reliably enough to tell a male from a female cell? If all cells in the developing brain showed differential sex gene expression, we could run female and male samples together on the same chip and demultiplex them later.

There are many good reasons why sex gene expression might be a positive solution for the demultiplexing problem:
- **Reducing the costs of scRNA-Seq experiments** and/or increasing the N of a sequencing experiment
- **Reducing the need for additional protocols**, which could be expensive or stressful to the cells
- **Highlight specific features that contribute to male vs. female brain development** in the early developing brain;
- **Encourage the inclusion of both male and female samples** in neuroscience research, which traditionally has been biased towards collecting data from male samples or fails to report sample sex, despite the potential ramifications for human health research ( [Mamlouk 2020](https://www.sciencedirect.com/science/article/pii/S0091302220300261?casa_token=J99EnQaWI4EAAAAA:1guIwA5Xa77U4x1vCOiRe7FB3g-9impuCdwXoWkekqcmvbKXTv3dLQz3RKjK3_i8mfcalNEr_Q) ), [Plevkova 2020](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8603716/) ).

## Data collection
I designed an experiment to collect cells that were either from male or female mice, at day E13.5 in brain development. The sex of the mice was confirmed by PCR, and these samples were sequenced separately. I also pooled some known male/female samples to further study how classification might look in cells from a pooled sample.

## Approach

I discovered that categorizing cells as female based on raw expression of Xist > 1 was already very successful (~90% accurate), albeit not perfect - many female cells did not express Xist, and a small minority of male cells (likely erroneously) had associated Xist reads. I can imagine situations in which that would be an unacceptably large margin of error in a demultiplexing experiment. Therefore, I decided to try and engineer a model that could perform binary classification to categorize murine neural cells as male or female on the basis of their scRNA-Seq profile.

**Initial Performance Goal**:
- Ideally, auROC = 1 (perfect ability to distinguish); depending on cell population studied, perhaps <5% of cells being mislabeled is acceptable
- Benchmark: should see Xist (X-linked) high in female and Ddx3y (Y-linked high in male)
- Generalizability to other datasets (or other cell types)

**Desires for Model**:
- Interpretability, so that I can extract clues about which individual genes drive the classification
- Not too many features (to maximize the chance that it won't overfit/will generalize to other datasets; and also because I am working with a relatively small corpus of confidently labeled training data, ~10,000 cells)

My approach was as follows:
- Clean+filter the data according to best principles for scRNA-Seq (e.g. removing cells that seemed spurious)
- Label the cells
- Create test/training set, sampling in a cell classification-aware way (in case some cell types are more heavily sex gene-biased, so that these will not drive the classification)
- Identify possible subsets of relevant features using univariate feature selection methods
- Use five-fold cross-validation-based grid search/randomized search to identify an appropriate models from a list of candidates
- After hyperparameter tuning and comparing performance, pick a set of optimal models whose performance can be compared to Xist-based thresholding and applied to new datasets to study generalizability

## Limitations**
It was not possible to collect a dataset that perfectly balanced all features (eg., order of sample extraction, perfectly balancing). An attempt were made to balance for the largest possible confounding factors, e.g. two brains in male and female alike came from LPS-exposed pregnancies. Nevertheless, it is difficult to judge to what extent a failure of these results to generalize might be due to the fact that some of these gene signatures may be produced by the interaction of sex and other factors, e.g. LPS exposure.

## Conclusions**
After a biologically-grounded model exploration process, I used a regularized logistic regression and features identified using a K-best/false positive rate-controlling strategy, I was able to achieve 97% accuracy in identifying male and female cells. 

The feature set selected was also interesting. Not all of these genes were related to sex chromosomes or sexual differentiation in mice, suggesting that complex networks of gene regulation may already be at play in a manner that distinguishes male from female cells.

My hope is that this method demonstrates the possibility of discovering novel gene signatures that inspire both biological hypotheses and solve practical problems related to optimizing experiment design given resource constraints.

## Additional Notes**
- This experiment was originally designed not only to facilitate the above study but to study the effects of a genotype on brain development. Since this dataset has not yet been published, I have de-identified some features of the dataset (specifically, genetic variant of the mouse) out of respect for my scientific colleagues who might want to publish this work.
- I did not attempt to remove doublets as it is hard to tell the difference between these and cells that legitimately represent cells that are mitosing, and possibly cells which are mitotic yet in the process of assuming a new cortical layer identity
- I wish to draw a distinction in this work between sex (the structural, functional, and behavioral characteristics of living things determined by sex chromosome), as opposed to gender (an identity) ([Torgrimson and Minson 2005](https://journals.physiology.org/doi/full/10.1152/japplphysiol.00376.2005)). It is not correct or rigorous to interpret this work as evidence for the prenatal determination of a chromosome-dependent gender identity.

# TODO: Coming soon
- Model performance
    - Explore feature transformations (trading interpretability for better abstractability/classification)
    - Apply feature engineering techniques that take into account matrix sparsity, or cell identity for example (e.g., will a classifier improve if it knows it is looking at a glutamatergic neuron?)
    - Robustness/Sensitivity analysis - how are downstream interpretations impacted when 10% of the cells are misclassified vs. 1?
- Interpretation of feature set
    - How highly expressed are the features with the highest weights? Are there genes that are rarely expressed but, when they do, count for a lot?
- Validation
    - Benchmarking against other datasets - murine neural cells or other, as long as it includes metadata indicating sex
- Niceities
    - Pipeline for classifying sets of cells
    - Dash visualization of the starting data, to better visualize the cell identities and backgrounds in the training data.
