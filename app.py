import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import os

st.set_page_config(page_title="Educational QA Model", page_icon="🎓", layout="centered")

@st.cache_resource
def load_model():
    base_model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    # Fallback to checkpoint-25 if final-adapter isn't available
    adapter_path = "./results-educational-tuning/final-adapter"
    if not os.path.exists(adapter_path):
        adapter_path = "./results-educational-tuning/checkpoint-25"
        
    tokenizer = AutoTokenizer.from_pretrained(adapter_path if os.path.exists(adapter_path) else base_model_id)
    
    # Load base model
    model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        torch_dtype=torch.float32,
        device_map="cpu"
    )
    
    # Load adapters if they exist
    if os.path.exists(adapter_path):
        model = PeftModel.from_pretrained(model, adapter_path)
        st.sidebar.success(f"Loaded fine-tuned adapters from: {adapter_path}")
    else:
        st.sidebar.warning("No fine-tuned adapters found. Using base model.")
        
    return model, tokenizer

st.title("🎓 Educational QA Model")
st.markdown("Ask educational questions and the instruction-tuned TinyLlama model will answer them!")

with st.spinner("Loading model... (this may take a minute on CPU)"):
    model, tokenizer = load_model()

instruction = st.text_area("Question / Instruction:", placeholder="Explain the process of photosynthesis to a middle school student.")
input_text = st.text_input("Additional Context (Optional):", placeholder="")

if st.button("Generate Answer"):
    if instruction:
        with st.spinner("Generating response..."):
            # Format the prompt
            if input_text:
                prompt = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n"
            else:
                prompt = f"### Instruction:\n{instruction}\n\n### Response:\n"
                
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=256,
                    temperature=0.7,
                    top_p=0.9,
                    repetition_penalty=1.1,
                    do_sample=True
                )
                
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            final_output = response.split("### Response:\n")[-1].strip()
            
            st.markdown("### Answer:")
            st.info(final_output)
    else:
        st.warning("Please enter a question or instruction.")
