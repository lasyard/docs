# npm

<https://www.npmjs.com/>

Check environment:

```console
$ npm doctor
```

Upgrate npm:

```console
$ npm install -g npm
```

:::{note}
Because our `npm` is installed in current user's home directory by `nvm` (along with `node`), no root previlege is needed.
:::

Clear cache:

```console
$ npm cache clear --force
```

Install packages in current directory:

```console
$ npm install
```

List packages installed:

```console
$ npm ls
```

List packages outdated:

```console
$ npm outdated
```

Install latest version of a package:

```console
$ npm install react@latest
```

Uninstall a package:

```console
$ npm uninstall @rjsf/core --force
```

Show configurations:

```console
npm config get
; node bin location = /Users/xxxx/.nvm/versions/node/v23.11.0/bin/node
; node version = v23.11.0
; npm local prefix = /Users/xxxx/workspace/homepage/lasys
; npm version = 11.3.0
...
```

Set registry mirror:

```console
$ npm config set registry https://mirrors.cloud.tencent.com/npm/
```

The configuration is saved in `~/.npmrc`.

:::{literalinclude} /_files/macos/home/npmrc
:language: ini
:::
