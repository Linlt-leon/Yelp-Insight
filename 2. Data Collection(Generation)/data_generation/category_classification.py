import json
import pandas as pd
from tqdm import tqdm
import re
import random

import torch
import transformers
from transformers import AutoTokenizer


# categories
Categories = ['Delivery', 'Burgers', 'Chinese', 'Italian', 'Reservations', 'Japanese', 'Mexican', 'Thai', 'Contractors', 'Electricians', 'Home Cleaners', 'HVAC', 'Landscaping', 'Locksmiths', 'Movers', 'Plumbers', 'Auto Repair', 'Auto Detailing', 'Body Shops', 'Car Wash', 'Car Dealers', 'Oil Change', 'Parking', 'Towing', 'Dry Cleaning', 'Phone Repair', 'Bars', 'Nightlife', 'Hair Salons', 'Gyms', 'Massage', 'Shopping', 'Health', 'Restaurants', 'Food', 'Others']

# define function to get category
def get_category(long_string):
    pattern = r'<([^>]+)>'
    category_match = re.search(pattern, long_string)
    category_name = category_match.group(1) if category_match else None
    
    if category_name is not None and category_name in Categories:
        return category_name
    else:
        return "Others"


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


# load business data
with open('./yelp/yelp_academic_dataset_business.json') as f:
    data = [json.loads(line) for line in f]
business = pd.DataFrame(data)



# define system prompt and fewshot example
system_prompt = "System:\n You are useful robot for business categories detection. The following are the labels of the business. You need to Classify the business into one of the 36 categories below {'Delivery', 'Burgers', 'Chinese', 'Italian', 'Reservations', 'Japanese', 'Mexican', 'Thai', 'Contractors', 'Electricians', 'Home Cleaners', 'HVAC', 'Landscaping', 'Locksmiths', 'Movers', 'Plumbers', 'Auto Repair', 'Auto Detailing', 'Body Shops', 'Car Wash', 'Car Dealers', 'Oil Change', 'Parking', 'Towing', 'Dry Cleaning', 'Phone Repair', 'Bars', 'Nightlife', 'Hair Salons', 'Gyms', 'Massage', 'Shopping', 'Health', 'Restaurants', 'Food', 'Others'}. You need to return results in the following form: 'Identify Category:<category_name>'"
fewshot_example = "\nExample: categories: 'Doctors, Traditional Chinese Medicine, Naturopathic/Holistic, Acupuncture, Health & Medical, Nutritionists' \n Identify Category:<Health>.<\s> \n categories: 'Department Stores, Shopping, Fashion, Home & Garden, Electronics, Furniture Stores' \n Identify Category:<Shopping>.<\s> \n categories: Shipping Centers, Local Services, Notaries, Mailbox Centers, Printing Services \n Identify Category:<Others>.<\s>"


# initialize new review dataframe
business_new = business.copy()
business_new['category_new'] = ["" for i in range(len(business))]

for i in tqdm(range(5000)):
    user_input = '\nUser:\n categories:'+str(business['categories'][i])+'\nIdentify Category:'
    prompt = system_prompt + fewshot_example + user_input
    sequences = pipeline(
        prompt,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=512,
    )
    
    gen_result = sequences[0]['generated_text'][len(prompt):min(len(prompt)+25,len(sequences[0]['generated_text']))]
    # print(gen_result)
    category = get_category(gen_result)
    # print(category)

    business_new['category_new'][i] = category
    
    
# save business_new to json
business_new[:5000].to_json('./yelp/yelp_academic_dataset_business_new_0_5000.json', orient='records', lines=True)
