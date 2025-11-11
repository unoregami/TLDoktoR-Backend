from flask import Flask, request, jsonify
import spacy
from summarizer import Summarizer
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")
model = Summarizer()
ytt_api = YouTubeTranscriptApi()

def clean_transcript(text):
    text = re.sub(r'\[?\d{1,2}:\d{2}(?::\d{2})?\]?', '', text)
    text = re.sub(r'^[A-Za-z ]+:', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s*\n\s*', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text).strip()
    doc = nlp(text)
    sentences = []
    for sent in doc.sents:
        s = sent.text.strip()
        if not s.endswith(('.', '?', '!')):
            s += '.'
        sentences.append(s.capitalize())
    return ' '.join(sentences)

def getText(transcript):
    return "\n".join([i['text'] for i in transcript])

def get_summary_ratio(summary_type):
    ratios = {"short": 0.2, "medium": 0.4, "long": 0.6}
    return ratios.get(summary_type.lower(), 0.4)

@app.route('/summarize_text', methods=['POST'])
def summarize_text():
    data = request.get_json()
    text = data.get("text", "")
    summary_type = data.get("summary_type", "medium")

    if not text:
        return jsonify({"error": "No input text provided"}), 400

    doc = nlp(text)
    cleaned_text = " ".join([sent.text for sent in doc.sents])
    ratio = get_summary_ratio(summary_type)
    summary = model(cleaned_text, ratio=ratio)
    return jsonify({"summary": summary})

@app.route('/summarize_youtube', methods=['POST'])
def summarize_youtube():
    data = request.get_json()
    url = data.get("url", "")
    summary_type = data.get("summary_type", "medium")

    try:
        if "youtube" in url:
            video_id = url.split("v=")[1].split("&")[0]
        else:
            video_id = url.split("/")[-1]

        transcript = ytt_api.get_transcript(video_id)
        input_text = clean_transcript(getText(transcript))
        doc = nlp(input_text)
        cleaned_text = " ".join([sent.text for sent in doc.sents])
        ratio = get_summary_ratio(summary_type)
        summary = model(cleaned_text, ratio=ratio)
        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


#hello
#hi
