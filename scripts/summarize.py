from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

MODEL_NAME = "facebook/bart-large-cnn"
# MODEL_NAME = "t5-small"
TOKENIZER = AutoTokenizer.from_pretrained(MODEL_NAME)
MODEL = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
SUMMARIZER = pipeline(task="summarization",
                      model=MODEL,
                      tokenizer=TOKENIZER)

def get_summary(text: str) -> str:
    return SUMMARIZER(text[:1024])[0]["summary_text"]
