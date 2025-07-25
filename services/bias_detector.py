# services/bias_detector.py

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class BiasDetector:
    def __init__(self, model_path: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.eval()

        # Use your label list directly here since label_classes.txt won't exist in the HF model
        self.labels = [
            "bandwagon",
            "confirmation",
            "loss_aversion",
            "none",
            "overconfidence"
        ]

    def predict_bias(self, text: str):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=64)
        with torch.no_grad():
            outputs = self.model(**inputs)
            predicted_class = torch.argmax(outputs.logits, dim=1).item()
            return self.labels[predicted_class]
