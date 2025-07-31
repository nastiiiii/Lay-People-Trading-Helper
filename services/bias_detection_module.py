import pandas as pd
import torch
import torch.nn as nn
from transformers import TrainingArguments, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from torch.utils.data import Dataset
from transformers import (
    AutoTokenizer,
    BertModel,
    Trainer
)

# Load CSV and encode labels
df = pd.read_csv("/Users/nasaska/PycharmProjects/DisProject/utils/synthetic_bias_detection_dataset.csv")
label_encoder = LabelEncoder()
df["label_encoded"] = label_encoder.fit_transform(df["label"])

#Tokenize and split
tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df["text"].tolist(),
    df["label_encoded"].tolist(),
    test_size=0.2,
    stratify=df["label_encoded"],
    random_state=42
)

train_encodings = tokenizer(train_texts, padding=True, truncation=True, max_length=64, return_tensors="pt")
val_encodings = tokenizer(val_texts, padding=True, truncation=True, max_length=64, return_tensors="pt")

#Create a PyTorch Dataset
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

train_dataset = BiasDataset(train_encodings, train_labels)
val_dataset = BiasDataset(val_encodings, val_labels)

# Custom model with correct classifier head
class CustomFinBERTClassifier(nn.Module):
    def __init__(self, model_name, num_labels):
        super().__init__()
        self.bert = BertModel.from_pretrained(model_name)
        self.dropout = nn.Dropout(0.1)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_labels)

    def forward(self, input_ids=None, attention_mask=None, token_type_ids=None, labels=None):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        pooled_output = outputs.pooler_output
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)
        loss = None
        if labels is not None:
            loss_fn = nn.CrossEntropyLoss()
            loss = loss_fn(logits, labels)
        return {"loss": loss, "logits": logits} if loss is not None else {"logits": logits}

# Load model
num_labels = len(label_encoder.classes_)
model = CustomFinBERTClassifier("yiyanghkust/finbert-tone", num_labels=num_labels)

#Training arguments
training_args = TrainingArguments(
    output_dir="./finbert_bias_detector",
    eval_strategy="epoch",
    per_device_train_batch_size=8,
    num_train_epochs=4,
    save_strategy="epoch",
    logging_dir="./logs",
    logging_steps=10,
)

#  Metrics
def compute_metrics(p):
    preds = p.predictions.argmax(axis=1)
    labels = p.label_ids
    return {
        "accuracy": accuracy_score(labels, preds),
        "f1": f1_score(labels, preds, average="weighted")
    }

#Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

# Train and save

trainer.train()
trainer.save_model("./finbert_bias_detector")
tokenizer.save_pretrained("./finbert_bias_detector")

torch.save(model.state_dict(), "./finbert_bias_detector/pytorch_model.bin")

tokenizer.save_pretrained("./finbert_bias_detector")

# Save the label encoder classes
with open("./finbert_bias_detector/label_classes.txt", "w") as f:
    for label in label_encoder.classes_:
        f.write(label + "\n")
