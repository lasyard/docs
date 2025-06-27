# kubebuilder

## Install

```console
$ curl -LO https://github.com/kubernetes-sigs/kubebuilder/releases/download/v4.6.0/kubebuilder_linux_amd64
$ chmod +x kubebuilder_linux_amd64
$ sudo cp kubebuilder_linux_amd64 /usr/local/bin/kubebuilder
```

Show version:

```console
$ kubebuilder version
Version: cmd.version{KubeBuilderVersion:"4.6.0", KubernetesVendor:"1.33.0", GitCommit:"cd90bd82a2d692fbf63ba0231699e2e3dc0b6a08", BuildDate:"2025-05-24T23:24:02Z", GoOs:"linux", GoArch:"amd64"}
```

## Usage

### Init a project

```console
$ mkdir k8app
$ cd k8app
$ kubebuilder init --domain lasyard.github.io --repo github.com/lasyard/coding-go/k8app
INFO Writing kustomize manifests for you to edit... 
INFO Writing scaffold for you to edit...          
INFO Get controller runtime:
...
INFO Update dependencies:
...
```

### Create an API

```console
$ kubebuilder create api --group io.github.lasyard --version v1 --kind App
INFO Create Resource [y/n]                        
y
INFO Create Controller [y/n]                      
y
INFO Writing kustomize manifests for you to edit... 
INFO Writing scaffold for you to edit...          
INFO api/v1/app_types.go                          
INFO api/v1/groupversion_info.go                  
INFO internal/controller/suite_test.go            
INFO internal/controller/app_controller.go        
INFO internal/controller/app_controller_test.go   
INFO Update dependencies:
...
INFO Running make:
...
```
