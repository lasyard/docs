from beam import function
import subprocess


@function(gpu="T4")
def is_gpu_available():
    print(subprocess.check_output(["nvidia-smi"]).decode())
    print("This code is running on a remote GPU!")


if __name__ == "__main__":
    is_gpu_available.remote()
