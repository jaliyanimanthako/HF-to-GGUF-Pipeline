import subprocess
from typing import Optional

"""
This script automates the process of converting a Hugging Face (HF) transformer model into the GGUF format used by llama.cpp, and optionally applies quantization to reduce the model size for faster inference and lower resource usage.

Here's a breakdown of what this script does:

1. **Argument Parsing**:
   - Uses `argparse` to collect required and optional inputs from the user.
   - `--hf_model`: Path or model ID of the Hugging Face model to convert.
   - `--gguf_output`: Path where the resulting GGUF file will be saved.
   - `--quantized_output`: Path to save the quantized GGUF (optional).
   - `--quant_type`: Type of quantization (e.g., Q4_0, Q8_0). If not provided, quantization is skipped.
   - `--quant_algo`: Quantization algorithm parameter (defaults to "8").

2. **Model Conversion**:
   - Constructs a command to run `convert_hf_to_gguf.py` from within the `llama.cpp` directory.
   - This script takes a Hugging Face model and converts it into GGUF format, suitable for use with the llama.cpp runtime.

3. **Optional Quantization**:
   - If both `quant_type` and `quantized_output` are specified, the script runs the `llama-quantize` binary to quantize the converted GGUF model.
   - Quantization helps in reducing the size and memory footprint of the model, often with minimal loss in accuracy depending on the type.

This script is useful for anyone working with transformer models who wants to quickly transition from a Hugging Face model to a format compatible with lightweight llama.cpp inference environments — particularly when operating in constrained computing environments where quantization offers significant advantages.
"""


def convert_model(
    hf_model: str,
    gguf_output: str,
    quantized_output: Optional[str] = None,
    quant_type: Optional[str] = None,
    quant_algo: str = "8"
):
    # Convert HF to GGUF
    convert_command = [
        "python",
        "llama.cpp/convert_hf_to_gguf.py",
        hf_model,
        "--outfile",
        gguf_output
    ]

    try:
        print("Converting HuggingFace model to GGUF...")
        subprocess.run(convert_command, check=True)

        # Quantize (only if quant_type and quantized_output are provided)
        if quant_type and quantized_output:
            quantize_command = [
                "llama.cpp/build/bin/llama-quantize",
                gguf_output,
                quantized_output,
                quant_type,
                quant_algo
            ]
            print(f"Quantizing GGUF using {quant_type}...")
            subprocess.run(quantize_command, check=True)
        else:
            print("Quantization skipped — raw GGUF saved.")

        print("Conversion completed.")

    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        raise


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Convert HF model to GGUF, optionally quantize.")
    parser.add_argument("--hf_model", required=True, help="HuggingFace model path or ID")
    parser.add_argument("--gguf_output", required=True, help="Path to save the GGUF file")
    parser.add_argument("--quantized_output", help="Path to save quantized GGUF file (if quantizing)")
    parser.add_argument("--quant_type", help="Quantization type (e.g., Q8_0). Leave empty to skip quant.")
    parser.add_argument("--quant_algo", default="8", help="Quantization algorithm (default: 8)")

    args = parser.parse_args()

    convert_model(
        hf_model=args.hf_model,
        gguf_output=args.gguf_output,
        quantized_output=args.quantized_output,
        quant_type=args.quant_type,
        quant_algo=args.quant_algo
    )


if __name__ == "__main__":
    main()
