# Miscellaneous

## Check version

:::{literalinclude} /_files/ubuntu/console/cat/version.txt
:language: console
:::

## Usage

### User management

Add a new user:

```sh
sudo adduser xxxx
```

Add the new user to the `sudo` group:

```sh
sudo usermod -aG sudo xxxx
```

Add a new user with other specified attributes:

```sh
sudo adduser --disabled-password --disabled-login --no-create-home --gecos "XXXX" --uid 1001 xxxx
```

Delete a user:

```sh
sudo deluser xxxx
```
