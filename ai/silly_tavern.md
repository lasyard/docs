# SillyTavern

<https://sillytavern.app/>

## Install and run

```console
$ git clone https://github.com/SillyTavern/SillyTavern -b release
$ cd SillyTavern
$ ./start.sh
...
SillyTavern 1.19.0
Running 'release' (06bde939f) - 9/15/2026, 3:01:34 AM GMT+8


Compiling frontend libraries...
webpack 5.105.4 compiled successfully in 241 ms

Launching in a browser: default...
SillyTavern is listening on IPv4: 127.0.0.1:8000

=================================================

Go to: http://127.0.0.1:8000/ to open SillyTavern

=================================================
...
```

## Config

The default config file:

:::{literalinclude} /_files/macos/workspace/silly_tarvern/config.yaml
:::

## Models

Using <project:llama.cpp.md> to run the GGUF models.

| HuggingFace Model                       | SillyTavern Template |
| :-------------------------------------- | :------------------- |
| TheDrummer/Rocinante-X-12B-v1-GGUF:Q8_0 | Mistral V3-Tekken    |
| bartowski/L3-8B-Stheno-v3.2-GGUF:Q8_0   | Llama 3 Instruct     |
| bartowski/MN-12B-Mag-Mell-R1-GGUF:Q8_0  | ChatML               |
