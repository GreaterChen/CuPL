from openai import OpenAI
import json
from tqdm import tqdm
import os

os.environ["http_proxy"] = "http://localhost:7890"
os.environ["https_proxy"] = "http://localhost:7890"
client = OpenAI(api_key="",
                base_url="https://api.chatanywhere.tech/v1")

json_name = "result.json"

category_list = ["oligodendroglioma", "astrocytoma", "glioblastoma"]
all_responses = {}
vowel_list = ['A', 'E', 'I', 'O', 'U']

for category in tqdm(category_list):

    if category[0].upper() in vowel_list:
        article = "an"
    else:
        article = "a"

    prompts = []
    prompts.append("How can you identify " + article + " " + category + "?")
    prompts.append("A caption of a FMRI image of " + article + " " + category + ":")
    prompts.append("Describe the significant features of " + article + " " + category + " in an FMRI scan.")
    prompts.append("What are the characteristic imaging findings of " + article + " " + category + "?")
    prompts.append("How does " + article + " " + category + " appear on an MRI scan?")
    prompts.append("What are the key distinguishing features of " + article + " " + category + " in medical imaging?")
    prompts.append("Describe the MRI characteristics that are typical for " + article + " " + category + ".")
    prompts.append("What unique features should be looked for in an MRI when diagnosing " + article + " " + category + "?")
    prompts.append("Explain the typical appearance of " + article + " " + category + " on a T1-weighted MRI scan.")
    prompts.append("Explain the typical appearance of " + article + " " + category + " on a T2-weighted MRI scan.")
    prompts.append("What is the typical risk level associated with " + article + " " + category + "?")
    prompts.append("Describe the survival rate for patients diagnosed with " + article + " " + category + ".")
    prompts.append("What is the median survival time for patients diagnosed with " + article + " " + category + "?")

    all_result = []
    for curr_prompt in tqdm(prompts):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.99,
            stop='.',
            n=10,
            max_tokens=50,
            messages=[
                {"role": "system", "content": "I need you to generate a short and accurate description of the object I want to identify"},
                {"role": "user", "content": curr_prompt},
            ]
        )

        for choice in response.choices:
            result = choice.message.content
            all_result.append(result.replace("\n\n", "") + ".")

    all_responses[category] = all_result

with open(json_name, 'w') as f:
    json.dump(all_responses, f, indent=4)
