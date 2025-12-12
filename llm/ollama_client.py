import requests
from typing import Optional, Dict

class OllamaClient:
    """Client for interacting with local Ollama LLM server"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.1:8b"):
        self.base_url = base_url
        self.model = model
        self._test_connection()
    
    def _test_connection(self):
        """Test if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            print(f"✅ Connected to Ollama server")
            
            models = response.json().get('models', [])
            model_names = [m['name'] for m in models]
            
            if self.model not in model_names:
                print(f"⚠️ Model '{self.model}' not found. Available: {model_names}")
        except Exception as e:
            print(f"❌ Cannot connect to Ollama: {e}")
            print("Make sure Ollama is running: ollama serve")
    
    def generate(self, prompt: str, context: str = "", system_prompt: str = "") -> str:
        """Generate response from Ollama"""
        full_prompt = f"{system_prompt}\n\nContext:\n{context}\n\nUser Query: {prompt}\n\nResponse:"
        
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            return response.json().get('response', 'No response generated')
        except Exception as e:
            return f"⚠️ Error generating response: {e}"
    
    def stream_generate(self, prompt: str, context: str = "", system_prompt: str = ""):
        """Generate streaming response from Ollama"""
        full_prompt = f"{system_prompt}\n\nContext:\n{context}\n\nUser Query: {prompt}\n\nResponse:"
        
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": True
        }
        
        try:
            response = requests.post(url, json=payload, stream=True, timeout=120)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    import json
                    try:
                        data = json.loads(line)
                        if 'response' in data:
                            yield data['response']
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            yield f"⚠️ Error: {e}"