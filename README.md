# 🦙 llama.cpp Automation Toolkit

This repository contains a set of automation scripts to streamline the setup, build, conversion, and optional quantization process for [llama.cpp](https://github.com/ggerganov/llama.cpp), a C++ inference engine for LLaMA-based models.

---

## 📂 Contents

- `setup_llama_cpp.py`  
  Clones the `llama.cpp` repo, initializes submodules, configures the build using CMake and Ninja, compiles the project using parallel jobs, and sets up a Python virtual environment.

- `convert_and_quantize.py`  
  Converts a Hugging Face model to GGUF format and optionally quantizes it using the compiled `llama-quantize` binary.

---

## 🛠️ Prerequisites

- Python 3.8+
- Git
- CMake
- Ninja
- A C++ compiler (e.g., `g++`)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
- Python `virtualenv` module

Install required tools (Ubuntu example):

```bash
sudo apt update
sudo apt install git cmake ninja-build g++ python3-venv
```

---

## 🚀 Usage

### 1. Setup llama.cpp

Run the setup script with the desired number of parallel build jobs:

```bash
python setup_llama_cpp.py -j 8
```

This script will:

- Clone the `llama.cpp` repository (if not already cloned)
- Initialize submodules
- Configure and build the project with Ninja
- Create a Python virtual environment and install required dependencies

After completion, activate the virtual environment:

```bash
source ~/llama-cpp-venv/bin/activate
```

---

### 2. Convert and (optionally) Quantize a Hugging Face Model

```bash
python convert_and_quantize.py \
  --hf_model TheBloke/LLaMA-2-7B-GGUF \
  --gguf_output llama-2-7b.gguf \
  --quantized_output llama-2-7b-q8.gguf \
  --quant_type Q8_0
```

- To **skip quantization**, just leave out `--quantized_output` and `--quant_type`.

---

## 🧪 Example

Convert without quantization:

```bash
python convert_and_quantize.py \
  --hf_model meta-llama/Llama-2-7b-hf \
  --gguf_output llama-2-7b.gguf
```

Convert *with* quantization:

```bash
python convert_and_quantize.py \
  --hf_model meta-llama/Llama-2-7b-hf \
  --gguf_output llama-2-7b.gguf \
  --quantized_output llama-2-7b-q4.gguf \
  --quant_type Q4_0
```

---

## 📁 Directory Structure

```
.
├── llama.cpp/              # Cloned repo
├── setup_llama_cpp.py      # Setup and build script
├── convert_and_quantize.py # Conversion and quantization script
├── requirenments.py        # Should contain `create_virtualenv()` function
└── README.md               # You're here
```

---

## ✨ Credits

- [`llama.cpp`](https://github.com/ggerganov/llama.cpp) by Georgi Gerganov
- Scripts authored and maintained by [Your Name](https://github.com/your-profile)

---

## 📄 License

MIT License