from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging
import traceback
from Backend.SpeechToText import SpeechRecognition
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from Backend.Model import FirstLayerDMM
from dotenv import dotenv_values

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Assistant")

# Initialize Flask app
app = Flask(__name__, static_folder='../Frontend')
CORS(app)

# Initialize components
try:
    logger.info("Initializing components...")
    speech_recognition = SpeechRecognition()
    search_engine = RealtimeSearchEngine()
    chatbot = ChatBot()
    text_to_speech = TextToSpeech()
    model = FirstLayerDMM()
    logger.info("All components initialized successfully")
except Exception as e:
    logger.error(f"Error initializing components: {str(e)}")
    logger.error(traceback.format_exc())
    raise

@app.route('/')
def serve_index():
    try:
        logger.info("Serving index.html")
        return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        logger.error(f"Error serving index.html: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "Failed to serve index.html"}), 500

@app.route('/<path:path>')
def serve_static(path):
    try:
        logger.info(f"Serving static file: {path}")
        return send_from_directory(app.static_folder, path)
    except Exception as e:
        logger.error(f"Error serving static file {path}: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": f"Failed to serve {path}"}), 404

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        logger.info("Received chat request")
        data = request.get_json()
        logger.info(f"Request data: {data}")
        
        if not data or 'message' not in data:
            logger.error("No message provided in request")
            return jsonify({"error": "No message provided"}), 400

        user_message = data['message']
        logger.info(f"Processing message: {user_message}")

        # Process the message through the decision model first
        decision = model(user_message)
        logger.info(f"Decision model output: {decision}")

        response = ""
        for query in decision:
            if "generate" in query:
                response = "Sorry, I can't generate that yet."
            elif "realtime" in query:
                try:
                    response = search_engine.search(query)
                    text_to_speech(response)
                except Exception as e:
                    logger.error(f"Error in realtime search: {str(e)}")
                    response = f"Error processing real-time search: {str(e)}"
            elif "general" in query:
                response = chatbot.process_message(query)
                text_to_speech(response)
            else:
                response = chatbot.process_message(query)

        logger.info(f"Final response: {response}")
        return jsonify({"response": response})
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/api/speech', methods=['POST'])
def speech():
    try:
        logger.info("Received speech recognition request")
        
        # Get speech input and convert to text
        text = speech_recognition.listen()
        if not text:
            logger.error("No speech detected")
            return jsonify({"error": "No speech detected"}), 400

        logger.info(f"Recognized speech: {text}")
        return jsonify({"text": text})
    except Exception as e:
        logger.error(f"Error in speech endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == '__main__':
    try:
        logger.info("Starting server...")
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        logger.error(traceback.format_exc()) 