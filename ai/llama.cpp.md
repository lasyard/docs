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
0.00.000.615 I srv  llama_server: initializing ...
0.00.099.259 I cmn  common_param: common_params_print_info: verbosity = 3 (adjust with the `-lv N` CLI arg)
0.00.129.090 I srv    operator(): Available models (1):
0.00.129.094 I srv    operator():   [     cache] bartowski/Rocinante-12B-v1.1-GGUF:Q8_0
0.00.129.142 W srv  llama_server: security: no API key is set and CORS allows all origins (see https://github.com/ggml-org/llama.cpp/pull/25655)
0.00.129.328 W srv  llama_server: security: router mode enabled - do not expose to untrusted environments
0.00.129.329 I srv  llama_server: starting server in router mode. models will be automatically loaded on-demand
0.00.131.124 I srv  llama_server: listening on http://127.0.0.1:8080
0.00.131.128 W srv  llama_server: notice: server default port will be changed to :9931 in a future release (ref: https://github.com/ggml-org/llama.cpp/pull/26508)
...
```

The command will serve the models in cache, loading as needed.

Show models in cache:

```console
$ llama serve --cache-list 
number of models in cache: 1
   1. bartowski/Rocinante-12B-v1.1-GGUF:Q8_0
```

The cache dir is `~/.cache/huggingface/hub`.

If there's more than 1 models, better to restrict the number of loaded models:

```console
$ llama serve --models-max 1
```

If you want to serve a specified model:

```console
$ llama serve -m ./Rocinante-12B-v1.1-Q8_0.gguf -ngl 99 -c 16384 -fa on
```
