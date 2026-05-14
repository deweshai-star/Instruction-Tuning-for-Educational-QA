import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model
from data_prep import load_and_prepare_data

def train_model():
    # We choose TinyLlama as it is very lightweight (1.1B parameters)
    model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    output_dir = "./results-educational-tuning"
    
    # 1. Load Data
    print("Preparing data...")
    dataset, tokenizer = load_and_prepare_data(model_id)
    
    # 2. Load Model (CPU-friendly: no quantization, use float32)
    print(f"Loading model {model_id}...")
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float32,
        device_map="cpu"
    )
    
    # Enable gradient checkpointing to reduce memory usage
    model.gradient_checkpointing_enable()
    
    # 3. Configure LoRA (Low-Rank Adaptation)
    # Only a tiny fraction of parameters are trained, making it feasible on CPU
    print("Configuring LoRA...")
    peft_config = LoraConfig(
        r=8,             # Rank (low = fewer trainable params = faster)
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],  # Only 2 modules to keep it fast
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()
    
    # 4. Training Arguments — Optimized for CPU
    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=1,   # Minimal batch size for CPU memory
        gradient_accumulation_steps=4,   # Effective batch size = 4
        optim="adamw_torch",            # Standard optimizer (paged_adamw needs GPU)
        logging_steps=5,
        learning_rate=2e-4,
        fp16=False,                     # CPU doesn't support fp16 training well
        bf16=False,
        max_grad_norm=0.3,
        max_steps=50,                   # Short run for CPU demo (increase for better results)
        warmup_steps=5,
        lr_scheduler_type="constant",
        save_strategy="steps",
        save_steps=25,
        use_cpu=True,                   # Force CPU
        dataloader_pin_memory=False,    # Not needed on CPU
    )
    
    # 5. Initialize Trainer
    print("Initializing Trainer...")
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    
    trainer = Trainer(
        model=model,
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"],
        args=training_args,
        data_collator=data_collator,
    )
    
    # 6. Start Training
    print("Starting training (CPU mode — this will take some time)...")
    trainer.train()
    
    # 7. Save the final model (adapters only)
    print("Saving trained adapters...")
    trainer.model.save_pretrained(f"{output_dir}/final-adapter")
    tokenizer.save_pretrained(f"{output_dir}/final-adapter")
    print("Training complete!")

if __name__ == "__main__":
    train_model()
