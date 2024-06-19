# lame

<https://lame.sourceforge.io/>

LAME is a high quality MPEG Audio Layer III (MP3) encoder licensed under the LGPL.

## Install

:::{include} /_frags/plats/macos.txt
:::

```sh
brew install lame
```

```sh
lame --version
```

:::{literalinclude} /_files/macos/output/lame/version.txt
:language: text
:class: cli-output
:::

## Usage

### Wave to MP3

```sh
lame -b 320 "audio.wav" "audio.mp3"
```
