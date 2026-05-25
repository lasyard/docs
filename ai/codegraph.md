# codegraph

<https://github.com/colbymchenry/codegraph>

## Install

```console
$ npx @colbymchenry/codegraph
Need to install the following packages:
@colbymchenry/codegraph@0.9.4
Ok to proceed? (y) y
┌  CodeGraph v0.9.4
│
◇  Which agents should CodeGraph configure?
│  opencode (detected)
│
◇  Install the codegraph CLI on your PATH? (Required so agents can launch the MCP server)
│  Yes
│
◇  Installed codegraph CLI on PATH
│
◇  Apply agent configs to all your projects, or just this one?
│  All projects
│
◆  opencode: Updated ~/.config/opencode/opencode.jsonc
│
◆  opencode: Created ~/.config/opencode/AGENTS.md
│
◇  Quick start ───────╮
│                     │
│  cd your-project    │
│  codegraph init -i  │
│                     │
├─────────────────────╯
│
└  Done! Restart your agent to use CodeGraph.
```

In the installation above, we configured it for [opencode](project:opencode.md). Check the mcps of opencode:

```console
$ opencode mcp list

┌  MCP Servers
│
●  ✓ codegraph connected
│      codegraph serve --mcp
│
└  1 server(s)
```

## Usage

Do as the "Quick start" says. A sqlite3 db will be create in `.codegraph`.
