# Use Cargo to Manage Rust Project

Create a new project:

```console
$ cargo new hello-rust
    Creating binary (application) `hello-rust` package
note: see more `Cargo.toml` keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html
```

Enter the project directory:

```console
$ cd hello-rust
```

Run the project:

```console
$ cargo run
   Compiling hello-rust v0.1.0 (/Users/jyg/workspace/coding/rust/hello-rust)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 2.84s
     Running `target/debug/hello-rust`
Hello, world!
```

Add a dependency:

```console
$ cargo add ferris-says
    Updating crates.io index
      Adding ferris-says v0.3.2 to dependencies
             Features:
             - clippy
    Updating crates.io index
     Locking 12 packages to latest Rust 1.90.0 compatible versions
      Adding aho-corasick v1.1.3
      Adding ferris-says v0.3.2
      Adding memchr v2.7.5
      Adding regex v1.11.2
      Adding regex-automata v0.4.10
      Adding regex-syntax v0.8.6
      Adding smallvec v1.15.1
      Adding smawk v0.3.2
      Adding textwrap v0.16.2
      Adding unicode-linebreak v0.1.5
      Adding unicode-width v0.1.14
      Adding unicode-width v0.2.1
```

Build (to compiling the dependecies):

```console
$ cargo build
   Compiling memchr v2.7.5
   Compiling regex-syntax v0.8.6
   Compiling smawk v0.3.2
   Compiling unicode-linebreak v0.1.5
   Compiling unicode-width v0.2.1
   Compiling smallvec v1.15.1
   Compiling textwrap v0.16.2
   Compiling unicode-width v0.1.14
   Compiling aho-corasick v1.1.3
   Compiling regex-automata v0.4.10
   Compiling regex v1.11.2
   Compiling ferris-says v0.3.2
   Compiling hello-rust v0.1.0 (/Users/jyg/workspace/coding/rust/hello-rust)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 13.92s
```

Change the `main.rs` source file of the project to:

```rust
use ferris_says::say;
use std::io::{BufWriter, stdout};

fn main() {
    let mut writer = BufWriter::new(stdout());
    say("Hello, world!", 24, &mut writer).unwrap();
}
```

Run it to see the output:

```console
$ cargo run        
   Compiling hello-rust v0.1.0 (/Users/jyg/workspace/coding/rust/hello-rust)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 1.05s
     Running `target/debug/hello-rust`
 _______________
< Hello, world! >
 ---------------
        \
         \
            _~^~^~_
        \) /  o o  \ (/
          '_   -   _'
          / '-----' \
```
