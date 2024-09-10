# pkgutil

`pkgutil` is a command-line tool that allows you to manage packages on macOS.

## Usage

List all installed packages:

```sh
pkgutil --pkgs
```

Show metadata for a package:

```sh
pkgutil --pkg-info com.apple.pkg.CLTools_Executables
```

{.cli-output}

```text
package-id: com.apple.pkg.CLTools_Executables
version: 14.2.0.0.1.1668646533
volume: /
location: /
install-time: 1671030261
groups: com.apple.FindSystemFiles.pkg-group
```

List installed files for a package:

```sh
pkgutil --files com.apple.pkg.CLTools_Executables
```

Discard receipt data for a package:

```sh
sudo pkgutil --forget com.apple.pkg.CLTools_Executables
```
