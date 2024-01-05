
def generate_legal_notice(input_message):
    from transformers import pipeline, set_seed
    generator = pipeline('text-generation', model='./Models//gpt2')
    set_seed(42)
    # print("generator ready...")
    return (generator(input_message, max_length=500, num_return_sequences=5)[0]["generated_text"])
    # return generator
# generator= generate_legal_notice()
# while(True):
    
if __name__ == "__main__":
    input_message = "Section 147 of the Indian Penal Code defines rioting as an offence where five or more persons are gathered together to commit an unlawful act or a lawful act by means of unlawful means. The punishment for rioting is provided under Section 148 of the Indian Penal Code, which states that whoever is guilty of rioting shall be punished with imprisonment of either description for a term which may extend to two years, or with fine, or"

    print(generate_legal_notice(input_message))
