#GENERAL API REQUEST IMPORTS
from flask import Flask, request, jsonify
from flask_cors import CORS
from waitress import serve

import matplotlib.pyplot as plt
import keras_ocr

# Create a Flask application instance
app = Flask(__name__)
# Enable CORS for all routes, allowing requests from any origin
CORS(app,resources={r"/*":{"origins":"*"}})

# Define a route for HTTP request
@app.route('/validate', methods=['POST'])
def detect_certificate_text():
    try:
        # Receive Data from Frontend API Request
        data = request.get_json()

        result = False

        pipeline = keras_ocr.pipeline.Pipeline()

        images = [
            data,
        ]

        words_found = [""]
        certificate_related_words = ["certificate", "certification", "university", "college", "institue", "degree", "graduate", "graduation" "coursework", "course", "certify", "association", "education", "organization", "program", "school", "award", "research", "appreciation", "presents", "present", "presented", "ministry", "certificat", "cisco", "google", "academy", "academic", "completed", "completion", "complete", "finished", "achievement", "pass", "passed", "programme", "program", "bachelor", "accreditation", "docotorate", "diploma", "training", "certifies", "certified", "honor", "honors", "department", "project", "congratulates", "congratulation", "professor", "digital", "requirements", "requirement", "doctor", "science", "president", "dean", "director", "ceo", "participation", "skill", "skills", "employment", "centre", "learn", "learning"]

        prediction = pipeline.recognize(images)

        for text, box in prediction[0]:
            words_found.append(text)

        print(words_found)

        for word in words_found:
            if word in certificate_related_words:
                print("a word exist")
                print(word)
                result = True
                break
            else:
                continue
        jsonify({'Certificate Words Found': result})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)