
def generate_legal_notice(input_message):
    from transformers import pipeline, set_seed
    generator = pipeline('text-generation', model='./Models//gpt2')
    set_seed(42)
    return (generator(input_message, max_length=500, num_return_sequences=5)[0]["generated_text"])
    # return generator
    
# if __name__ == "__main__":
#     input_message = "I am a text generative model.."

#     print(generate_legal_notice(input_message))
