import os
from datasets import load_dataset
from transformers import AutoTokenizer

def load_and_prepare_data(model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
    print("Loading Alpaca dataset...")
    # Load the Alpaca dataset
    dataset = load_dataset("tatsu-lab/alpaca")
    
    print(f"Loading tokenizer for {model_id}...")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    # Ensure pad token is set (TinyLlama and Qwen might need this)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    def generate_prompt(data_point):
        """Formats the data point into the instruction format."""
        if data_point["input"]:
            return f"### Instruction:\n{data_point['instruction']}\n\n### Input:\n{data_point['input']}\n\n### Response:\n{data_point['output']}"
        else:
            return f"### Instruction:\n{data_point['instruction']}\n\n### Response:\n{data_point['output']}"

    def process_dataset(data_point):
        prompt = generate_prompt(data_point)
        # Tokenize the prompt
        tokenized = tokenizer(
            prompt,
            truncation=True,
            max_length=512, # Kept short for local laptop memory constraints
            padding="max_length"
        )
        tokenized["labels"] = tokenized["input_ids"].copy()
        return tokenized

    print("Formatting and tokenizing dataset...")
    # Use a small subset for CPU-only training (full dataset is 52k which is too slow on CPU)
    train_data = dataset['train'].select(range(1000))
    tokenized_dataset = train_data.map(process_dataset, remove_columns=train_data.column_names)
    
    # Split into train and eval
    split_dataset = tokenized_dataset.train_test_split(test_size=0.1, seed=42)
    
    print(f"Train dataset size: {len(split_dataset['train'])}")
    print(f"Test dataset size: {len(split_dataset['test'])}")
    
    return split_dataset, tokenizer

if __name__ == "__main__":
    split_dataset, tokenizer = load_and_prepare_data()
    print("Sample prompt decoded:")
    sample = split_dataset["train"][0]
    print(tokenizer.decode(sample["input_ids"][:50]))
    print("Data preparation complete!")
