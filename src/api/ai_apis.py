"""
AI API Integrations
Connect to external AI services to learn from them
"""

import os
from typing import Optional, Dict, Any, List
import yaml
import logging
from dotenv import load_dotenv

# API clients (will be imported conditionally)
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class AIAPIs:
    """Manages connections to external AI APIs for learning"""

    def __init__(self, config_path: str = "configs/config.yaml"):
        self.config = self._load_config(config_path)
        self.clients = {}
        self._initialize_clients()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration"""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _initialize_clients(self) -> None:
        """Initialize API clients based on available keys"""

        # Groq
        if GROQ_AVAILABLE and self.config['apis']['groq']['enabled']:
            api_key = os.getenv('GROQ_API_KEY')
            if api_key:
                self.clients['groq'] = Groq(api_key=api_key)
                logger.info("Groq API initialized")
            else:
                logger.warning("Groq enabled but no API key found")

        # OpenAI
        if OPENAI_AVAILABLE and self.config['apis']['openai'].get('enabled', False):
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.clients['openai'] = OpenAI(api_key=api_key)
                logger.info("OpenAI API initialized")

        # Anthropic
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if ANTHROPIC_AVAILABLE and anthropic_key:
            self.clients['anthropic'] = Anthropic(api_key=anthropic_key)
            logger.info("Anthropic API initialized")

        # HuggingFace
        hf_token = os.getenv('HUGGINGFACE_TOKEN')
        if hf_token and self.config['apis']['huggingface']['enabled']:
            self.clients['huggingface'] = hf_token
            logger.info("HuggingFace token loaded")

        if not self.clients:
            logger.warning("No API clients initialized. Check your .env file and API keys.")

    def query_groq(self, prompt: str, system: Optional[str] = None) -> str:
        """Query Groq API"""
        if 'groq' not in self.clients:
            raise ValueError("Groq client not initialized")

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.clients['groq'].chat.completions.create(
                model=self.config['apis']['groq']['model'],
                messages=messages,
                max_tokens=self.config['apis']['groq']['max_tokens']
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            return ""

    def query_openai(self, prompt: str, system: Optional[str] = None) -> str:
        """Query OpenAI API"""
        if 'openai' not in self.clients:
            raise ValueError("OpenAI client not initialized")

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.clients['openai'].chat.completions.create(
                model=self.config['apis']['openai']['model'],
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return ""

    def query_huggingface(self, prompt: str, model: Optional[str] = None) -> str:
        """Query HuggingFace Inference API"""
        if 'huggingface' not in self.clients:
            raise ValueError("HuggingFace token not available")

        model = model or self.config['apis']['huggingface']['model']
        api_url = f"https://api-inference.huggingface.co/models/{model}"

        headers = {"Authorization": f"Bearer {self.clients['huggingface']}"}
        payload = {"inputs": prompt}

        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '')
                return str(result)
            else:
                logger.error(f"HuggingFace API error: {response.status_code}")
                return ""
        except Exception as e:
            logger.error(f"HuggingFace API error: {e}")
            return ""

    def query_any(self, prompt: str, prefer: Optional[str] = None) -> Dict[str, str]:
        """Query any available API and return response"""

        if prefer and prefer in self.clients:
            apis_to_try = [prefer] + [k for k in self.clients.keys() if k != prefer]
        else:
            apis_to_try = list(self.clients.keys())

        for api_name in apis_to_try:
            try:
                if api_name == 'groq':
                    response = self.query_groq(prompt)
                elif api_name == 'openai':
                    response = self.query_openai(prompt)
                elif api_name == 'huggingface':
                    response = self.query_huggingface(prompt)
                else:
                    continue

                if response:
                    return {
                        "source": api_name,
                        "response": response
                    }
            except Exception as e:
                logger.warning(f"Failed to query {api_name}: {e}")
                continue

        return {
            "source": "none",
            "response": ""
        }

    def learn_from_apis(self, questions: List[str]) -> List[Dict[str, Any]]:
        """Ask multiple questions to APIs and collect responses"""

        learning_data = []

        for question in questions:
            logger.info(f"Asking: {question}")

            result = self.query_any(question)

            if result['response']:
                learning_data.append({
                    "question": question,
                    "answer": result['response'],
                    "source": result['source']
                })

        return learning_data


if __name__ == "__main__":
    # Test API connections
    apis = AIAPIs()

    test_prompt = "Explain what machine learning is in one sentence."
    result = apis.query_any(test_prompt)

    print(f"\nPrompt: {test_prompt}")
    print(f"Source: {result['source']}")
    print(f"Response: {result['response']}")
