# opencode

<https://opencode.ai/>

## Install

```console
$ curl -fsSL https://opencode.ai/install | bash

Installing opencode version: 1.2.25
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■ 100%
Successfully added opencode to $PATH in /Users/xxxx/.zshrc

                                 ▄     
█▀▀█ █▀▀█ █▀▀█ █▀▀▄ █▀▀▀ █▀▀█ █▀▀█ █▀▀█
█░░█ █░░█ █▀▀▀ █░░█ █░░░ █░░█ █░░█ █▀▀▀
▀▀▀▀ █▀▀▀ ▀▀▀▀ ▀  ▀ ▀▀▀▀ ▀▀▀▀ ▀▀▀▀ ▀▀▀▀


OpenCode includes free models, to start:

cd <project>  # Open directory
opencode      # Run command

For more information visit https://opencode.ai/docs
```

## Usage

```console
$ opencode providers list

┌  Credentials ~/.local/share/opencode/auth.json
│
└  0 credentials
```

```console
$ opencode auth list

┌  Credentials ~/.local/share/opencode/auth.json
│
└  0 credentials
```

After connect to Github Copilot.

```console
$ opencode providers list

┌  Credentials ~/.local/share/opencode/auth.json
│
●  GitHub Copilot oauth
│
└  1 credentials

```

```console
$ opencode models github-copilot
github-copilot/claude-haiku-4.5
github-copilot/claude-opus-4.5
github-copilot/claude-opus-4.6
github-copilot/claude-opus-41
github-copilot/claude-sonnet-4
github-copilot/claude-sonnet-4.5
github-copilot/claude-sonnet-4.6
github-copilot/gemini-2.5-pro
github-copilot/gemini-3-flash-preview
github-copilot/gemini-3-pro-preview
github-copilot/gemini-3.1-pro-preview
github-copilot/gpt-4.1
github-copilot/gpt-4o
github-copilot/gpt-5
github-copilot/gpt-5-mini
github-copilot/gpt-5.1
github-copilot/gpt-5.1-codex
github-copilot/gpt-5.1-codex-max
github-copilot/gpt-5.1-codex-mini
github-copilot/gpt-5.2
github-copilot/gpt-5.2-codex
github-copilot/gpt-5.3-codex
github-copilot/gpt-5.4
github-copilot/gpt-5.4-mini
github-copilot/grok-code-fast-1
```
