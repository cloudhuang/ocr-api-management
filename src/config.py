from dotenv import load_dotenv
import os

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the .env file in the parent directory
env_path = os.path.join(current_dir, '..', '.env')

# Load environment variables from .env file
load_dotenv(dotenv_path=env_path, override=True)

# Example usage:
# API_KEY = os.getenv("API_KEY")
# DATABASE_URL = os.getenv("DATABASE_URL")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OLLAMA_HOST = os.getenv("OLLAMA_HOST")
OLLAMA_KEY = os.getenv("OLLAMA_KEY")
VLLM_MODEL = os.getenv("VLLM_MODEL", "qwen2.5vl:32b")  # Default to llama3-70b-instruct if not set

if __name__ == "__main__":
    # Print the loaded configuration for debugging
    print(f"OLLAMA_MODEL: {OLLAMA_MODEL}")
    print(f"OLLAMA_HOST: {OLLAMA_HOST}")
    print(f"OLLAMA_KEY: {OLLAMA_KEY}")
    print(f"VLLM_MODEL: {VLLM_MODEL}")