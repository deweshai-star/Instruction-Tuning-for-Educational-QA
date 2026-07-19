# Presenter Notes: Instruction Tuning for Educational QA

This document provides page-by-page talking points (reading notes) for presenting your slides. Use these notes to guide your narrative, highlight key metrics, and explain technical details smoothly.

---

## Slide 1: Title Slide
**Slide Title**: Instruction Tuning for Educational QA
**Focus**: Project Introduction, Context, & Main Goal

### What to say:
* *"Good morning/afternoon everyone. Today, I am presenting my project on **Instruction Tuning for Educational QA**."*
* *"The goal of this project is to address a common bottleneck in deploying Generative AI in classroom settings: **compute constraints**."*
* *"While state-of-the-art Large Language Models (LLMs) perform exceptionally well, they require massive, expensive GPU setups. In this project, I have fine-tuned a lightweight LLM—specifically **TinyLlama 1.1B**—using parameter-efficient techniques, allowing us to train and run a domain-specific educational assistant directly on standard consumer CPUs (like a student or teacher's laptop), with zero cloud cost."*

---

## Slide 2: End-to-End Development Pipeline
**Slide Title**: End-to-End Development Pipeline
**Focus**: Explaining the 4-Stage Workflow (Data -> Model -> CPU Training -> Streamlit App)

### What to say:
* *"Here, we see the end-to-end architecture of our project, broken down into four core stages."*
* *"(Stage 1) **Data Engineering**: We begin with the gold-standard **Alpaca dataset** from Stanford. We filter a subset of 1,000 instruction-following samples, split them into 900 training and 100 evaluation pairs, and format them into structured prompts with `### Instruction`, `### Input` (if applicable), and `### Response` templates. We tokenize them using the LLaMA tokenizer with a max length of 512 to constrain memory."*
* *"(Stage 2) **Model Adaptation**: We load the pre-trained **TinyLlama 1.1B** decoder-only model. To make fine-tuning feasible on a laptop, we use **LoRA (Low-Rank Adaptation)** to target only the Query (`q_proj`) and Value (`v_proj`) projection matrices in the self-attention layer."*
* *"(Stage 3) **CPU-Optimized Training**: We configure PyTorch to train entirely on CPU in **float32 precision**. We optimize memory usage via **Gradient Checkpointing** and use a tiny batch size of 1 with gradient accumulation of 4 steps to simulate an effective batch size of 4."*
* *"(Stage 4) **Local Deployment**: The output is a tiny set of adapter weights (~4.5MB). We wrapped this in a **Streamlit application (`app.py`)** that automatically loads the base model and overlays our adapters to answer student queries locally."*

---

## Slide 3: Methodology (PEFT & LoRA)
**Slide Title**: Methodology: Low-Rank Adaptation (LoRA)
**Focus**: Why we use LoRA & The Math/Param Reduction

### What to say:
* *"Let's dive into the core methodology: **Why PEFT and LoRA?**"*
* *"If we perform **Full Parameter Tuning** (on the left), we would have to update all **1.1 Billion parameters** of TinyLlama. This means updating massive matrices of gradients and optimizer states, which requires over **24 GB of GPU VRAM** to train in float32. This is completely impossible on commodity CPUs or standard laptops."*
* *"To solve this, we use **Low-Rank Adaptation (LoRA)** (on the right). Instead of modifying the massive base weights, we freeze them. We then inject two small, low-rank matrices ($A$ and $B$) alongside the key projection layers."*
* *"By choosing a rank ($r$) of 8 and alpha of 16, we compress the updates. Out of the 1.1 Billion parameters, **only 1,126,400 parameters** are trainable. That is just **0.1% of the model**."*
* *"Because we are updating only 1.1M parameters, the training memory footprint drops by over 99%, and our final saved adapter file size is just **4.5 MB**."*

---

## Slide 4: Training & System Configuration
**Slide Title**: Training Configuration & Loss Performance
**Focus**: Hardware constraints & Training loss progression

### What to say:
* *"Next, let's look at the training execution details and performance metrics."*
* *"To simulate a real-world local training setup, we forced the trainer onto **CPU only** (`use_cpu=True`) using standard **float32 precision**. The peak RAM consumption was around **6 GB**, meaning it fits comfortably within standard modern laptops."*
* *"On the right, you can see the empirical training loss from our `trainer_state.json` logs over 25 steps:"*
  * *"At step 5, the loss starts at **1.89**."*
  * *"By step 10, it drops to **1.80**."*
  * *"At step 20, it reaches its lowest point of **1.43** before stabilizing around **1.52** at step 25."*
* *"This consistent downward trend confirms that the model is successfully learning to follow the instruction-response format, adapting its generation style to be more concise and educational."*

---

## Slide 5: Results & Classroom Deployment
**Slide Title**: Results & Classroom Deployment
**Focus**: Streamlit app walkthrough & Sample output

### What to say:
* *"Finally, let's look at the results and how this works in practice."*
* *"We built a frontend using **Streamlit** to make the model accessible to non-technical users. The app has a smart load-and-fallback logic: it automatically scans for fine-tuned LoRA adapters (looking for `final-adapter/` or `checkpoint-25/`). If found, it overlays them. If not, it falls back to the base model, guaranteeing the application always runs."*
* *"Let's look at the output comparison on the right. When we prompt the model with: **'Explain the process of photosynthesis to a middle school student.'**, the fine-tuned model produces a highly structured response."*
* *"Instead of giving a dry, overly academic explanation, it explains the Calvin cycle, the role of chlorophyll, and breaks it down into simple terms: 'Plants use solar energy, water, and air to make their own food and release clean air for us to breathe!'"*
* *"This shows that even a lightweight model of 1.1 Billion parameters can become a highly effective, private, offline teaching assistant running entirely on local CPU hardware."*
* *"Thank you, and I am happy to take any questions."*
