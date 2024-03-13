#!/usr/bin/env python3
# A collection of functions useful in multiple notebooks

from sklearn.metrics import make_scorer, confusion_matrix
import pandas as pd

# Visualizations
def vis_meta_cellcount_stacked_bar(adata, meta_col, dict_colors):
    cellcounts = pd.DataFrame(adata.obs.groupby('sample_ids_letter')[meta_col].value_counts())
    cellcounts_wide = cellcounts.pivot_table(index='sample_ids_letter', columns=meta_col, values='count')

    cellcounts_wide_colors = [dict_colors[key] for key in cellcounts_wide.columns]

    cellcounts_wide.plot(kind='bar', stacked=True, color=cellcounts_wide_colors) 


# Measurements of classifier assessments used in feature seelction etc
def specificity(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return tn / (tn + fp)

def false_positive_rate(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return fp / (tn + fp)

def false_negative_rate(y_true, y_pred): # AKA recall
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return fn / (fn + tp)

def precision(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return tp / (tp + fp)