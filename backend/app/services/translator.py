from groq import Groq
from app.core.config import GROQ_API_KEY
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)
def translate_text(text, language):
    if language == "en":
        logger.info(f"Language is English, returning original text (length: {len(text)} chars)")
        return text

    logger.info(f"Translating text from English to {language}")
    logger.debug(f"Text to translate (first 100 chars): {text[:100]}...")
    
    prompt = f"Translate the following financial advice into {language}:\n{text}"

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1024
        )
        
        logger.info(f"Successfully translated text to {language}")
        translation = response.choices[0].message.content
        logger.debug(f"Translated text (first 100 chars): {translation[:100]}...")
        
        return translation
        
    except Exception as e:
        logger.error(f"Error in translating text to {language}: {str(e)}", exc_info=True)
        return text  # Return original text as fallback