# helm

<https://helm.sh/>

The package manager for Kubernetes.

Helm is the best way to find, share, and use software built for Kubernetes.

## Install

### CentOS

:CPU: x86_64 * 8
:OS: CentOS 8.5

```sh
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod +x get_helm.sh
./get_helm.sh
```

```sh
helm version
```

{.cli-output}

```go
version.BuildInfo{Version:"v3.15.0-rc.2", GitCommit:"c4e37b39dbb341cb3f716220df9f9d306d123a58", GitTreeState:"clean", GoVersion:"go1.22.3"}
```

## Usage

Add a repository:

```sh
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```

Show repositories:

```sh
helm repo list
```

{.cli-output}

```text
NAME                    URL                                               
kubernetes-dashboard    https://kubernetes.github.io/dashboard/           
prometheus-community    https://prometheus-community.github.io/helm-charts
```

List (deployed) releases in all namespaces:

```sh
helm list -A
```

{.cli-output}

```text
NAME                    NAMESPACE               REVISION        UPDATED                                 STATUS          CHART                         APP VERSION
kubernetes-dashboard    kubernetes-dashboard    1               2024-05-30 16:28:11.77744534 +0800 CST  deployed        kubernetes-dashboard-7.4.0
```
