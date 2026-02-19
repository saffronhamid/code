# Phishing Detection Project — Interview Q&A (OSX)

Use this as a concise, spoken-answer guide. Replace bracketed placeholders with your actual choices.

## 1) Problem Understanding

**Can you briefly explain your phishing detection project?**
I built a phishing URL classifier that flags whether a URL is legitimate or malicious. It ingests URLs, extracts features (lexical, domain, and optional content/hosting signals), trains a supervised model, and outputs a probability so the system can tune the alert threshold for different risk levels.

**Why did you choose this problem?**
Phishing is a high‑impact, real‑world security issue with clear business consequences. It’s also a great ML problem because you can compare precision/recall trade‑offs and show how model decisions map to user risk.

**What was the main challenge?**
The biggest challenge was **class imbalance and evolving attacker behavior**. Legitimate URLs dominate, and attackers change tactics, so the model must generalize and be monitored over time.

---

## 2) Data & Features

**What features did you use and why?**
I used a mix of:
- **Lexical URL features**: length, number of dots, special characters, presence of “@”, “-”, or IP address in the hostname — strong signals for obfuscation.
- **Domain/host features**: domain age, registrar, DNS TTL, SSL certificate presence/age — reflects trust and stability.
- **Content features (optional)**: HTML form count, external links, login keywords — catches phishing pages that mimic brands.

**Was your dataset imbalanced?**
Yes. Legitimate URLs heavily outnumber phishing URLs.

**How did you handle imbalance?**
I combined:
- **Class weighting** in the model.
- **Threshold tuning** based on precision/recall needs.
- (Optional) **Resampling** like SMOTE or under‑sampling for robustness checks.

**How did you split train and test data?**
I used a **stratified split** (e.g., 80/20) to preserve class ratios, and I ensured no near‑duplicate URLs leaked across splits. If timestamps were available, I used a **time‑based split** to test real‑world drift.

---

## 3) Model & Reasoning

**Why did you choose Logistic Regression / Random Forest?**
- **Logistic Regression** is interpretable and fast, good for a baseline and feature importance.
- **Random Forest** handles non‑linear patterns and feature interactions without heavy feature engineering.

**What other models did you try?**
I compared with **Gradient Boosting / XGBoost**, **SVM**, and a simple **Naive Bayes** baseline to understand the trade‑offs between accuracy and interpretability.

**What metric did you use and why?**
I used **precision, recall, F1**, and **ROC‑AUC**. For phishing, **recall** matters because missing a phishing link is costly, but I also monitor precision to avoid alert fatigue.

**Why is accuracy not enough here?**
With imbalanced data, a model can be “accurate” by predicting everything as legitimate. Accuracy hides poor phishing detection performance.

**Did your model overfit? How did you check?**
I compared train vs. validation metrics, used cross‑validation, and monitored performance on a held‑out test set. Large train‑test gaps signaled overfitting.

---

## 4) Evaluation & Trade‑offs

**What is more dangerous: false positive or false negative in phishing detection?**
A **false negative** (missed phishing) is usually more dangerous because it exposes users to compromise. But too many false positives can reduce trust in the system, so I tuned thresholds based on deployment risk tolerance.

**How would you improve your system?**
- Add **fresh threat intel feeds** and domain reputation signals.
- Incorporate **content‑based features** or lightweight page rendering.
- Add **online monitoring** and retraining for drift.

**What are the limitations of your approach?**
- Reliance on static features can be evaded.
- Labels can be noisy or delayed.
- Model performance can degrade as attackers change tactics.

---

## 5) Bonus Depth

**Why use log‑loss instead of MSE?**
Log‑loss is designed for probabilistic classification and penalizes confident wrong predictions more than MSE. It aligns better with classification likelihoods.

**How would you deploy this in production?**
As a **REST service** or **batch scoring pipeline** with:
- Feature extraction service
- Model server (e.g., FastAPI + model artifact)
- Thresholding + alerting layer
- Monitoring for drift and latency

**How would you handle model drift?**
Track input feature distributions, alert on drift, collect feedback, and retrain on recent data. Use a shadow model to test updates safely.

**What happens if attackers change patterns?**
Performance drops; that’s why continuous monitoring and retraining with updated features is essential.

**If I give you 10 million URLs, will your system scale?**
Yes, with batch feature extraction, distributed processing (Spark or Ray), and incremental model updates. Feature computation is the main bottleneck, so parallelization is key.

---

## What They Are Testing (Quick Reminder)
- Clarity of explanation
- Trade‑off reasoning
- Real‑world impact awareness
- Justification of metrics and model choices
