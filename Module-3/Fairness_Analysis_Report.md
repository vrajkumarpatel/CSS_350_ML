# Short Report: Bias Analysis and Mitigation in Adult Income Dataset

## Introduction
This report details the analysis of bias in the UCI Adult Income Dataset using logistic regression. The dataset includes demographic features like age, gender, race, and education to predict income (>50K or <=50K). The analysis follows the assignment steps: exploration, preprocessing, model training, fairness metrics calculation, mitigation via reweighting, and re-evaluation.

## Data Exploration and Bias Identification
The dataset has 32,561 samples with features such as age (mean ~38), gender (67% male), race (86% White), and income (24% >50K). Distributions reveal potential biases:
- Gender: Males have 31% >50K vs. 11% for females, indicating gender pay gap.
- Race: White 26% >50K, Black 12%, Asian-Pac-Islander 32%, but minorities underrepresented.
- Age: Higher income for mid-age groups (30-50 years).
Sources of bias: historical inequalities in wages, education, and occupation embedded in data.

## Model Training and Baseline Performance
Categorical features were one-hot encoded, sex/income binarized, no explicit missing values. Dataset split 70/30. Logistic regression trained, achieving ~80% accuracy on test set. Confusion matrix shows 92% TN rate but lower TP for positive class.

## Fairness Metrics Calculation
Using AIF360:
- Demographic Parity (DP): Difference in positive prediction rates (males - females) = -0.20, indicating males favored.
- Equalized Odds (EO): TPR difference 0.05, FPR 0.07; females have lower TP rates.
Observed biases: Model perpetuates gender/racial disparities; e.g., higher false negatives for minorities, leading to unfair income prediction.

## Bias Mitigation
Applied reweighting on gender (unprivileged: female=0, privileged: male=1). Retrained model on weighted data.

## Re-evaluation
- Accuracy: Stable at ~80% (change 0.00).
- DP: Improved to 0.00.
- Disparate Impact: From 0.36 to 1.00.
- EO: TPR/FPR differences reduced slightly, but trade-off noted.
Mitigation effective for parity without accuracy loss, improving fairness for gender groups.

## Findings and Trade-offs
Initial model shows strong gender bias (DP violation 0.20), racial bias (varying prediction rates). Reweighing eliminates DP difference, achieving disparate impact=1, confirming effectiveness in balancing groups. Trade-offs: Minimal accuracy impact, but EO shows minor worsening in TPR for males; overall, fairness gains outweigh costs. Recommendation: Use reweighting for demographic parity in similar tasks, monitor multiple metrics.

Word count: ~350
