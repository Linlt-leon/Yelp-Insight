import json
import pandas as pd
from tqdm import tqdm
import re
import random

import torch
import transformers
from transformers import AutoTokenizer


# function to get num1 and num2 from output
def get_num(output):
    pattern = r'\{([a-z-]+):(\d+),\s*([a-z-]+):(\d+)\}'
    matches = re.findall(pattern, output)
    list_of_dicts = [{match[0]: int(match[1]), match[2]: int(match[3])} for match in matches]
    # print(list_of_dicts)

    if len(list_of_dicts)==0:
        return random.randint(1, 5), random.randint(0, 1)

    if 'sentiment' in list_of_dicts[0]:
        num1 = list_of_dicts[0]['sentiment']
    else:
        num1 = random.randint(1, 5)
        
    if 'human-robot' in list_of_dicts[0]:
        num2 = list_of_dicts[0]['human-robot']
    else:
        num2 = random.randint(0, 1)
    
    return num1, num2


# load model and tokenizer
model = "/hy-tmp/llama-2-7b-chat-hf"
prompt = "What is the approximate number of luffas that a fully grown luffa tree can produce in a single growing season?\n"

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device_map="auto",
)


# load review data
with open('./yelp/yelp_academic_dataset_review.json') as f:
    data = [json.loads(line) for line in f]
review = pd.DataFrame(data)


# define system prompt and fewshot example
system_prompt = "System:\n You are useful robot good for sentiment analysis and meaning detection. The following are customer reviews of the business. You need to Classify the text into five sentiment level with number 1,2,3,4,5 (1:very negative, 2:negative, 3:neutral, 4:positive, 5:very positive) and classify the text into meaningful or meaningless with number 1 or 0 (1:human, 0:robot). Note that most of the review are '1:human'. You need to return results in the following form: 'Result:{sentiment:num1, human-robot:num2}.'"
fewshot_example = "\nExample: Review:Sometimes this food is very very good.  Unfortunately it's not consistent.   Ordered something I've been getting for years and every other time it tastes incredible. It's like they have different people in the kitchen and you don't know who you will get. So 50 % of the time it's excellent. \n Result:{sentiment:3, human-robot:1}.<\s>\n Review:It is good. \n Result:{sentiment:4, human-robot:0}.<\s> \n Review:HOLY SMOKES!\n\nactual pumpkin pie mixed in with the frozen custard......are you kidding me? Why hasn't this become a huge sweep the nation treat. \n\nThe best part was the chunks of pie crust. Like finding a diamond inside another diamond. Super yummy.\n Result:{sentiment:5, human-robot:1}.<\s>"

# initialize new review dataframe
review_new = review.copy()
review_new['sentiment'] = [0 for i in range(len(review))]
review_new['human-robot'] = [-1 for i in range(len(review))]

# generate new review data
for i in tqdm(range(5000)):
    user_input = '\nUser:\n Review:'+review_new['text'][i]+'\nResult:'
    prompt = system_prompt + fewshot_example + user_input
    sequences = pipeline(
        prompt,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=512,
    )
    
    gen_result = sequences[0]['generated_text'][len(prompt):]
    num1, num2 = get_num(gen_result)
    # print(num1,num2)

    review_new['sentiment'][i] = num1
    review_new['human-robot'][i] = num2
    
    
# save checkin_new to json
review_new[:5000].to_json('./yelp/yelp_academic_dataset_review_new_0_5000.json', orient='records', lines=True)
