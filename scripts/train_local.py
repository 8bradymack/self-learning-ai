#!/usr/bin/env python3
"""
Local Training Script
Fine-tunes the model on accumulated knowledge using LoRA
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import json
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
from datasets import Dataset
import yaml
from datetime import datetime

def load_config():
    """Load configuration"""
    with open('configs/config.yaml', 'r') as f:
        return yaml.safe_load(f)

def load_training_data(file_path='training_data.json'):
    """Load training data from JSON"""
    print(f"\n📂 Loading training data from {file_path}...")
    with open(file_path, 'r') as f:
        data = json.load(f)
    print(f"✓ Loaded {len(data)} training examples")
    return data

def prepare_dataset(data, tokenizer):
    """Convert training data to HuggingFace dataset"""
    print("\n🔧 Preparing dataset...")

    # Format as conversational prompts
    texts = []
    for item in data:
        # Create instruction-following format
        text = f"Question: {item['prompt']}\n\nAnswer: {item['completion']}"
        texts.append(text)

    # Tokenize
    def tokenize_function(examples):
        return tokenizer(
            examples['text'],
            truncation=True,
            max_length=512,
            padding='max_length'
        )

    # Create dataset
    dataset = Dataset.from_dict({'text': texts})
    tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=['text'])

    print(f"✓ Dataset prepared with {len(tokenized_dataset)} examples")
    return tokenized_dataset

def setup_model_and_lora(config):
    """Load model and apply LoRA"""
    print("\n🤖 Loading base model...")

    model_name = config['model']['base_model']
    device = config['model']['device']

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Load model
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map=device,
        torch_dtype=torch.float32  # MPS works best with float32
    )

    print(f"✓ Model loaded: {model_name}")
    print(f"✓ Device: {device}")
    print(f"✓ Parameters: {model.num_parameters():,}")

    # Setup LoRA
    print("\n🔧 Configuring LoRA...")
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=config['learning']['lora_r'],
        lora_alpha=config['learning']['lora_alpha'],
        lora_dropout=config['learning']['lora_dropout'],
        target_modules=["c_attn"],  # GPT2 attention modules
        bias="none"
    )

    model = get_peft_model(model, lora_config)
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())

    print(f"✓ LoRA applied")
    print(f"✓ Trainable parameters: {trainable_params:,} ({100 * trainable_params / total_params:.2f}%)")

    return model, tokenizer

def train_model(model, tokenizer, dataset, config):
    """Train the model with LoRA"""
    print("\n🚀 Starting training...\n")

    # Training arguments
    output_dir = f"data/models/checkpoints_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=config['learning']['batch_size'],
        gradient_accumulation_steps=config['learning']['gradient_accumulation_steps'],
        learning_rate=float(config['learning']['learning_rate']),
        warmup_steps=config['learning']['warmup_steps'],
        logging_steps=10,
        save_steps=50,
        save_total_limit=2,
        logging_dir=f"{output_dir}/logs",
        report_to="none",
        remove_unused_columns=False,
        use_cpu=False if config['model']['device'] in ['mps', 'cuda'] else True,
    )

    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False  # Causal LM, not masked LM
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=data_collator,
    )

    # Train!
    print("="*60)
    print("TRAINING IN PROGRESS")
    print("="*60)
    trainer.train()

    print("\n✅ Training complete!")

    # Save final model
    final_model_path = "data/models/trained_model"
    model.save_pretrained(final_model_path)
    tokenizer.save_pretrained(final_model_path)

    print(f"\n💾 Model saved to: {final_model_path}")
    print(f"📊 Checkpoints saved to: {output_dir}")

    return final_model_path

def main():
    print("\n" + "="*60)
    print("LOCAL MODEL TRAINING")
    print("="*60)

    # Load config
    config = load_config()

    # Load training data
    training_data = load_training_data()

    if len(training_data) < 10:
        print("\n⚠️  Not enough training data (need at least 10 examples)")
        print("   Run more learning cycles first!")
        return

    # Setup model and LoRA
    model, tokenizer = setup_model_and_lora(config)

    # Prepare dataset
    dataset = prepare_dataset(training_data, tokenizer)

    # Train
    model_path = train_model(model, tokenizer, dataset, config)

    print("\n" + "="*60)
    print("🎉 TRAINING COMPLETE!")
    print("="*60)
    print(f"\nYour AI is now smarter!")
    print(f"Trained on {len(training_data)} examples")
    print(f"\nTo use the trained model:")
    print(f"1. Update configs/config.yaml")
    print(f"2. Set base_model to: '{model_path}'")
    print(f"3. Run the AI in interactive mode")
    print("\n")

if __name__ == "__main__":
    main()
