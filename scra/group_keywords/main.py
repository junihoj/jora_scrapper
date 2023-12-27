import openai
openai_api_key = open('api_key.txt', 'r').read()
openai.api_key = openai_api_key
# openai.completions.create([])
# use_prompt = f"Company: {company}\nMeta: {meta_desc}\nDescription: {description}\n###\n"
# result = openai.Completion.create(
#                     model="curie:ft-punch-2021-12-08-10-46-24",
#                     prompt=use_prompt,
#                     temperature=0.37,
#                     max_tokens=100,
#                     top_p=1,
#                     frequency_penalty=2,
#                     presence_penalty=2,
#                     stop=["###", "\n", "END"])

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content":"What is the difference between celsius and fahrenheit"}
    ]
)

print(response)
# chat_log=[]

# while True:
    # user_message = input()
    # if user_message.lower() == 'quit':
    #     break
    # else:
    #     chat_log.append({"role":"user", "content":user_message})
    #     response = openai.chat.completions.create(
    #         model="gpt-3.5-turbo",
    #         messages=chat_log
    #     )

    #     assistant_response = response['choices'][0]['message']['content']
    #     print("CHATGPT:", assistant_response.strip("\n").strip())
    #     chat_log.append({"role":"assistant", "content":assistant_response.strip("\n").strip()})

    # response["choices"][0]["message"]["content"]