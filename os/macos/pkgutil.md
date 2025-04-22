# pkgutil

List all installed packages:

```console
$ pkgutil --pkgs
```

Show metadata for a package:

```console
$ pkgutil --pkg-info com.apple.pkg.CLTools_Executables
package-id: com.apple.pkg.CLTools_Executables
version: 14.2.0.0.1.1668646533
volume: /
location: /
install-time: 1717553998
groups: com.apple.FindSystemFiles.pkg-group
```

List installed files for a package:

```console
$ pkgutil --files com.apple.pkg.CLTools_Executables
```

Discard receipt data for a package:

```console
$ sudo pkgutil --forget com.apple.pkg.CLTools_Executables
```
