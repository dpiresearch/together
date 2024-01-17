#
# This program takes an image of a workflow, generates a text description
# and attempts to generate a python program that implements the workflow.
#

import base64
import requests
import os
import openai
import re


# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
# image_path = "/Users/dpang/Downloads/flask.jpg"
image_path = "/Users/dpang/dev/togetherai/data/flow.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

#
# Make the call to Openai to get a summary of the image
#
payload = {
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Summarize the workflow in the image in the following way in less than 50 words: A step labeled ? followed. by a step labeled ? where the question mark is filled by the text detected in the boxes"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

prompt = response.json()['choices'][0]['message']['content']
print("OpenAI results: " + prompt)

# Define the path to your file
file_path = 'data/promptcode.txt' # This file holds instructions for the LLM to generate code
prompt_path = 'data/prompt.txt'   # This file is an example prompt for testing.  Represents the output/summary from the vision model

# Open the file and read its contents
with open(file_path, 'r') as file:
    file_contents = file.read()

# file_contents now holds the contents of the file as a string
# print(file_contents)

# Open the prompt file and read its contents
# with open(prompt_path, 'r') as file:
#     prompt = file.read()

print("Input: " + prompt)

client = openai.OpenAI(
  api_key=os.environ.get("TOGETHER_API_KEY"),
  base_url='https://api.together.xyz',
)

#
# START Diagnostic information
#
def count_words(string):
    # Split the string into words
    words = string.split()

    # Count the number of words
    return len(words)

# Example usage
example_string = "Hello, this is an example string."
word_count = count_words(example_string)
print("Number of words:", word_count)

# print("system: "+count_words(file_contents)

print(f"system: {file_contents}")
print(f"user: {prompt}")
#
# END Diagnostic information
#

#
# Call the LLM to generate code
#
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
  max_tokens=20000
)

answer=chat_completion.choices[0].message.content
print("====START ANSWER====")
print(answer)
print("====END ANSWER====")

# print(chat_completion)

def extract_text_between_backticks(text):
    # Regular expression pattern to match text between triple backticks
    pattern = r'```(.*?)```'

    # Find all matches in the text
    matches = re.findall(pattern, text, re.DOTALL)

    return matches

extracted_text = extract_text_between_backticks(answer)

# File path where you want to write the strings
file_path = "code_output.py"

# Open the file in write mode
with open(file_path, 'w') as file:
    # Iterate over the list and write each string to the file
    for etext in extracted_text:
        file.write(etext + '\n')  # Add a newline character after each string

for etext in extracted_text:
    print("====")
    print(etext)
    print("====")
# print("========Extracted text:", extracted_text)
