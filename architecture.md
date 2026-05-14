# Architecture: Instruction Tuning for Educational QA

## Overview

This project fine-tunes a pre-trained Large Language Model (LLM) using the **Alpaca instruction-following dataset** to create an Educational Question Answering system. The pipeline uses **Parameter-Efficient Fine-Tuning (PEFT)** with **LoRA (Low-Rank Adaptation)** to make training feasible on consumer-grade hardware (CPU-only laptops).

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA PIPELINE                            │
│                                                             │
│  ┌──────────────┐    ┌────────────────┐    ┌─────────────┐  │
│  │ Alpaca       │───▶│ Prompt         │───▶│ Tokenized   │  │
│  │ Dataset      │    │ Formatting     │    │ Dataset     │  │
│  │ (HuggingFace)│    │ (Instruction/  │    │ (train/test │  │
│  │              │    │  Input/Output) │    │  split)     │  │
│  └──────────────┘    └────────────────┘    └─────────────┘  │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    MODEL LAYER                              │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              TinyLlama 1.1B (Base Model)             │   │
│  │                                                      │   │
│  │   ┌─────────┐  ┌─────────┐  ┌─────────┐             │   │
│  │   │ Frozen  │  │ Frozen  │  │ Frozen  │  ...         │   │
│  │   │ Layers  │  │ Layers  │  │ Layers  │              │   │
│  │   └────┬────┘  └────┬────┘  └────┬────┘              │   │
│  │        │             │            │                   │   │
│  │   ┌────▼────┐  ┌────▼────┐  ┌────▼────┐              │   │
│  │   │  LoRA   │  │  LoRA   │  │  LoRA   │  (Trainable) │   │
│  │   │ Adapter │  │ Adapter │  │ Adapter │              │   │
│  │   │ q_proj  │  │ v_proj  │  │  ...    │              │   │
│  │   └─────────┘  └─────────┘  └─────────┘              │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    TRAINING PIPELINE                        │
│                                                             │
│  ┌──────────────┐    ┌────────────────┐    ┌─────────────┐  │
│  │ HuggingFace  │───▶│ Causal LM      │───▶│ Trained     │  │
│  │ Trainer      │    │ Loss           │    │ LoRA        │  │
│  │ (AdamW)      │    │ (Next Token    │    │ Adapters    │  │
│  │              │    │  Prediction)   │    │ (.safetens) │  │
│  └──────────────┘    └────────────────┘    └─────────────┘  │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    INFERENCE PIPELINE                       │
│                                                             │
│  ┌──────────────┐    ┌────────────────┐    ┌─────────────┐  │
│  │ User         │───▶│ Base Model +   │───▶│ Educational │  │
│  │ Question     │    │ LoRA Adapters  │    │ Answer      │  │
│  │ (Prompt)     │    │ (Merged)       │    │ (Generated) │  │
│  └──────────────┘    └────────────────┘    └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Dataset — Alpaca (tatsu-lab/alpaca)

| Property       | Value                           |
|----------------|----------------------------------|
| Source          | `tatsu-lab/alpaca` on HuggingFace |
| Total Samples  | 52,002                           |
| Subset Used    | 1,000 (for CPU training)         |
| Train/Test     | 90% / 10% split                  |
| Fields          | `instruction`, `input`, `output` |

Each sample is formatted into a structured prompt:

```
### Instruction:
{instruction}

### Input:
{input}   ← (optional, omitted if empty)

### Response:
{output}
```

### 2. Base Model — TinyLlama 1.1B

| Property          | Value                              |
|-------------------|------------------------------------|
| Model             | `TinyLlama/TinyLlama-1.1B-Chat-v1.0` |
| Parameters        | 1.1 Billion                        |
| Architecture      | LLaMA (Decoder-only Transformer)   |
| Context Length     | 2048 tokens                        |
| Training Precision | float32 (CPU compatible)          |

**Why TinyLlama?** It is one of the smallest high-quality LLMs available, making it feasible to fine-tune and run inference on consumer hardware without a dedicated GPU.

### 3. Fine-Tuning Strategy — LoRA (Low-Rank Adaptation)

| Property            | Value        |
|---------------------|--------------|
| Method              | LoRA via PEFT |
| Rank (r)            | 8            |
| Alpha               | 16           |
| Target Modules      | `q_proj`, `v_proj` |
| Dropout             | 0.05         |
| Trainable Params    | ~1.1M (0.1% of total) |
| All Params          | ~1.1B        |

**Why LoRA?** Instead of updating all 1.1B parameters, LoRA injects small trainable matrices into specific attention layers. This reduces memory usage by ~99% and training time dramatically while still allowing the model to learn new behaviors.

### 4. Training Configuration

| Property                   | Value      |
|----------------------------|------------|
| Batch Size (per device)    | 1          |
| Gradient Accumulation      | 4 steps    |
| Effective Batch Size       | 4          |
| Optimizer                  | AdamW      |
| Learning Rate              | 2e-4       |
| Max Steps                  | 50         |
| Warmup Steps               | 5          |
| LR Scheduler               | Constant   |
| Max Sequence Length         | 512 tokens |
| Hardware                   | CPU only   |

## Technology Stack

| Component       | Library / Tool                              |
|-----------------|---------------------------------------------|
| Language        | Python 3.10+                                |
| Deep Learning   | PyTorch                                     |
| Transformers    | HuggingFace `transformers`                  |
| Dataset Loading | HuggingFace `datasets`                      |
| Fine-Tuning     | `peft` (LoRA), HuggingFace `Trainer`        |
| Tokenizer       | AutoTokenizer (LLaMA tokenizer)             |
| Model Hosting   | HuggingFace Hub                             |

## File Structure

```
Instruction Tuning for Educational QA/
├── data_prep.py          # Data loading, formatting, tokenization
├── train.py              # Model loading, LoRA config, training loop
├── inference.py          # Load adapters, generate educational answers
├── requirements.txt      # Python dependencies
├── architecture.md       # This file
├── README.md             # Setup and execution guide
└── results-educational-tuning/   # (generated after training)
    └── final-adapter/
        ├── adapter_model.safetensors
        └── adapter_config.json
```
