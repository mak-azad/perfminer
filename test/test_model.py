import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load the tokenizer and model only once, outside the function
tokenizer = AutoTokenizer.from_pretrained("ManojAlexender/Finetuned_Final_LM_200k")
model = AutoModelForSequenceClassification.from_pretrained("ManojAlexender/Finetuned_Final_LM_200k")

def get_prediction(input_text):
    # Tokenize the input text
    inputs = tokenizer(input_text, return_tensors="pt",truncation=True, max_length=512)

    # Perform inference without computing gradients for efficiency
    with torch.no_grad():
        logits = model(**inputs).logits

    # Get the predicted class ID
    predicted_class_id = logits.argmax().item()

    # Retrieve the label from the model's config
    predicted_label = model.config.id2label[predicted_class_id]

    return predicted_label

# Example usage
input_text = "this is not causing a performance problem"
predicted_label = get_prediction(input_text)
print(predicted_label)
