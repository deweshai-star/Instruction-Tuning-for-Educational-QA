# Presenter Notes: Instruction Tuning for Educational QA (8-Slide Version)

This document provides page-by-page talking points (reading notes) for presenting the updated, improved slide deck.

---

## Slide 1: Topic (Title Slide)
**Slide Title**: Instruction Tuning for Educational QA
**Focus**: Project Introduction, Context, & Main Goal

### Talking Points:
* *"Good morning/afternoon everyone. Today, I am presenting my project: **Instruction Tuning for Educational QA**."*
* *"This project addresses a major constraint in modern generative AI deployment: the high cost and computational footprint of running Large Language Models (LLMs)."*
* *"By applying Parameter-Efficient Fine-Tuning (PEFT) with LoRA, we train a lightweight model—**TinyLlama 1.1B**—to serve as a domain-specific educational question-answering assistant that can be trained and run completely offline, locally on standard consumer CPUs."*

---

## Slide 2: Project Objectives
**Slide Title**: Project Objectives
**Focus**: Key Motivations (CPU Training, Classroom Assistant, Privacy)

### Talking Points:
* *"Let's establish our core objectives."*
* *"First, **CPU-Only Accessibility**. Standard LLM training requires expensive, enterprise-grade GPUs. We wanted to design a pipeline that trains and runs on a standard laptop with about 6 GB of RAM, democratizing access to customized model building."*
* *"Second, **Classroom-Ready Assistance**. Standard models often generate overly academic or long-winded answers. Our objective is to fine-tune the model to give concise, structured, student-friendly responses."*
* *"Third, **Privacy & Offline Support**. Many schools have limited internet or strict regulations regarding student data. A fully offline application ensures complete privacy with zero cloud bills."*

---

## Slide 3: Dataset & Preparation
**Slide Title**: Alpaca Instruction Dataset
**Focus**: Stanford Alpaca, Subset Split, Prompt Template

### Talking Points:
* *"Now, let's discuss our dataset and preprocessing pipeline."*
* *"We utilize Stanford's **Alpaca dataset**, which is released under the Creative Commons license. While the full dataset contains over 52,000 samples, we extracted a curated subset of **1,000 instruction-following samples** to stay within laptop CPU resource constraints."*
* *"We split this subset into **900 training samples** and **100 evaluation samples**."*
* *"On the right, you can see how data points are engineered. Each sample is parsed into a structured prompt using tags: `### Instruction`, an optional `### Input` context box, and a `### Response`. We tokenize these prompts using the LLaMA tokenizer with a strict max length of 512 tokens to conserve memory."*

---

## Slide 4: Workflow & Architecture
**Slide Title**: End-to-End Workflow & System Architecture
**Focus**: 4-Stage Architecture Flow

### Talking Points:
* *"Here is the end-to-end system architecture of our pipeline, split into four linear steps."*
* *"First, **Data Prep**: We download the subset, apply our instruction prompt wrapper, and pad/truncate the tokenized input."*
* *"Second, **PEFT Configuration**: We load the base TinyLlama 1.1B model and freeze 99.9% of its parameters. We inject trainable Low-Rank matrices (with rank $r=8$, alpha $=16$) into the query and value attention projection modules."*
* *"Third, **CPU-Only Training**: We pass our configured model and data to the PyTorch CPU trainer using float32 precision, gradient checkpointing, and an effective batch size of 4 via gradient accumulation."*
* *"Fourth, **Local Web UI**: Once training concludes, we save the lightweight adapters (~4.5MB). We load them inside a local Streamlit browser interface (`app.py`), which reads user input and runs real-time inference on the CPU."*

---

## Slide 5: Challenges & Solutions
**Slide Title**: Development Challenges & Key Solutions
**Focus**: Overcoming Memory Limits & Path Resolution Crashes

### Talking Points:
* *"During development, we faced two critical challenges."*
* *"The first challenge was **Severe CPU Memory Constraints**. Loading a 1.1B model and running backpropagation can easily crash a consumer laptop. We solved this by enabling gradient checkpointing to discard intermediate activations, using LoRA to reduce trainable parameters to just 0.1%, and using a small batch size of 1 with gradient accumulation."*
* *"The second challenge was **Path Resolution and Fallback Crashes**. If the final adapter directory was missing, the Hugging Face library would try to find it online and crash. To fix this, we refactored the loading logic in `app.py` and `inference.py` to recursively search for local checkpoints (like `checkpoint-25/`) and, if no adapter is found, gracefully fall back to the base model instead of crashing."*

---

## Slide 6: Empirical Results & Conclusion
**Slide Title**: Empirical Results & Conclusion
**Focus**: Loss Convergence Table & Project Takeaways

### Talking Points:
* *"Next, let's look at our empirical results."*
* *"On the left is the loss convergence table from our `trainer_state.json` logs. Over the 25 training steps:"*
  * *"Step 5 started with a training loss of **1.8983**."*
  * *"By Step 15, the loss dropped to **1.6545**."*
  * *"And by Step 25, it successfully converged to **1.5245**."*
* *"This steady decrease in loss proves that the model successfully learned the instruction-following patterns."*
* *"In conclusion, this project proves that CPU-only instruction tuning is highly feasible, cost-effective, offline-ready, and lightweight—saving only 4.5 MB of adapter weights."*

---

## Slide 7: Future Directions
**Slide Title**: Future Directions
**Focus**: Dataset Scaling, Quantization, and RAG

### Talking Points:
* *"Looking ahead, there are three primary future directions we want to explore."*
* *"First, **Scale Dataset & Context Length**: We plan to increase our training subset to over 10,000 samples and expand our context length to 2048 tokens to support analyzing complete textbook chapters."*
* *"Second, **Quantized Larger Models**: We want to experiment with larger open-source models like Qwen-2.5-7B or Gemma-2-9B, using 4-bit or 8-bit CPU quantization libraries like llama.cpp to keep them running efficiently on consumer laptops."*
* *"Third, **RAG Syllabus Integration**: We plan to implement Retrieval-Augmented Generation, allowing teachers to upload specific syllabus PDFs locally so the model can ground its answers in classroom material, eliminating hallucinations."*

---

## Slide 8: GitHub & Repository Details
**Slide Title**: GitHub Repository & Setup Details
**Focus**: Git URL, Setup guide, File structure

### Talking Points:
* *"Finally, all code and models are open-sourced."*
* *"The repository is hosted at the URL shown on the left: `https://github.com/deweshai-star/Instruction-Tuning-for-Educational-QA`."*
* *"To set up the project on any standard machine, users only need to run three simple steps:"*
  1. *"Clone the repo."*
  2. *"Create a virtual environment and run `pip install -r requirements.txt`."*
  3. *"Start the web application with `streamlit run app.py`."*
* *"On the right is our project's file structure. It contains self-contained modules: `data_prep.py` for preprocessing, `train.py` for model tuning, `inference.py` for command-line testing, and `app.py` for the Streamlit web GUI."*
* *"Thank you very much. I am now open to any questions."*
