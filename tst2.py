from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# Load the tokenizer and model
model_name = "./Models//distilbart-cnn-12-6"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Create a summarization pipeline
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

# Example text to summarize
text_to_summarize = """
The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct.

"""

# Generate a summary
summary = summarizer(text_to_summarize, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)

# Print the summary
print(summary[0]['summary_text'])
