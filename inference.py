import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import os

def generate_response(instruction, input_text=""):
    # Base model and adapter paths
    base_model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    adapter_path = "./results-educational-tuning/final-adapter"
    if not os.path.exists(adapter_path):
        adapter_path = "./results-educational-tuning/checkpoint-25"
        
    print(f"Loading base model: {base_model_id}...")
    tokenizer = AutoTokenizer.from_pretrained(adapter_path if os.path.exists(adapter_path) else base_model_id)
    
    # Load on CPU with float32
    model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        torch_dtype=torch.float32,
        device_map="cpu"
    )
    
    # Load adapters if they exist
    if os.path.exists(adapter_path):
        print(f"Loading fine-tuned adapters from {adapter_path}...")
        try:
            model = PeftModel.from_pretrained(model, adapter_path)
            print("Adapters loaded successfully.")
        except Exception as e:
            print(f"Could not load adapters: {e}")
            print("Running base model for comparison instead.")
    else:
        print("No fine-tuned adapters found. Running base model.")
        
    # Format the prompt
    if input_text:
        prompt = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n"
    else:
        prompt = f"### Instruction:\n{instruction}\n\n### Response:\n"
        
    print("\n--- Generating Response ---")
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    # Generate output
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1,
            do_sample=True
        )
        
    # Decode and print
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Extract only the response part
    final_output = response.split("### Response:\n")[-1]
    
    print(f"\nInstruction: {instruction}")
    if input_text:
        print(f"Input: {input_text}")
    print(f"\nGenerated Answer: {final_output}\n")

if __name__ == "__main__":
    print("Welcome to the Educational QA Inference Tester!")
    instruction = "Explain the process of photosynthesis to a middle school student."
    input_text = ""
    
    generate_response(instruction, input_text)
    
    # Uncomment to enable interactive testing
    # while True:
    #     user_inst = input("Enter an instruction (or 'q' to quit): ")
    #     if user_inst.lower() == 'q': break
    #     user_input = input("Enter input context (optional): ")
    #     generate_response(user_inst, user_input)
