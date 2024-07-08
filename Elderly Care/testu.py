from transformers import GPT2LMHeadModel, GPT2Tokenizer

model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name, max_length=100, padding=True)

print("GPT-2 ChatBot: Hello! I'm here to help. Type 'exit' to end the conversation.")

while True:
    user_input = input("You: ")

    if user_input.lower() == 'exit':
        print("GPT-2 ChatBot: Goodbye!")
        break


    input_ids = tokenizer.encode(user_input, return_tensors="pt", max_length=100, truncation=True)
    attention_mask = input_ids.clone().detach()
    attention_mask[:, :] = 1  
    attention_mask[input_ids == tokenizer.pad_token_id] = 0  


    output = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_length=100,
        num_beams=5,
        no_repeat_ngram_size=2,
        top_k=50,
        top_p=0.95,
        temperature=0.1,
        do_sample=True
    )


    response = tokenizer.decode(output[0], skip_special_tokens=True)
    if "http" not in response:
        print("GPT-2 ChatBot:", response)
    else:
        print("GPT-2 ChatBot: I'm sorry, I don't have information on that topic.")
