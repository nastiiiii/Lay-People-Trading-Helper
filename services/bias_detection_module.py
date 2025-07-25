import pandas as pd
import torch
from sklearn.preprocessing import LabelEncoder
from torch.utils.data import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer, BertConfig, BertModel
)

# === Step 1: Load CSV and encode labels ===
df = pd.read_csv("/Users/nasaska/PycharmProjects/DisProject/utils/bias_detection_dataset.csv")
label_encoder = LabelEncoder()
df["label_encoded"] = label_encoder.fit_transform(df["label"])

# === Step 2: Tokenize text ===
tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
tokens = tokenizer(
    list(df["text"]),
    padding=True,
    truncation=True,
    max_length=64,
    return_tensors="pt"
)

# === Step 3: Create a PyTorch Dataset ===
class BiasDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        return {
            key: val[idx] for key, val in self.encodings.items()
        } | {"labels": torch.tensor(self.labels[idx])}

    def __len__(self):
        return len(self.labels)

dataset = BiasDataset(tokens, df["label_encoded"].tolist())

# === Step 4: Load model and set training arguments ===
config = BertConfig.from_pretrained("yiyanghkust/finbert-tone", num_labels=len(label_encoder.classes_))
model = AutoModelForSequenceClassification.from_config(config)
model.bert = BertModel.from_pretrained("yiyanghkust/finbert-tone")

training_args = TrainingArguments(
    output_dir="./finbert_bias_detector",
    evaluation_strategy="epoch",
    per_device_train_batch_size=8,
    num_train_epochs=4,
    save_strategy="epoch",
    logging_dir="./logs",
    logging_steps=10,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer,
)

# === Step 5: Train and Save ===
trainer.train()
trainer.save_model("./finbert_bias_detector")
tokenizer.save_pretrained("./finbert_bias_detector")

# Save the label encoder classes
with open("./finbert_bias_detector/label_classes.txt", "w") as f:
    for label in label_encoder.classes_:
        f.write(label + "\n")
