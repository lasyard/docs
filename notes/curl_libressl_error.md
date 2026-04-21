# Homebrew 安装软件时发生 curl 错误

在 macOS Monterey 上用 `brew` 安装软件时报如下错误：

```text
curl: (35) LibreSSL SSL_connect: SSL_ERROR_SYSCALL in connection to ghcr.io:443
```

这是 `brew` 试图用 `curl` 下载文件，但发现 https 连接的时候出错了。原因不明，可能与 proxy 的某些设置与 `LibreSSL` 不兼容有关。

系统自带的 `curl` 版本：

```console
$ type curl
curl is /usr/bin/curl
$ curl --version
curl 8.7.1 (x86_64-apple-darwin21.0) libcurl/8.7.1 (SecureTransport) LibreSSL/3.3.6 zlib/1.2.11 nghttp2/1.45.1
Release-Date: 2024-03-27
Protocols: dict file ftp ftps gopher gophers http https imap imaps ipfs ipns ldap ldaps mqtt pop3 pop3s rtsp smb smbs smtp smtps telnet tftp
Features: alt-svc AsynchDNS GSS-API HSTS HTTP2 HTTPS-proxy IPv6 Kerberos Largefile libz MultiSSL NTLM SPNEGO SSL threadsafe UnixSockets
```

换用 OpenSSL 版本的 `curl` 可解决：

```console
$ brew install curl
...
==> Caveats
==> curl
curl is keg-only, which means it was not symlinked into /usr/local,
because macOS already provides this software and installing another version in
parallel can cause all kinds of trouble.

If you need to have curl first in your PATH, run:
  echo 'export PATH="/usr/local/opt/curl/bin:$PATH"' >> ~/.zshrc

For compilers to find curl you may need to set:
  export LDFLAGS="-L/usr/local/opt/curl/lib"
  export CPPFLAGS="-I/usr/local/opt/curl/include"

zsh completions have been installed to:
  /usr/local/opt/curl/share/zsh/site-functions
```

如上面的输出所言，需要将 `/usr/local/opt/curl/bin` 加入到 `PATH` 环境变量（必须放在 `/usr/bin` 前面）以取代系统的 `curl`.

新的 `curl` 的版本：

```console
$ type curl
curl is /usr/local/opt/curl/bin/curl
$ curl --version
curl 8.9.1 (x86_64-apple-darwin21.6.0) libcurl/8.9.1 OpenSSL/3.3.2 (SecureTransport) zlib/1.2.11 brotli/1.1.0 zstd/1.5.6 libidn2/2.3.7 libssh2/1.11.0 nghttp2/1.63.0 librtmp/2.3
Release-Date: 2024-07-31
Protocols: dict file ftp ftps gopher gophers http https imap imaps ipfs ipns ldap ldaps mqtt pop3 pop3s rtmp rtsp scp sftp smb smbs smtp smtps telnet tftp
Features: alt-svc AsynchDNS brotli GSS-API HSTS HTTP2 HTTPS-proxy IDN IPv6 Kerberos Largefile libz MultiSSL NTLM SPNEGO SSL threadsafe TLS-SRP UnixSockets zstd
```

那么安装 `curl` 会不会受到这个错误的困扰？会的，死循环了是不是？

解决的方法之一是暴力重试，有一定的概率不出错。

---

后来在 macOS Tahoe 上安装 `brew` 依然碰到了这个问题，一看 `curl` 果然还是那个版本。我承认，暴力重试的方法是不负责任的。解决的办法是通过其他途径安装 `curl`.

实际上，问题的发生是因为在终端里使用 `HTTPS_PROXY`, 如果设置了系统的全局代理，问题自然解决。

Tahoe 上安装以后的版本，注意 CPU 架构也变了：

```console
$ curl --version
curl 8.19.0 (aarch64-apple-darwin25.3.0) libcurl/8.19.0 OpenSSL/3.6.2 zlib/1.2.12 brotli/1.2.0 zstd/1.5.7 AppleIDN libssh2/1.11.1 nghttp2/1.69.0 ngtcp2/1.22.1 nghttp3/1.15.0 mit-krb5/1.7-prerelease OpenLDAP/2.4.28/Apple
Release-Date: 2026-03-11
Protocols: dict file ftp ftps gopher gophers http https imap imaps ipfs ipns ldap ldaps mqtt mqtts pop3 pop3s rtsp scp sftp smb smbs smtp smtps telnet tftp ws wss
Features: alt-svc AppleSecTrust AsynchDNS brotli GSS-API HSTS HTTP2 HTTP3 HTTPS-proxy IDN IPv6 Kerberos Largefile libz NTLM SPNEGO SSL threadsafe TLS-SRP UnixSockets zstd
```
