import subprocess
import sys


def check_python():
    print("[Python]")
    print(sys.version)


def check_torch():
    print("\n[PyTorch / CUDA]")

    try:
        import torch
    except ImportError:
        print("torch is not installed.")
        return

    print("torch version:", torch.__version__)
    print("torch cuda version:", torch.version.cuda)
    print("cuda available:", torch.cuda.is_available())

    if torch.cuda.is_available():
        print("gpu:", torch.cuda.get_device_name(0))
    else:
        print("gpu: CPU only")
        print("warning: LoRA training on CPU is not recommended.")


def check_nvidia_smi():
    print("\n[nvidia-smi]")

    try:
        result = subprocess.run(
            ["nvidia-smi"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            print(result.stdout)
        else:
            print("nvidia-smi command exists but failed.")
            print(result.stderr)

    except FileNotFoundError:
        print("nvidia-smi not found.")
        print("If this is WSL without local GPU, this is expected.")


def check_huggingface():
    print("\n[Hugging Face Auth]")

    try:
        result = subprocess.run(
            ["hf", "auth", "whoami"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Hugging Face login not confirmed.")
            print(result.stderr)
            print("Run: hf auth login")

    except FileNotFoundError:
        print("hf command not found.")
        print("Install huggingface_hub or check requirements-train.txt.")


def main():
    check_python()
    check_torch()
    check_nvidia_smi()
    check_huggingface()


if __name__ == "__main__":
    main()
