# lame

<https://lame.sourceforge.io/>

## Install

::::{tabs}
:{tab} macOS Monterey
Install using `brew`:

```console
$ brew install lame
```

Check the version:

```console
$ lame --version
LAME 64bits version 3.100 (http://lame.sf.net)

Copyright (c) 1999-2011 by The LAME Project
Copyright (c) 1999,2000,2001 by Mark Taylor
Copyright (c) 1998 by Michael Cheng
Copyright (c) 1995,1996,1997 by Michael Hipp: mpglib

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Library General Public
License as published by the Free Software Foundation; either
version 2 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Library General Public License for more details.

You should have received a copy of the GNU Library General Public
License along with this program. If not, see
<http://www.gnu.org/licenses/>.
```

:::
::::

## Usage

Convert `.wav` to `.mp3`:

```console
$ lame -b 320 "audio.wav" "audio.mp3"
```
