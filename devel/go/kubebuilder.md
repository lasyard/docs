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
$ kubebuilder create api --group app --version v1 --kind App
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

Generate manifests:

```console
$ make manifests
/home/ubuntu/workspace/coding-go/k8app/bin/controller-gen rbac:roleName=manager-role crd webhook paths="./..." output:crd:artifacts:config=config/crd/bases
```

### Run on cluster

Build the image and push it to a repository:

```console
$ make docker-build IMG=las3:443/lasyard.github.io/app:latest
$ make docker-push IMG=las3:443/lasyard.github.io/app:latest
```

Deploy the controller:

```console
$ make deploy IMG=las3:443/lasyard.github.io/app:latest
/home/ubuntu/workspace/coding-go/k8app/bin/controller-gen rbac:roleName=manager-role crd webhook paths="./..." output:crd:artifacts:config=config/crd/bases
cd config/manager && /home/ubuntu/workspace/coding-go/k8app/bin/kustomize edit set image controller=las3:443/lasyard.github.io/app:latest
/home/ubuntu/workspace/coding-go/k8app/bin/kustomize build config/default | kubectl apply -f -
namespace/k8app-system created
customresourcedefinition.apiextensions.k8s.io/apps.lasyard.github.io created
serviceaccount/k8app-controller-manager created
role.rbac.authorization.k8s.io/k8app-leader-election-role created
clusterrole.rbac.authorization.k8s.io/k8app-app-admin-role created
clusterrole.rbac.authorization.k8s.io/k8app-app-editor-role created
clusterrole.rbac.authorization.k8s.io/k8app-app-viewer-role created
clusterrole.rbac.authorization.k8s.io/k8app-manager-role created
clusterrole.rbac.authorization.k8s.io/k8app-metrics-auth-role created
clusterrole.rbac.authorization.k8s.io/k8app-metrics-reader created
rolebinding.rbac.authorization.k8s.io/k8app-leader-election-rolebinding created
clusterrolebinding.rbac.authorization.k8s.io/k8app-manager-rolebinding created
clusterrolebinding.rbac.authorization.k8s.io/k8app-metrics-auth-rolebinding created
service/k8app-controller-manager-metrics-service created
deployment.apps/k8app-controller-manager created
```

Show the deployment:

```console
$ k get all -n k8app-system
NAME                                            READY   STATUS    RESTARTS   AGE
pod/k8app-controller-manager-56cf8cdccc-nqwxv   1/1     Running   0          29s

NAME                                               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/k8app-controller-manager-metrics-service   ClusterIP   10.108.42.128   <none>        8443/TCP   29s

NAME                                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/k8app-controller-manager   1/1     1            1           29s

NAME                                                  DESIRED   CURRENT   READY   AGE
replicaset.apps/k8app-controller-manager-56cf8cdccc   1         1         1       29s
```

Create an `App`:

```console
$ kubectl apply -k config/samples/
app.lasyard.github.io/app-sample created
```

Show the logs of the pod:

```console
$ kubectl logs k8app-controller-manager-56cf8cdccc-nqwxv -n k8app-system
...
2025-06-30T10:37:49Z    INFO    Starting Controller {"controller": "app", "controllerGroup": "lasyard.github.io", "controllerKind": "App"}
2025-06-30T10:37:49Z    INFO    Starting workers    {"controller": "app", "controllerGroup": "lasyard.github.io", "controllerKind": "App", "worker count": 1}
2025-06-30T10:37:50Z    INFO    controller-runtime.metrics  Serving metrics server  {"bindAddress": ":8443", "secure": true}
Reconciling App: default/app-sample
```

### Clean up

```console
$ make undeploy
/home/ubuntu/workspace/coding-go/k8app/bin/kustomize build config/default | kubectl delete --ignore-not-found=false -f -
namespace "k8app-system" deleted
customresourcedefinition.apiextensions.k8s.io "apps.lasyard.github.io" deleted
serviceaccount "k8app-controller-manager" deleted
role.rbac.authorization.k8s.io "k8app-leader-election-role" deleted
clusterrole.rbac.authorization.k8s.io "k8app-app-admin-role" deleted
clusterrole.rbac.authorization.k8s.io "k8app-app-editor-role" deleted
clusterrole.rbac.authorization.k8s.io "k8app-app-viewer-role" deleted
clusterrole.rbac.authorization.k8s.io "k8app-manager-role" deleted
clusterrole.rbac.authorization.k8s.io "k8app-metrics-auth-role" deleted
clusterrole.rbac.authorization.k8s.io "k8app-metrics-reader" deleted
rolebinding.rbac.authorization.k8s.io "k8app-leader-election-rolebinding" deleted
clusterrolebinding.rbac.authorization.k8s.io "k8app-manager-rolebinding" deleted
clusterrolebinding.rbac.authorization.k8s.io "k8app-metrics-auth-rolebinding" deleted
service "k8app-controller-manager-metrics-service" deleted
deployment.apps "k8app-controller-manager" deleted
```
