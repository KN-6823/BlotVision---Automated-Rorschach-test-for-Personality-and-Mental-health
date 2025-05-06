from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
from transformers import pipeline
from templates import personality_templates, strengths_templates, weaknesses_templates, approach_templates
import random
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
import os
import traceback

app = Flask(__name__)

# --- Add CORS for BOTH endpoints ---
CORS(app, resources={
    r"/analyze": {
        "origins": "http://localhost:3000",
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    },
    r"/generate-report-image": {
        "origins": "http://localhost:3000",
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "expose_headers": ["Content-Disposition"]
    }
})
# --- End CORS ---

sentiment_analyzer = pipeline("sentiment-analysis")
emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
classifier = pipeline("text-classification", model="jtatman/roberta-base-biomed-myers-briggs-description-classifier")
attribute_classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

current_card_id_counter = 1

def analyze_sentiment(text):
    sentiment = sentiment_analyzer(text)
    return sentiment[0]

def analyze_emotion(text):
    emotions = emotion_analyzer(text)
    return max(emotions, key=lambda x: x['score']) if emotions else {"label": "neutral", "score": 0.0}

def generate_personality_report(sentiment, dominant_emotion, structured_data):
    report = {
        "Personality": "",
        "Strengths": [],
        "Weaknesses": [],
        "Approach": ""
    }

    if sentiment['label'] == 'NEGATIVE':
        report["Personality"] += random.choice(personality_templates["negative"])
    elif sentiment['label'] == 'POSITIVE':
        report["Personality"] += random.choice(personality_templates["positive"])
    
    emotion_label = dominant_emotion['label'].capitalize()
    if emotion_label in personality_templates["emotion_based"]:
        report["Personality"] += " " + random.choice(personality_templates["emotion_based"][emotion_label])
    
    if structured_data.get('FormQuality') == 'Excellent':
        report["Strengths"].extend(strengths_templates["FormQuality"]["Excellent"])
    elif structured_data.get('FormQuality') == 'Average':
        report["Strengths"].extend(strengths_templates["FormQuality"]["Average"])
    
    dev_quality = structured_data.get('DevelopmentalQuality')
    if dev_quality == 'Good':
        report["Strengths"].extend(strengths_templates["DevelopmentalQuality"]["Good"])
    elif dev_quality == 'Neutral':
        report["Strengths"].extend(strengths_templates["DevelopmentalQuality"]["Average"])
    
    if sentiment['label'] == 'NEGATIVE':
        report["Weaknesses"].extend(weaknesses_templates["negative_sentiment"])
    
    emotion_label_lower = dominant_emotion['label']
    if emotion_label_lower in weaknesses_templates["emotion_based"]:
        report["Weaknesses"].extend(weaknesses_templates["emotion_based"][emotion_label_lower])
    
    if structured_data.get('FormQuality') == 'Excellent' and sentiment['label'] == 'POSITIVE':
        report["Approach"] = random.choice(approach_templates["positive_sentiment"])
    elif sentiment['label'] == 'NEGATIVE':
        report["Approach"] = random.choice(approach_templates["negative_sentiment"])
    else:
        report["Approach"] = random.choice(approach_templates["neutral_sentiment"])
    
    return report

def classify_mbti_response(response):
    print(f"--- Classifying MBTI for Input ---")
    print(f"Input Text: '{response}'")
    # No try/except - let errors propagate if model fails
    result = classifier(response)
    print(f"Raw Classifier Output: {result}") # See the model's full output

    if result and isinstance(result, list) and result[0] and 'label' in result[0]:
        predicted_class = result[0]['label']
        print(f"Predicted MBTI Label: {predicted_class}")
        print("---------------------------------")
        return predicted_class
    else:
        print(f"Warning: Unexpected classifier output format: {result}")
        print("---------------------------------")
        return "Unknown" # Fallback if format is wrong

def infer_attributes(response):
    classification = attribute_classifier(response)
    attributes = {
        "Location": "Center" if "center" in response.lower() else "Other",
        "DevelopmentalQuality": "Good" if "detailed" in response.lower() else "Neutral",
        "FormQuality": "Excellent" if "precise" in response.lower() else "poor"
    }
    return attributes

def perform_single_analysis(row, card_id):
    response = row['Response']
    sentiment = analyze_sentiment(response)
    dominant_emotion = analyze_emotion(response)
    report_context = {**row, 'Sentiment': sentiment, 'DominantEmotion': dominant_emotion}
    personality_report = generate_personality_report(sentiment, dominant_emotion, row)
    mbti_result = classify_mbti_response(response)

    analysis_result = {
        "cardID": card_id,
        "Location": row['Location'],
        "DevelopmentalQuality": row['DevelopmentalQuality'],
        "FormQuality": row['FormQuality'],
        "Sentiment": sentiment,
        "Dominant Emotion": dominant_emotion,
        "Personality Report": personality_report,
        "MBTI Prediction": mbti_result
    }
    return analysis_result

def load_and_resize_image(image_path, size=(150, 150)):
    try:
        img = Image.open(image_path)
        img = img.resize(size)
        return img
    except FileNotFoundError:
        print(f"Error: Image not found at path: {image_path}")
        return Image.new("RGB", size, "#cccccc")
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return Image.new("RGB", size, "#cccccc")

def create_static_poster(most_common_mbti_type):
    print(f"\n--- Creating STATIC poster based on MBTI: {most_common_mbti_type} ---")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        csv_path = os.path.join(base_dir, "data", "OUTPUT.csv")
        df = pd.read_csv(csv_path, encoding="ISO-8859-1")
    except Exception as e:
        print(f"FATAL: Could not load or read CSV data from {csv_path}. Error: {e}")
        raise ValueError(f"Could not load required CSV data: {e}")

    row = df[df["Answer"] == most_common_mbti_type]
    if row.empty:
        print(f"Warning: No data found for MBTI type: {most_common_mbti_type} in CSV. Cannot create poster.")
        raise ValueError(f"MBTI type {most_common_mbti_type} not found in CSV.")

    data = row.iloc[0]
    image_width, image_height = 600, 800
    background_color = "#ffddd2"
    image = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)

    try:
        font_path_bold = os.path.join(base_dir, "fonts", "DejaVuSans-Bold.ttf")
        font_path_regular = os.path.join(base_dir, "fonts", "DejaVuSans.ttf")
        font_large = ImageFont.truetype(font_path_bold, 64)
        font_medium = ImageFont.truetype(font_path_bold, 24)
        font_small = ImageFont.truetype(font_path_regular if os.path.exists(font_path_regular) else font_path_bold, 16)
        print("Successfully loaded custom fonts.")
    except IOError:
        print("WARNING: Custom fonts not found in 'fonts' folder or failed to load. Using default.")
        font_large, font_medium, font_small = [ImageFont.load_default()] * 3

    image_path = data.get('Image')
    main_image = load_and_resize_image(image_path, size=(200, 185)) if pd.notna(image_path) else Image.new("RGB", (200,185), "#cccccc")

    container_spacing = 20
    header_height = 30
    subtext_height = 90
    container_height = header_height + subtext_height
    simple_container_height = 30
    image_container_height = 210

    y_offset = 80
    draw.rectangle([(30, y_offset), (270, y_offset + image_container_height)], fill="#cccccc", outline="black", width=2)
    image.paste(main_image, (50, y_offset + 10))
    y_offset += image_container_height + container_spacing

    for i in range(2):
        container_color = "#e6f7ff"; header_color = "#b3e0ff"; text_color = "#004080"; header_text_color = "#003366"
        draw.rectangle([(30, y_offset), (270, y_offset + container_height)], fill=container_color, outline="black", width=2)
        draw.rectangle([(30, y_offset), (270, y_offset + header_height)], fill=header_color, outline="black", width=2)
        header_text = "Strengths" if i == 0 else "Weaknesses"
        text_bbox = draw.textbbox((0, 0), header_text, font=font_medium)
        text_height = text_bbox[3] - text_bbox[1]
        header_x_offset = (270 - 30 - (text_bbox[2] - text_bbox[0])) / 2 + 30
        header_y_offset = y_offset + (header_height - text_height) / 2
        draw.text((header_x_offset, header_y_offset), header_text, font=font_medium, fill=header_text_color)
        strength_cols = [f"Strengths {j+1}" for j in range(3)]
        weakness_cols = [f"Weakness {j+1}" for j in range(3)]
        subtexts_keys = strength_cols if i == 0 else weakness_cols
        subtexts = [data.get(key, '') for key in subtexts_keys]
        for idx, text in enumerate(subtexts):
            bullet_y = y_offset + 40 + idx * 20
            draw.text((40, bullet_y), f"• {text}", font=font_small, fill=text_color)
        y_offset += container_height + container_spacing

    draw.rectangle([(30, y_offset), (270, y_offset + container_height)], fill="#ffe6cc", outline="black", width=2)
    draw.rectangle([(30, y_offset), (270, y_offset + header_height)], fill="#ffcc99", outline="black", width=2)
    header_text = "Strong attraction"
    text_bbox = draw.textbbox((0, 0), header_text, font=font_medium)
    header_x_offset = (270 - 30 - (text_bbox[2] - text_bbox[0])) / 2 + 30
    draw.text((header_x_offset, y_offset + 5), header_text, font=font_medium, fill="#994d00")
    image1_path = data.get('Strong attraction 1', '')
    image2_path = data.get('Strong attraction 2', '')
    image1 = load_and_resize_image(image1_path, size=(75, 75)) if pd.notna(image1_path) else Image.new("RGB", (75,75), "#CCCCCC")
    image2 = load_and_resize_image(image2_path, size=(75, 75)) if pd.notna(image2_path) else Image.new("RGB", (75,75), "#CCCCCC")
    image.paste(image1, (50, y_offset + 40))
    image.paste(image2, (160, y_offset + 40))

    y_offset = 50
    draw.text((350, y_offset), "You are...", font=font_medium, fill="black")
    y_offset += 30 + container_spacing
    title_text = data.get("Title", "Unknown Type")
    draw.text((450, y_offset), title_text, font=font_large, fill="#006d77", anchor="mm")
    y_offset += 30 + container_spacing
    percentage_val = data.get('Percentage', 0)
    draw.text((350, y_offset), f"{percentage_val}% people are also this type", font=font_medium, fill="black")
    y_offset += 30 + container_spacing

    for i in range(5):
        container_x1, container_y1 = 320, y_offset
        container_x2, container_y2 = 570, y_offset + simple_container_height
        draw.rectangle([ (container_x1, container_y1), (container_x2, container_y2) ], fill="#d9f2d9", outline="black", width=2)
        sentence_text = data.get(f"Sentence {i+1}", '')
        text_bbox = draw.textbbox((0, 0), sentence_text, font=font_medium)
        text_width = text_bbox[2] - text_bbox[0]
        text_x_offset = container_x1 + (container_x2 - container_x1 - text_width) / 2
        text_y_offset = container_y1 + 5
        draw.text((text_x_offset, text_y_offset), sentence_text, font=font_medium, fill="#006600")
        y_offset += simple_container_height + container_spacing

    container_color = "#ffe6e6"; header_color = "#ff9999"; text_color = "#cc0000"; header_text_color = "#800000"
    draw.rectangle([(320, y_offset), (570, y_offset + container_height)], fill=container_color, outline="black", width=2)
    draw.rectangle([(320, y_offset), (570, y_offset + header_height)], fill=header_color, outline="black", width=2)
    header_text = "Qualities"
    text_bbox = draw.textbbox((0, 0), header_text, font=font_medium)
    header_x_offset = (570 - 320 - (text_bbox[2] - text_bbox[0])) / 2 + 320
    draw.text((header_x_offset, y_offset + 5), header_text, font=font_medium, fill=header_text_color)
    draw.text((340, y_offset + 40), data.get("Qualities 1", ''), font=font_medium, fill=text_color)
    draw.text((340, y_offset + 70), data.get("Qualities 2", ''), font=font_small, fill=text_color)
    draw.text((340, y_offset + 100), data.get("Qualities 3", ''), font=font_small, fill=text_color)
    y_offset += container_height + container_spacing

    draw.rectangle([(320, y_offset), (570, y_offset + container_height)], fill="#e6ccff", outline="black", width=2)
    draw.rectangle([(320, y_offset), (570, y_offset + header_height)], fill="#d1b3ff", outline="black", width=2)
    header_text = "Weak attraction"
    text_bbox = draw.textbbox((0, 0), header_text, font=font_medium)
    header_x_offset = (570 - 320 - (text_bbox[2] - text_bbox[0])) / 2 + 320
    draw.text((header_x_offset, y_offset + 5), header_text, font=font_medium, fill="#4d0066")
    image1_path = data.get('Weak attraction 1', '')
    image2_path = data.get('Weak attraction 2', '')
    image1 = load_and_resize_image(image1_path, size=(75, 75)) if pd.notna(image1_path) else Image.new("RGB", (75,75), "#CCCCCC")
    image2 = load_and_resize_image(image2_path, size=(75, 75)) if pd.notna(image2_path) else Image.new("RGB", (75,75), "#CCCCCC")
    image.paste(image1, (340, y_offset + 40))
    image.paste(image2, (460, y_offset + 40))

    output_filename = f"{most_common_mbti_type}_poster_static.png"
    try:
        image.save(output_filename)
        print(f"Saved static poster: {output_filename}")
        return output_filename
    except Exception as e:
        print(f"Error saving static poster {output_filename}: {e}")
        raise IOError(f"Failed to save image {output_filename}")

@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze_endpoint():
    global current_card_id_counter

    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        return response

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    data = request.get_json()
    user_response = data.get('response')
    if not user_response:
        return jsonify({"error": "Missing 'response' in request body"}), 400

    print(f"\n--- Analyzing response Card ID {current_card_id_counter} ---")
    inferred_attributes = infer_attributes(user_response)
    row = {"Response": user_response, **inferred_attributes}

    try:
        analysis_result = perform_single_analysis(row, current_card_id_counter)
        current_card_id_counter += 1
        print(f"--- Analysis Complete for Card ID {analysis_result['cardID']} ---")
        print(analysis_result)
        response = jsonify(analysis_result)
        return response
    except Exception as e:
        print(f"Error during analysis: {traceback.format_exc()}")
        return jsonify({"error": f"Analysis failed: {e}"}), 500

@app.route('/generate-report-image', methods=['POST', 'OPTIONS'])
def generate_report_image_endpoint():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        return response

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    data = request.get_json()
    analysis_results = data.get('responses')

    if not analysis_results or not isinstance(analysis_results, list):
        return jsonify({"error": "Missing or invalid 'responses' data in request"}), 400

    print(f"\n--- Generating Final Report from {len(analysis_results)} results ---")
    global current_card_id_counter
    current_card_id_counter = 1

    try:
        if analysis_results:
            mbti_types = [res.get('MBTI Prediction', 'Unknown') for res in analysis_results if isinstance(res, dict)]
            most_common_mbti_type = Counter(mbti_types).most_common(1)[0][0] if mbti_types else "Unknown"
        else:
            most_common_mbti_type = "Unknown"

        print(f"Most Common MBTI Type: {most_common_mbti_type}")

        output_filename = create_professional_poster(analysis_results)

        if output_filename is None:
            raise ValueError("Poster creation failed (returned None). Check logs.")

        file_path = os.path.join(os.getcwd(), output_filename)

        if not os.path.exists(file_path):
            print(f"Error: Poster file '{output_filename}' not found after creation.")
            raise FileNotFoundError(f"Generated file not found: {output_filename}")

        print(f"Sending file: {file_path}")
        response = send_file(
            file_path,
            mimetype='image/png',
            as_attachment=True,
            download_name=output_filename
        )
        return response

    except Exception as e:
        print(f"Error during report generation: {traceback.format_exc()}")
        return jsonify({"error": f"Failed to generate report: {e}"}), 500

def create_professional_poster(analysis_results):
    print(f"--- Creating DYNAMIC professional poster from {len(analysis_results)} results ---")
    final_mbti_type = Counter([r.get('MBTI Prediction','?') for r in analysis_results]).most_common(1)[0][0]
    output_filename = f"{final_mbti_type}_professional_report.png"
    # ... (image saving logic) ...
    print(f"Placeholder: Would save dynamic poster as {output_filename}")
    # For testing return a known name, replace with actual save+return
    # Make sure this file actually gets created by the function's implementation
    # For now, just return a placeholder filename to test flow:
    # return output_filename

    # TEMPORARY: Call static just to return *something* until dynamic is fully implemented
    # REMOVE THIS LINE WHEN create_professional_poster IS FULLY IMPLEMENTED
    return create_static_poster(final_mbti_type)

if __name__ == '__main__':
    if not os.path.exists('data'): os.makedirs('data')
    if not os.path.exists('fonts'): os.makedirs('fonts'); print("Created 'fonts' dir.")

    print("Starting Flask app on http://localhost:5000 ...")
    app.run(debug=True, port=5000)
