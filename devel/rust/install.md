# Install Rust Development Environment

::::{tab-set}
:::{tab-item} macOS

```console
$ curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
info: downloading installer

Welcome to Rust!

This will download and install the official compiler for the Rust
programming language, and its package manager, Cargo.

Rustup metadata and toolchains will be installed into the Rustup
home directory, located at:

  /Users/xxxx/.rustup

This can be modified with the RUSTUP_HOME environment variable.

The Cargo home directory is located at:

  /Users/xxxx/.cargo

This can be modified with the CARGO_HOME environment variable.

The cargo, rustc, rustup and other commands will be added to
Cargo's bin directory, located at:

  /Users/xxxx/.cargo/bin

This path will then be added to your PATH environment variable by
modifying the profile files located at:

  /Users/xxxx/.profile
  /Users/xxxx/.zshenv

You can uninstall at any time with rustup self uninstall and
these changes will be reverted.

Current installation options:


   default host triple: x86_64-apple-darwin
     default toolchain: stable (default)
               profile: default
  modify PATH variable: yes

1) Proceed with standard installation (default - just press enter)
2) Customize installation
3) Cancel installation
>
...
info: default toolchain set to 'stable-x86_64-apple-darwin'

  stable-x86_64-apple-darwin installed - rustc 1.90.0 (1159e78c4 2025-09-14)


Rust is installed now. Great!

To get started you may need to restart your current shell.
This would reload your PATH environment variable to include
Cargo's bin directory ($HOME/.cargo/bin).

To configure your current shell, you need to source
the corresponding env file under $HOME/.cargo.

This is usually done by running one of the following (note the leading DOT):
. "$HOME/.cargo/env"            # For sh/bash/zsh/ash/dash/pdksh
source "$HOME/.cargo/env.fish"  # For fish
source $"($nu.home-path)/.cargo/env.nu"  # For nushell
```

For `zsh`, the installer already added a line to `~/.zshenv`:

```console
$ cat ~/.zshenv
. "$HOME/.cargo/env"
```

Show the version:

```console
$ cargo --version
cargo 1.90.0 (840b83a10 2025-07-30)
$ rustc --version
rustc 1.90.0 (1159e78c4 2025-09-14)
```

:::
::::

## rustup

Update rust:

```console
$ rustup update
info: syncing channel updates for 'stable-x86_64-apple-darwin'
info: checking for self-update

  stable-x86_64-apple-darwin unchanged - rustc 1.90.0 (1159e78c4 2025-09-14)

info: cleaning up downloads & tmp directories
```

To see the book:

```console
$ rustup doc --book
Opening docs named `book` in your browser
```
