import json

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

def summarize(news_article: str):
    # Read the news content parallely and summarize and add the summary to the file_name

    prompt = f"Summarize the below news article in about 50 words. Highlight the major takeaways from the article : {news_article}"

    model_name = "google/flan-t5-base"
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name
    ).to("cpu")

    tokenizer = AutoTokenizer.from_pretrained(model_name, padding_side="right")
    model_inputs = tokenizer([prompt], return_tensors="pt").to("cpu")

    generated_ids = model.generate(**model_inputs, max_new_tokens=100, max_length=100, num_beams=5, no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=0.7)
    output = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

    summary = output[0]
    print(summary)
    
    return summary

def summarize_wrapper(news_json_file):
    json_file = open(news_json_file)
    news_json_data = json.load(json_file)
    news_content = news_json_data['results'][0]['content']
    summary = summarize(news_article=news_content)
    # summary = 'Test Summary'
    news_json_data['results'][0]['summary'] = summary
    news_json_data = json.dumps(news_json_data, indent=4)
    with open(news_json_file, 'w') as fp:
        fp.write(news_json_data)
    return news_json_file

if __name__=="__main__":
    summarize_wrapper('../api_news/sample_data.json')

