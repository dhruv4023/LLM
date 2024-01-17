from transformers import pipeline

def generate_notice(input_text):
    generator =  pipeline("text-generation", model="pszemraj/opt-350m-email-generation")  # Adjust model and device as needed

    notice = generator(input_text, max_length=500, num_return_sequences=1, temperature=0.7)[0]['generated_text']
    return notice

if __name__ == "__main__":
    # Replace 'your_input_text' with your actual input text
    input_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."

    generated_notice = generate_notice(input_text)
    print("Original Text:")
    print(input_text)
    print("\nGenerated Notice:")
    print(generated_notice)
