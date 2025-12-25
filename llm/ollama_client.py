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
        # Truncate context if too long (max ~4000 chars to be safe)
        max_context_length = 4000
        if len(context) > max_context_length:
            context = context[:max_context_length] + "\n\n[Context truncated due to length...]"
        
        full_prompt = f"{system_prompt}\n\nContext:\n{context}\n\nUser Query: {prompt}\n\nResponse:"
        
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "num_ctx": 4096,  # Context window size
                "temperature": 0.7
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            return response.json().get('response', 'No response generated')
        except requests.exceptions.HTTPError as e:
            # Try to get detailed error from response
            try:
                error_detail = response.json().get('error', str(e))
            except:
                error_detail = str(e)
            print(f"❌ Ollama HTTP Error: {error_detail}")
            return f"⚠️ Error generating response: {error_detail}\n\nTry using a smaller model like 'qwen:1.8b' or restart Ollama."
        except requests.exceptions.Timeout:
            return "⚠️ Request timed out. The model might be too slow or overloaded. Try a smaller model."
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
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