# lame

<https://lame.sourceforge.io/>

## Install

::::{plat} macos
:vers: macOS Monterey

```sh
brew install lame
```

Check the version:

:::{literalinclude} /_files/macos/console/lame/version.txt
:language: console
:::

::::

## Usage

### Wave to MP3

```sh
lame -b 320 "audio.wav" "audio.mp3"
```
