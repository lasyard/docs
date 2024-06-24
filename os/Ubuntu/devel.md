# Install Development Tools on Ubuntu

## C/C++

Install build essenstial:

```sh
sudo apt satisfy build-essential
```

Install kernel headers if you need to compile kernel modules:

```sh
sudo apt satisfy linux-headers-$(uname -r)
```

Install other tools:

```sh
sudo apt satisfy fakeroot devscripts
```

If you want to build deb packages, you need to install `equivs`:

```sh
sudo apt satisfy equivs
```
