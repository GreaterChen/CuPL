from openai import OpenAI
import json
from tqdm import tqdm
import os

os.environ["http_proxy"] = "http://localhost:7890"
os.environ["https_proxy"] = "http://localhost:7890"
client = OpenAI(api_key="sk-KxibEeHJ32gk7ZlpMHiTNmF3Iqn2YWSYAnXVd0Zzqt3L0dK1",
                base_url="https://api.chatanywhere.tech/v1")

json_name = "adni_AD_prompt_result.json"

category_list = ["NC", "MCI", "AD"]
all_responses = {}
vowel_list = ['A', 'E', 'I', 'O', 'U']

for category in ["AD"]:
    if category[0].upper() in vowel_list:
        article = "an"
    else:
        article = "a"

    prompts = []
    prompts.append("Describe the significant MRI features of " + category + ".")
    prompts.append("What are the characteristic MRI findings of " + category + "?")
    prompts.append("How does " + category + " manifest in MRI scans?")
    prompts.append("What are the key MRI markers for diagnosing " + category + "?")
    prompts.append("Describe the MRI characteristics that are typical for " + category + ".")
    prompts.append("What unique MRI features should be looked for when diagnosing " + category + "?")
    prompts.append("What are the stages or severity levels of " + category + "?")
    # prompts.append("Discuss the progression of " + category + " and its impact on MRI results.")
    # prompts.append("What is the clinical significance of MRI findings in " + category + "?")
    # prompts.append("How can you identify " + article + " " + category + "?")
    prompts.append("What are the key distinguishing features of " + article + " " + category + " in medical imaging?")
    # prompts.append("What unique features should be looked for in an MRI when diagnosing " + article + " " + category + "?")
    prompts.append("What is the typical risk level associated with " + article + " " + category + "?")

    all_result = []
    for curr_prompt in tqdm(prompts):
        for i in tqdm(range(10)):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    temperature=0.99,
                    stop='.',
                    max_tokens=50,
                    messages=[
                        {"role": "system", "content": "I need you to generate a short and accurate description based on the ADNI dataset which includes NC (Normal Control), MCI (Mild Cognitive Impairment), and AD (Alzheimer's Disease) categories. Focus on distinguishing structural MRI features."},
                        {"role": "user", "content": curr_prompt},
                    ]
                )
                try:
                    for choice in response.choices:
                        try:
                            result = choice.message.content
                            all_result.append(result.replace("\n\n", "") + ".")
                        except:
                            continue
                except:
                    continue
            except:
                continue

    all_responses[category] = all_result

with open(json_name, 'w') as f:
    json.dump(all_responses, f, indent=4)

