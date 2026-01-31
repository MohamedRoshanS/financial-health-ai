from app.core.config import GROQ_API_KEY
from groq import Groq
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)
logger.info("Groq client initialized successfully")

def generate_ai_insights(analysis):
    logger.info(f"Starting AI insights generation for analysis with score: {analysis['score']}")
    
    prompt = f"""
You are a financial advisor for small and medium businesses in India.

Given this financial analysis:
Score: {analysis['score']} / 100
Status: {analysis['status']}

Score Breakdown:
{analysis['breakdown']}

Identified Risks:
{analysis['risks']}

Industry Benchmark Comparison:
{analysis['benchmarks']}

Forecast:
{analysis['forecast']}

Tasks:
1. Explain the financial health in simple language (non-finance owner).
2. Mention what is going well.
3. Mention what needs attention (if any).
4. Give 3 clear actionable recommendations.
5. Keep tone professional, friendly, and concise.
"""

    logger.info("Sending request to Llama 3.1 8B Instant model via Groq API")
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=1024
        )
        
        logger.info("Successfully received response from Groq API")
        logger.debug(f"Response token usage: {response.usage}")
        
        insights = response.choices[0].message.content
        logger.info(f"Generated insights length: {len(insights)} characters")
        
        return insights
        
    except Exception as e:
        logger.error(f"Error in generating AI insights: {str(e)}", exc_info=True)
        return f"Error generating insights. Please try again later."