from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import logging
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
app = Flask(__name__, 
    static_folder='Frontend',
    template_folder='Frontend'
)
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
    raise

@app.route('/')
def index():
    """Serve the main application page."""
    return render_template('index.html', 
                         username=Username, 
                         assistant_name=Assistantname)

@app.route('/help')
def help():
    """Serve the help page."""
    return render_template('help.html')

@app.route('/about')
def about():
    """Serve the about page."""
    return render_template('about.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests."""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400

        user_message = data['message']
        logger.info(f"Processing message: {user_message}")

        # Process the message through the decision model
        decision = model(user_message)
        logger.info(f"Decision model output: {decision}")

        response = ""
        for query in decision:
            if "generate" in query:
                response = "Sorry, I can't generate that yet."
            elif "realtime" in query:
                try:
                    response = search_engine.search(query)
                    text_to_speech.speak(response)
                except Exception as e:
                    logger.error(f"Error in realtime search: {str(e)}")
                    response = f"Error processing real-time search: {str(e)}"
            elif "general" in query:
                response = chatbot.process_message(query)
                text_to_speech.speak(response)
            else:
                response = chatbot.process_message(query)

        return jsonify({"response": response})
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/api/speech', methods=['POST'])
def speech():
    """Handle speech recognition requests."""
    try:
        text = speech_recognition.listen()
        if not text:
            return jsonify({"error": "No speech detected"}), 400
        return jsonify({"text": text})
    except Exception as e:
        logger.error(f"Error in speech endpoint: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == '__main__':
    try:
        logger.info("Starting server...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
