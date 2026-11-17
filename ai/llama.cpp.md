# llama.cpp

<https://github.com/ggml-org/llama.cpp>

## Install

:::::{tab-set}
::::{tab-item} macOS
:sync: macos

```console
$ brew install llama.cpp
```

The app downloaded from <https://llama.app/> is more like a front end for macOS, which can install `llama.cpp` and download models as needed.

::::
:::::

## Usage

As simple as:

```console
$ llama serve
0.00.001.234 I srv  llama_server: initializing ...
0.00.120.491 I cmn  common_param: common_params_print_info: verbosity = 3 (adjust with the `-lv N` CLI arg)
0.00.147.080 I srv    operator(): Available models (1):
0.00.147.083 I srv    operator():   [     cache] TheDrummer/Cydonia-24B-v4.3-GGUF:Q4_K_M
0.00.147.119 W srv  llama_server: security: no API key is set and CORS allows all origins (see https://github.com/ggml-org/llama.cpp/pull/25655)
0.00.147.124 W srv  llama_server: security: router mode enabled - do not expose to untrusted environments
0.00.147.125 I srv  llama_server: starting server in router mode. models will be automatically loaded on-demand
0.00.148.545 I srv  llama_server: listening on http://127.0.0.1:9931
...
```

The command will serve the models in cache, loading as needed.

Show models in cache:

```console
$ llama serve --cache-list
number of models in cache: 1
   1. TheDrummer/Cydonia-24B-v4.3-GGUF:Q4_K_M
```

The cache dir is `~/.cache/huggingface/hub`.

If there's more than 1 models, better to restrict the number of loaded models:

```console
$ llama serve --models-max 1
```

If you want to serve a specified model:

```console
$ llama serve -m ./Cydonia-24B-v4zg-Q4_K_M.gguf -ngl 99 -c 16384 -fa on
```
