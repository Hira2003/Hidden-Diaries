from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
import torch

model_name = "nateraw/bert-base-uncased-emotion"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def detect_emotion(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)
        top_prob, top_idx = torch.max(probs, dim=1)
        label = model.config.id2label[top_idx.item()]
    return label, top_prob.item()
