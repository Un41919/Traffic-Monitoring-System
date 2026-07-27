"""
=========================================
Model Evaluation
Traffic-Monitoring-System
Version : 2.1.0
=========================================
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

from settings import (
    MODEL_NAME,
    DATA_FOLDER,
    OUTPUT_FOLDER,
    CSV_FILENAME
)

# ==================================================
# Path
# ==================================================

csv_path = os.path.join(DATA_FOLDER, CSV_FILENAME)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Jika CSV memakai koma, ubah sep=";" menjadi sep=","
df = pd.read_csv(csv_path, sep=";")

print("=" * 50)
print("Evaluation Dataset")
print("=" * 50)
print(df.head())
print(f"\nTotal Data : {len(df)}")

# ==================================================
# Labels
# ==================================================

y_true = df["actual_class"]
y_pred = df["predicted_class"]

# ==================================================
# Metrics
# ==================================================

accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, average="weighted", zero_division=0)
recall = recall_score(y_true, y_pred, average="weighted", zero_division=0)
f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)

print("\n" + "=" * 50)
print("Overall Metrics")
print("=" * 50)
print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

# ==================================================
# Classification Report
# ==================================================

report = classification_report(y_true, y_pred, zero_division=0)

report_path = os.path.join(OUTPUT_FOLDER, "classification_report.txt")

with open(report_path, "w", encoding="utf-8") as file:
    file.write(f"Model : {MODEL_NAME}\n")
    file.write(f"Total Samples : {len(df)}\n\n")
    file.write(f"Accuracy  : {accuracy:.4f}\n")
    file.write(f"Precision : {precision:.4f}\n")
    file.write(f"Recall    : {recall:.4f}\n")
    file.write(f"F1 Score  : {f1:.4f}\n\n")
    file.write(report)

# ==================================================
# Metrics CSV
# ==================================================

metrics = pd.DataFrame({
    "Metric": ["Accuracy", "Precision", "Recall", "F1 Score"],
    "Value": [accuracy, precision, recall, f1]
})

metrics.to_csv(
    os.path.join(OUTPUT_FOLDER, "metrics.csv"),
    index=False
)

# ==================================================
# Confusion Matrix
# ==================================================

labels = sorted(df["actual_class"].unique())

cm = confusion_matrix(y_true, y_pred, labels=labels)

fig, ax = plt.subplots(figsize=(8, 8))

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=labels
)

disp.plot(
    ax=ax,
    cmap="Blues",
    colorbar=False,
    values_format="d"
)

plt.title(f"Confusion Matrix ({MODEL_NAME})")
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_FOLDER, "confusion_matrix.png"),
    dpi=300
)

plt.close()

# ==================================================
# Normalized Confusion Matrix
# ==================================================

cm_norm = confusion_matrix(
    y_true,
    y_pred,
    labels=labels,
    normalize="true"
)

fig, ax = plt.subplots(figsize=(8, 8))

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm_norm,
    display_labels=labels
)

disp.plot(
    ax=ax,
    cmap="Blues",
    colorbar=False,
    values_format=".2f"
)

plt.title(f"Normalized Confusion Matrix ({MODEL_NAME})")
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_FOLDER,
        "confusion_matrix_normalized.png"
    ),
    dpi=300
)

plt.close()

# ==================================================
# Summary
# ==================================================

summary = f"""# Model Evaluation Summary

Model : {MODEL_NAME}

Total Samples : {len(df)}

Accuracy : {accuracy:.4f}
Precision : {precision:.4f}
Recall : {recall:.4f}
F1 Score : {f1:.4f}

Ground Truth Distribution

{df['actual_class'].value_counts().to_string()}

Predicted Distribution

{df['predicted_class'].value_counts().to_string()}
"""

with open(
    os.path.join(OUTPUT_FOLDER, "evaluation_summary.md"),
    "w",
    encoding="utf-8"
) as file:
    file.write(summary)

print("\n" + "=" * 50)
print("Classification Report")
print("=" * 50)
print(report)

print("\nEvaluation completed successfully.")
