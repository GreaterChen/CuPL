import json
import torch
import clip
from tqdm import tqdm

# 加载CLIP模型
model, preprocess = clip.load("ViT-L/14", download_root="ViT-L")
model.eval()

# 输入JSON文件路径和输出文件路径
PATH_TO_PROMPTS = "result.json"
OUTPUT_FILE_PATH = "embedding_results.json"


# 函数：生成嵌入
def generate_embeddings(classnames, prompts_dict):
    with torch.no_grad():
        embeddings = {}
        for classname in tqdm(classnames):
            texts = prompts_dict[classname]
            texts = clip.tokenize(texts, truncate=True).cuda()  # Tokenize
            class_embeddings = model.encode_text(texts)  # Text embedding
            class_embeddings /= class_embeddings.norm(dim=-1, keepdim=True)
            class_embedding = class_embeddings.mean(dim=0)
            class_embedding /= class_embedding.norm()
            embeddings[classname] = class_embedding.cpu().numpy().tolist()  # 将tensor转换为列表并存储
        return embeddings


# 加载JSON文件中的数据
with open(PATH_TO_PROMPTS) as f:
    gpt3_prompts = json.load(f)

# 类别名和文本名（与JSON文件中的键一致）
classnames = list(gpt3_prompts.keys())

# 生成嵌入
print("Creating embeddings...")
embeddings = generate_embeddings(classnames, gpt3_prompts)
print("Done.\n")

# 保存嵌入到JSON文件
with open(OUTPUT_FILE_PATH, 'w') as f:
    json.dump(embeddings, f)

print(f"Embeddings saved to {OUTPUT_FILE_PATH}")
