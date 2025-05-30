# ffmpeg

<https://ffmpeg.org/>

## Install

::::{tab-set}
:::{tab-item} macOS Monterey

```console
$ brew install ffmpeg
```

Check the version:

```console
$ ffmpeg -version
ffmpeg version 7.0.2 Copyright (c) 2000-2024 the FFmpeg developers
built with Apple clang version 14.0.0 (clang-1400.0.29.202)
configuration: --prefix=/usr/local/Cellar/ffmpeg/7.0.2 --enable-shared --enable-pthreads --enable-version3 --cc=clang --host-cflags= --host-ldflags= --enable-ffplay --enable-gnutls --enable-gpl --enable-libaom --enable-libaribb24 --enable-libbluray --enable-libdav1d --enable-libharfbuzz --enable-libjxl --enable-libmp3lame --enable-libopus --enable-librav1e --enable-librist --enable-librubberband --enable-libsnappy --enable-libsrt --enable-libssh --enable-libsvtav1 --enable-libtesseract --enable-libtheora --enable-libvidstab --enable-libvmaf --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxml2 --enable-libxvid --enable-lzma --enable-libfontconfig --enable-libfreetype --enable-frei0r --enable-libass --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-libspeex --enable-libsoxr --enable-libzmq --enable-libzimg --disable-libjack --disable-indev=jack --enable-videotoolbox --enable-audiotoolbox
libavutil      59.  8.100 / 59.  8.100
libavcodec     61.  3.100 / 61.  3.100
libavformat    61.  1.100 / 61.  1.100
libavdevice    61.  1.100 / 61.  1.100
libavfilter    10.  1.100 / 10.  1.100
libswscale      8.  1.100 /  8.  1.100
libswresample   5.  1.100 /  5.  1.100
libpostproc    58.  1.100 / 58.  1.100
```

:::
::::

## Usage

### Trim

```console
$ ffmpeg -i input.mp4 -ss 00:02:22 -to 00:03:33 -c copy out.mp4
```

### Scale

```console
$ ffmpeg -i input.mp4 -vf scale=1920:1080 out.mp4
```

### Rotate

```console
$ ffmpeg -i input.mp4 -c copy -metadata:s:v:0 rotate=90 out.mp4
```

### Change FPS

```console
$ ffmpeg -i input.mp4 -vf fps=25 out.mp4
```

### Check

```console
$ ffmpeg -v error -i input.mp4 -f null
```

### mkv to mp4

```console
$ ffmpeg -i input.mkv -c:a copy -c:v copy -f mp4 out.mp4
```

:::{note}
`mp4` cannot contain `ass` subtitles.
:::

### Extract subtitle

```console
$ ffmpeg -i input.mkv -map 0:s:1 -c:s copy -f ass out.ass
```

### Concat files

Create a file `confiles.txt`:

```text
file 'a.mp3'
file 'b.mp3'
```

Then you can concat `a.mp3` and `b.mp3` by:

```console
$ ffmpeg -f concat -safe 0 -i confiles.txt -c copy out.mp3
```
