# bias_detector.py
import torch
from transformers import AutoTokenizer

from services.bias_detection_module import CustomFinBERTClassifier

model_path = "/Users/nasaska/PycharmProjects/DisProject/services/finbert_bias_detector"

tokenizer = AutoTokenizer.from_pretrained(model_path)
base_model = "yiyanghkust/finbert-tone"

model = CustomFinBERTClassifier(base_model, num_labels=5)
model.load_state_dict(torch.load(f"{model_path}/pytorch_model.bin"))
model.eval()


# Load label classes
with open(f"{model_path}/label_classes.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]

def predict_bias(text: str) -> str:
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=64)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs["logits"]
        predicted_class = torch.argmax(logits, dim=1).item()
        return labels[predicted_class]