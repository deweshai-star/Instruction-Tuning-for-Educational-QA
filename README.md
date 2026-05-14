# Instruction Tuning for Educational QA

Fine-tune a lightweight LLM (TinyLlama 1.1B) using the **Alpaca instruction-following dataset** to build an Educational Question Answering system. Uses **LoRA (Low-Rank Adaptation)** for parameter-efficient training, making it feasible to run on a standard laptop without a GPU.

## Features

- **Lightweight Model**: Uses TinyLlama 1.1B — only 1.1 billion parameters
- **Efficient Training**: LoRA fine-tunes only ~0.1% of parameters (~1.1M out of 1.1B)
- **CPU Compatible**: Fully optimized for CPU-only machines (no GPU required)
- **Educational QA**: Trained on instruction-following data to answer educational questions
- **HuggingFace Ecosystem**: Built with `transformers`, `peft`, and `datasets`

## Dataset

**Alpaca Dataset** — [tatsu-lab/alpaca](https://huggingface.co/datasets/tatsu-lab/alpaca)

| Property        | Value    |
|-----------------|----------|
| Total Samples   | 52,002   |
| Subset Used     | 1,000    |
| Train / Test    | 900 / 100|
| Format          | Instruction → Input → Response |

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/deweshai-star/Instruction-Tuning-for-Educational-QA.git
cd Instruction-Tuning-for-Educational-QA
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note (Windows):** If you face issues with `bitsandbytes`, you can safely ignore it — the CPU training pipeline does not use it.

### 4. Prepare the Data

Downloads the Alpaca dataset from HuggingFace, formats it into instruction prompts, and tokenizes it.

```bash
python data_prep.py
```

**Expected output:**
```
Loading Alpaca dataset...
Loading tokenizer for TinyLlama/TinyLlama-1.1B-Chat-v1.0...
Formatting and tokenizing dataset...
Train dataset size: 900
Test dataset size: 100
Data preparation complete!
```

### 5. Train the Model

Loads TinyLlama, applies LoRA adapters, and trains for 50 steps on the prepared dataset.

```bash
python train.py
```

**Expected output:**
```
Preparing data...
Loading model TinyLlama/TinyLlama-1.1B-Chat-v1.0...
Configuring LoRA...
trainable params: 1,126,400 || all params: 1,101,174,784 || trainable%: 0.1023
Starting training (CPU mode)...
{'loss': 2.3456, 'step': 5}
{'loss': 2.1234, 'step': 10}
...
Training complete!
```

The trained LoRA adapter weights are saved to `./results-educational-tuning/final-adapter/`.

### 6. Run Inference

Test the fine-tuned model with educational questions.

```bash
python inference.py
```

**Expected output:**
```
Welcome to the Educational QA Inference Tester!
Loading base model: TinyLlama/TinyLlama-1.1B-Chat-v1.0...
Loading fine-tuned adapters...
Adapters loaded successfully.

--- Generating Response ---
Instruction: Explain the process of photosynthesis to a middle school student.
Generated Answer: Photosynthesis is the process by which plants convert sunlight...
```

## Project Structure

```
├── data_prep.py          # Data loading, formatting, tokenization
├── train.py              # Model loading, LoRA config, training loop
├── inference.py          # Load adapters and generate answers
├── requirements.txt      # Python dependencies
├── architecture.md       # Detailed system architecture
└── README.md             # This file
```

## Architecture

See [architecture.md](architecture.md) for a detailed breakdown of the pipeline, model architecture, LoRA configuration, and training strategy.

## Requirements

- Python 3.10+
- ~6 GB RAM (for loading model in float32)
- No GPU required (CPU training supported)
- Internet connection (first run downloads the model and dataset)

## License

This project uses the Alpaca dataset which is released under the [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) license.
