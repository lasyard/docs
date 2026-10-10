# HuggingFace

<https://huggingface.co/>

## Install

```console
$ pip install -U huggingface_hub
```

## Usage

```console
$ hf download bartowski/Rocinante-12B-v1.1-GGUF Rocinante-12B-v1.1-Q8_0.gguf
...
✓ Downloaded
  path: /Users/xxxx/.cache/huggingface/hub/models--bartowski--Rocinante-12B-v1.1-GGUF/snapshots/9d15ca24c675a428fc5821cccc537f2a6f64987d/Rocinante-12B-v1.1-Q8_0.gguf
```

You can download a model to a specified dir by `--local-dir /path/to/dir`. Note there will be a `.cache` dir generated in it.
