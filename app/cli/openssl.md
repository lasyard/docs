# openssl

## Install

:::::{tab-set}
::::{tab-item} macOS
:sync: macos

```console
$ brew install openssl
```

::::
::::{tab-item} Ubuntu
:sync: ubuntu

```console
$ sudo apt install openssl
```

::::
:::::

## Usage

Generate a key:

```console
$ openssl genrsa -out ca.key 4096
```

Create a self signed cert as root:

```console
$ openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -subj "/CN=CA" -out ca.crt
```

Generate another key:

```console
$ openssl genrsa -out server.key 4096
```

Create a request for vouching the `server.key`:

```console
$ openssl req -new -key server.key -subj "/CN=server" -out server.csr
```

Vouching the request by the root CA to generate the new cert for the `server.key`:

```console
$ openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365 -sha256
Certificate request self-signature ok
subject=CN = server
```

Show the content of the cert:

```console
$ openssl x509 -noout -text -in server.crt
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            32:b7:e1:c9:c7:00:c2:b0:e1:5c:35:40:29:98:2a:90:eb:8c:11:92
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: CN = CA
        Validity
            Not Before: Sep 14 07:44:02 2026 GMT
            Not After : Sep 14 07:44:02 2027 GMT
        Subject: CN = server
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (4096 bit)
                Modulus:
                    ...
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Subject Key Identifier: 
                8A:2A:C7:2C:07:04:33:BD:96:33:92:1F:1B:4B:10:8B:2E:1B:E8:C0
            X509v3 Authority Key Identifier: 
                A3:EF:58:4B:8D:F6:F3:D1:5E:D1:BA:E6:B3:1D:7F:B8:B0:9D:9A:A4
    Signature Algorithm: sha256WithRSAEncryption
    Signature Value:
        ...
```
