from openai import OpenAI
import json
from tqdm import tqdm
import os

client = OpenAI(
    api_key="sk-72f0655555424cfca18341651dbf5f40",
    base_url="https://api.deepseek.com",
)

json_name = "/home/chenlb/CuPL/dr/DR_prompt_result.json"

category_list = ["NO-DR", "Mild NPDR", "Moderate NPDR", "Severe NPDR", "PDR"]
all_responses = {}
vowel_list = ['A', 'E', 'I', 'O', 'U']

for category in category_list:
    if category[0].upper() in vowel_list:
        article = "an"
    else:
        article = "a"

    prompts = []
    prompts.append("Describe the significant fundus features of " + category + ".")
    prompts.append("What are the characteristic fundus findings of " + category + "?")
    prompts.append("How does " + category + " manifest in fundus images?")
    prompts.append("What are the key markers for diagnosing " + category + " in fundus imaging?")
    prompts.append("Describe the fundus characteristics that are typical for " + category + ".")
    prompts.append("What unique features should be looked for when diagnosing " + category + " in fundus images?")
    prompts.append("What are the stages or severity levels of " + category + " in diabetic retinopathy?")
    prompts.append("What are the key distinguishing features of " + article + " " + category + " in fundus imaging?")
    prompts.append("What is the typical risk level associated with " + article + " " + category + " in diabetic retinopathy?")


    all_result = []
    for curr_prompt in tqdm(prompts):
        try:
            messages=[
                {"role": "system", "content": 'I need you to generate a short and accurate description based on diabetic retinopathy classifications, which include NO-DR (No Diabetic Retinopathy), Mild NPDR (Mild Non-Proliferative Diabetic Retinopathy), Moderate NPDR (Moderate Non-Proliferative Diabetic Retinopathy), Severe NPDR (Severe Non-Proliferative Diabetic Retinopathy), and PDR (Proliferative Diabetic Retinopathy) categories. Focus on distinguishing clinical features, such as microaneurysms, hemorrhages, venous beading, and neovascularization. Each time you respond, you should provide ten answers. The ten answers should be as different as possible, addressing the question from different angles, while keeping them as concise as possible. Sample Json Output: {"results:["NO-DR indicates the absence of any diabetic retinopathy-related changes in the retina.", "NO-DR is characterized by the absence of any diabetic retinopathy-related changes in the retina."]}'},
                {"role": "user", "content": curr_prompt},
            ]

            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                temperature=0.99,
                response_format={'type': 'json_object'}
            )
                    
            try:
                results = json.loads(response.choices[0].message.content)['results']
                for result in results:
                    all_result.append(result)
            except Exception as e:
                print(e)
                continue
        except Exception as e:
            print(e)

            continue

    all_responses[category] = all_result

with open(json_name, 'w') as f:
    json.dump(all_responses, f, indent=4)

