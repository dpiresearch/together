# Define the path to your file
file_path = 'data/promptcode.txt'
prompt_path = 'data/prompt.txt'

# Open the file and read its contents
with open(file_path, 'r') as file:
    file_contents = file.read()

# file_contents now holds the contents of the file as a string
# print(file_contents)

# Open the prompt file and read its contents
with open(prompt_path, 'r') as file:
    prompt = file.read()

# prompt="A step labeled gpt and a step labeled deepgram"
print(prompt)

import openai
import os

client = openai.OpenAI(
  api_key=os.environ.get("TOGETHER_API_KEY"),
  base_url='https://api.together.xyz',
)

chat_completion = client.chat.completions.create(
  messages=[
    {
      "role": "system",
      "content": file_contents,
    },
    {
      "role": "user",
      "content": prompt,
    }
  ],
  model="mistralai/Mixtral-8x7B-Instruct-v0.1",
  # model="togethercomputer/Qwen-7B-Chat",
  # model="dfmaptool@gmail.com/Mistral-7B-Instruct-v0.1-my-demo-finetune-2024-01-13-07-41-37",
  max_tokens=10000
)

print(chat_completion.choices[0].message.content)

