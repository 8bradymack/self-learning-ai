"""
Base Model Loader
Handles loading and managing the base language model on M3 Mac
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, PeftModel
import yaml
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelLoader:
    """Manages loading and inference for the base model"""

    def __init__(self, config_path: str = "configs/config.yaml"):
        self.config = self._load_config(config_path)
        self.model = None
        self.tokenizer = None
        self.device = self._get_device()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _get_device(self) -> str:
        """Determine best available device"""
        if torch.backends.mps.is_available():
            logger.info("Using Apple Silicon MPS backend")
            return "mps"
        elif torch.cuda.is_available():
            logger.info("Using CUDA GPU")
            return "cuda"
        else:
            logger.info("Using CPU (will be slow)")
            return "cpu"

    def load_base_model(self, model_name: Optional[str] = None) -> None:
        """Load the base language model"""
        if model_name is None:
            model_name = self.config['model']['base_model']

        logger.info(f"Loading model: {model_name}")

        try:
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=True
            )

            # Add padding token if missing
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            # Load model with appropriate settings for M3
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )

            logger.info(f"Model loaded successfully on {self.device}")
            logger.info(f"Model parameters: {self.model.num_parameters():,}")

        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise

    def generate(self, prompt: str, max_length: Optional[int] = None, **kwargs) -> str:
        """Generate text from prompt"""
        if self.model is None or self.tokenizer is None:
            raise ValueError("Model not loaded. Call load_base_model() first.")

        max_length = max_length or self.config['model']['max_length']

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=self.config['model'].get('temperature', 0.7),
                do_sample=True,
                **kwargs
            )

        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Remove the prompt from the output
        response = generated_text[len(prompt):].strip()
        return response

    def prepare_for_training(self) -> None:
        """Prepare model for LoRA fine-tuning"""
        if self.model is None:
            raise ValueError("Model not loaded. Call load_base_model() first.")

        learning_config = self.config['learning']

        # Configure LoRA
        lora_config = LoraConfig(
            r=learning_config['lora_r'],
            lora_alpha=learning_config['lora_alpha'],
            lora_dropout=learning_config['lora_dropout'],
            target_modules=learning_config['target_modules'],
            bias="none",
            task_type="CAUSAL_LM"
        )

        # Apply LoRA to model
        self.model = get_peft_model(self.model, lora_config)
        self.model.print_trainable_parameters()

        logger.info("Model prepared for LoRA training")

    def save_model(self, path: str) -> None:
        """Save model and tokenizer"""
        if self.model is None or self.tokenizer is None:
            raise ValueError("No model to save")

        Path(path).mkdir(parents=True, exist_ok=True)
        self.model.save_pretrained(path)
        self.tokenizer.save_pretrained(path)
        logger.info(f"Model saved to {path}")

    def load_checkpoint(self, path: str) -> None:
        """Load a saved checkpoint"""
        logger.info(f"Loading checkpoint from {path}")

        self.tokenizer = AutoTokenizer.from_pretrained(path)
        base_model_name = self.config['model']['base_model']

        # Load base model
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )

        # Load LoRA weights
        self.model = PeftModel.from_pretrained(base_model, path)
        logger.info("Checkpoint loaded successfully")


if __name__ == "__main__":
    # Test the model loader
    loader = ModelLoader()
    loader.load_base_model()

    test_prompt = "What is artificial intelligence?"
    response = loader.generate(test_prompt)
    print(f"\nPrompt: {test_prompt}")
    print(f"Response: {response}")
