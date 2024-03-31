from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os

def convert_documentation(input_contents, openai_api_key, source_language, target_language):
    # set client
    client = OpenAI(api_key=openai_api_key)

    # Define conversion prompt
    prompt = f"Translate the following {source_language.capitalize()} documentation in markdown format to {target_language.capitalize()}. Converted documentation should also be in markdown format :\n\n{input_contents}\n\nConverted {target_language.capitalize()} documentation:"
    print("Prompt:")
    print(prompt)
    print("="*100)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )

    # Extract and return converted documentation
    converted_documentation = chat_completion.choices[0].message.content.strip()
    return converted_documentation


# add openai_api_key to environment variables
# While you can provide an api_key keyword argument, using python-dotenv may be preferred so that your API Key is not stored in source control
# steps - create .env file and add api key as OPENAI_API_KEY="My API Key"
_ = load_dotenv(find_dotenv()) # finds .env file and adds key-value pairs specified in .env to enviornment variables
openai_api_key   = os.environ.get("OPENAI_API_KEY") 
#print("openai_api_key: ", openai_api_key)
if (openai_api_key is None) :
    print('OpenAI API key not found. Please check .env file exists with key "OPENAI_API_KEY" present in file')
    exit()
if (len(openai_api_key.strip()) == 0) :
    print('Missing OpenAI API key - please provide api key value in .env file as OPENAI_API_KEY="My API Key"')
    exit()

# Specify different params below
source_language  = "python"
target_language  = "java"
input_file_path  = "./samples/python_to_others/input_python_doc.md"
output_file_path = "./samples/python_to_others/output_{}_doc.md".format(target_language) # new file will be created or existing file will be overwritten

# Read input file
with open(input_file_path, "r", encoding="utf-8") as file:
    input_contents = file.read()

# convert documentation
converted_documentation = convert_documentation(input_contents, openai_api_key, source_language, target_language)    
print("Completion result")
print(converted_documentation)

# Write output to file
with open(output_file_path, "w", encoding="utf-8") as file:
    file.write(converted_documentation)
print(f"Conversion complete. Output saved to {output_file_path}.")
