# npm

<https://www.npmjs.com/>

## Usage

Check environment:

```sh
npm doctor
```

Upgrate npm:

```sh
sudo npm install -g npm
```

Clear cache:

```sh
npm cache clear --force
```

Install packages in current directory:

```sh
npm install
```

List packages installed:

```sh
npm ls
```

List packages outdated:

```sh
npm outdated
```

Install latest version of a package:

```sh
npm install react@latest
```

Uninstall a package:

```sh
npm uninstall @rjsf/core --force
```

Show configurations:

:::{literalinclude} /_files/macos/console/npm/c_get.txt
:console:
:::

Set registry mirror:

```sh
npm config set registry https://mirrors.cloud.tencent.com/npm/
```

The configuration is saved in `~/.npmrc`.
