from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

def summarize(file_name: str):
    # Read the news content parallely and summarize and add the summary to the file_name

    new_article = """
        Customers and partners across all industries and of all sizes are using Amazon Q to transform the way their employees get work done. This is AWS has announced the general availability of Amazon Q, the most capable generative artificial intelligence (AI)-powered assistant for accelerating software development and leveraging companies’ internal data. Amazon Q not only generates highly accurate code, it also tests, debugs, and has multi-step planning and reasoning capabilities that can transform and implement new code generated from developer requests. Amazon Q also makes it easier for employees to get answers to questions across business data such as company policies, product information, business results, code base, employees, and many other topics by connecting to enterprise data repositories to summarize the data logically, analyze trends, and engage in dialog about the data. “Amazon Q is the most capable generative AI-powered assistant available today with industry-leading accuracy, advanced agents capabilities, and best-in-class security that helps developers become more productive and helps business users to accelerate decision making,” said Dr. Swami Sivasubramanian, vice president of Artificial Intelligence and Data at AWS. “Since we announced the service at re:Invent, we have been amazed at the productivity gains developers and business users have seen. Early indications signal Amazon Q could help our customers’ employees become more than 80% more productive at their jobs; and with the new features we’re planning on introducing in the future, we think this will only continue to grow.” Today’s announcement includes the general availability of Amazon Q Developer and Amazon Q Business, as well as the new Amazon Q Apps capability (in preview). Here’s a quick look at what they can do:
    """
    prompt = f"Summarize the below news article in about 50 words. Highlight the major takeaways from the article : {new_article}"

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
    
    result = {}
    return result

