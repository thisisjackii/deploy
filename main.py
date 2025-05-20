import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import spacy
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.get_json()
        text = data['text']

        try:
            nlp_ner = spacy.load("./models/model-best")
            doc = nlp_ner(text) # input sample text   
            d = []
            if len(doc.ents) > 0:
                for ent in doc.ents:
                    # d.append((ent.label_, ent.text))
                    d.append({
                        "start": ent.start_char,
                        "end": ent.end_char,
                        "label": ent.label_,
                        "text": ent.text,
                    })
                return jsonify(
                    {
                        "text": text,
                        "ner_tag": d
                    })
            else:
                return jsonify({"error": "NER Tag Not Found"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return "OK"

if __name__ == "__main__":
    app.run(debug=True)