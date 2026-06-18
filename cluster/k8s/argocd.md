# ArgoCD

<https://argoproj.github.io/cd/>

## Install

### In cluster

```console
$ helm repo add argo https://argoproj.github.io/argo-helm
$ helm repo update
$ helm pull argo/argo-cd
```

```console
$ helm install argocd argo-cd-9.5.17.tgz --namespace argocd --create-namespace --set global.domain=las1
NAME: argocd
LAST DEPLOYED: Wed Jun  3 14:16:09 2026
NAMESPACE: argocd
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
In order to access the server UI you have the following options:

1. kubectl port-forward service/argocd-server -n argocd 8080:443

    and then open the browser on http://localhost:8080 and accept the certificate

2. enable ingress in the values file `server.ingress.enabled` and either
      - Add the annotation for ssl passthrough: https://argo-cd.readthedocs.io/en/stable/operator-manual/ingress/#option-1-ssl-passthrough
      - Set the `configs.params."server.insecure"` in the values file and terminate SSL at your ingress: https://argo-cd.readthedocs.io/en/stable/operator-manual/ingress/#option-2-multiple-ingress-objects-and-hosts


After reaching the UI the first time you can login with username: admin and the random password generated during the installation. You can find the password by running:

kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

(You should delete the initial secret afterwards as suggested by the Getting Started Guide: https://argo-cd.readthedocs.io/en/stable/getting_started/#4-login-using-the-cli)
```

> [!NOTE]
> The `global.domain` is set to the domain we expose the argocd service.

Show the workloads:

```console
$ kubectl get svc,deploy -n argocd
NAME                                       TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)             AGE
service/argocd-applicationset-controller   ClusterIP   10.103.117.59   <none>        7000/TCP            53s
service/argocd-dex-server                  ClusterIP   10.105.77.156   <none>        5556/TCP,5557/TCP   53s
service/argocd-redis                       ClusterIP   10.100.74.58    <none>        6379/TCP            53s
service/argocd-repo-server                 ClusterIP   10.109.28.160   <none>        8081/TCP            53s
service/argocd-server                      ClusterIP   10.102.127.32   <none>        80/TCP,443/TCP      53s

NAME                                               READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/argocd-applicationset-controller   1/1     1            1           53s
deployment.apps/argocd-dex-server                  1/1     1            1           53s
deployment.apps/argocd-notifications-controller    1/1     1            1           53s
deployment.apps/argocd-redis                       1/1     1            1           53s
deployment.apps/argocd-repo-server                 1/1     1            1           53s
deployment.apps/argocd-server                      1/1     1            1           53s
```

Now expose the service by modify its type to LoadBalancer (also with available external IPs for we don't have IP provider):

```console
$ kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer", "externalIPs": ["10.225.4.52", "10.220.70.125"]}}'
service/argocd-server patched
```

Now we can access the web UI. The initial admin password can be get as said in the installation notes. Or by CLI metioned hereafter.

### CLI

:::::{tab-set}
::::{tab-item} macOS
:sync: macos

```console
$ brew install argocd
```

```console
$ argocd version  
argocd: v3.4.3+1801122.dirty
  BuildDate: 2026-05-28T15:08:05Z
  GitCommit: 1801122b4391cad4961301f787006dc9a88c2dd3
  GitTreeState: dirty
  GitTag: v3.4.3
  GoVersion: go1.26.3
  Compiler: gc
  Platform: darwin/arm64
{"level":"fatal","msg":"Argo CD server address unspecified","time":"2026-06-03T10:35:48+08:00"}
```

::::
:::::

## Usage

### Accounts

Get the initial password of admin:

```console
$ argocd admin initial-password -n argocd
xxxxxxxxxxxxxxxx

 This password must be only used for first time login. We strongly recommend you update the password using `argocd account update-password`.
```

Login:

```console
$ argocd login las1                      
WARNING: server certificate had error: error creating connection: tls: failed to verify certificate: x509: certificate signed by unknown authority. Proceed insecurely (y/n)? y
Username: admin
Password: 
'admin:login' logged in successfully
Context 'las1' updated
```

Now the server is added to context list:

```console
$ argocd context
CURRENT  NAME  SERVER
*        las1  las1
```

Change the password of current user (admin):

```console
$ argocd account update-password
```

Then the secret of intial password can be deleted:

```console
$ kubectl delete secret argocd-initial-admin-secret -n argocd
secret "argocd-initial-admin-secret" deleted from argocd namespace
```

The default cluster is where ArgoCD installed:

```console
$ argocd cluster list
SERVER                          NAME        VERSION  STATUS   MESSAGE                                                  PROJECT
https://kubernetes.default.svc  in-cluster  1.35.0   Unknown  Cluster has no applications and is not being monitored.
```

### Repos

Before create an app, add the repo to make sure it can be connected:

```console
$ argocd repo add git@github.com:lasyard/coding-go.git --name argocd-example --ssh-private-key-path ~/.ssh/id_ed25519
Repository 'git@github.com:lasyard/coding-go.git' added
```

Show the repo list:

```console
$ argocd repo list
TYPE  NAME            REPO                                  INSECURE  OCI    LFS    CREDS  STATUS      MESSAGE  PROJECT
git   argocd-example  git@github.com:lasyard/coding-go.git  false     false  false  false  Successful
```

### Apps

Then we can create an app in the cluster specified by `--dest-server` using this repo:

```console
$ argocd app create upload --repo git@github.com:lasyard/coding-go.git --path k8s/upload-svc --dest-server https://kubernetes.default.svc --dest-namespace default 
application 'upload' created
```

List the apps:

```console
$ argocd app list
NAME           CLUSTER                         NAMESPACE  PROJECT  STATUS     HEALTH   SYNCPOLICY  CONDITIONS  REPO                                  PATH            TARGET
argocd/upload  https://kubernetes.default.svc  default    default  OutOfSync  Missing  Manual      <none>      git@github.com:lasyard/coding-go.git  k8s/upload-svc  
```

Show the app details:

```console
$ argocd app get upload
Name:               argocd/upload
Project:            default
Server:             https://kubernetes.default.svc
Namespace:          default
URL:                https://las1/applications/upload
Source:
- Repo:             git@github.com:lasyard/coding-go.git
  Target:           
  Path:             k8s/upload-svc
SyncWindow:         Sync Allowed
Sync Policy:        Manual
Sync Status:        OutOfSync from  (3cc2757)
Health Status:      Missing

GROUP              KIND        NAMESPACE  NAME                STATUS     HEALTH   HOOK  MESSAGE
                   Service     default    upload-svc          OutOfSync  Missing        
apps               Deployment  default    upload-svc          OutOfSync  Missing        
networking.k8s.io  Ingress     default    upload-svc-ingress  OutOfSync  Missing
```

> [!NOTE]
> ArgoCD will search the repo for things that can be installed in kubernetes. The other files does not matter. Only put the related files in the path for best practice.

Actually, the app is a resource stored in `argocd` namespace:

```console
$ kubectl get app -n argocd       
NAME     SYNC STATUS   HEALTH STATUS
upload   OutOfSync     Missing
```

We need to sync the app mannually:

```console
$ argocd app sync upload
TIMESTAMP                  GROUP                    KIND   NAMESPACE                  NAME    STATUS    HEALTH        HOOK  MESSAGE
2026-06-04T14:35:02+08:00                        Service     default            upload-svc  OutOfSync  Missing              
2026-06-04T14:35:02+08:00   apps              Deployment     default            upload-svc  OutOfSync  Missing              
2026-06-04T14:35:02+08:00  networking.k8s.io     Ingress     default    upload-svc-ingress  OutOfSync  Missing              
2026-06-04T14:35:05+08:00  networking.k8s.io     Ingress     default    upload-svc-ingress  OutOfSync  Missing              ingress.networking.k8s.io/upload-svc-ingress created
2026-06-04T14:35:05+08:00                        Service     default            upload-svc  OutOfSync  Missing              service/upload-svc created
2026-06-04T14:35:05+08:00   apps              Deployment     default            upload-svc  OutOfSync  Missing              deployment.apps/upload-svc created
2026-06-04T14:35:06+08:00                        Service     default            upload-svc    Synced  Healthy                  service/upload-svc created
2026-06-04T14:35:06+08:00   apps              Deployment     default            upload-svc    Synced  Progressing              deployment.apps/upload-svc created
2026-06-04T14:35:06+08:00  networking.k8s.io     Ingress     default    upload-svc-ingress    Synced  Progressing              ingress.networking.k8s.io/upload-svc-ingress created

Name:               argocd/upload
Project:            default
Server:             https://kubernetes.default.svc
Namespace:          default
URL:                https://las1/applications/upload
Source:
- Repo:             git@github.com:lasyard/coding-go.git
  Target:           
  Path:             k8s/upload-svc
SyncWindow:         Sync Allowed
Sync Policy:        Manual
Sync Status:        Synced to  (3cc2757)
Health Status:      Progressing

Operation:          Sync
Sync Revision:      3cc2757fe554830bb989daf7028565a2028b1dbf
Phase:              Succeeded
Start:              2026-06-04 14:35:05 +0800 CST
Finished:           2026-06-04 14:35:05 +0800 CST
Duration:           0s
Message:            successfully synced (all tasks run)

GROUP              KIND        NAMESPACE  NAME                STATUS  HEALTH       HOOK  MESSAGE
                   Service     default    upload-svc          Synced  Healthy            service/upload-svc created
apps               Deployment  default    upload-svc          Synced  Healthy            deployment.apps/upload-svc created
networking.k8s.io  Ingress     default    upload-svc-ingress  Synced  Progressing        ingress.networking.k8s.io/upload-svc-ingress created
```

At the URL provided above, you can find a figure to illustrate the app:

![argocd_upload_app.png)](/_images/cluster/k8s/argocd_upload_app.png)

Actually, the app itself is a resource in namespace `argocd`:

```console
$ kubectl get app -n argocd
NAME     SYNC STATUS   HEALTH STATUS
upload   Synced        Healthy
```

You can even create an app by create an app resource resource directly. Write the `yaml` file like:

:::{literalinclude} /_files/macos/workspace/argocd/upload_app.yaml
:::

Then apply it:

```console
$ kubectl apply -f upload_app.yaml
application.argoproj.io/upload created
```

For we set it to sync automatically, manual sync is not needed this time.

The sources are cached, do force refreshing:

```console
$ argocd app get upload --hard-refresh
```

### SSO

Through Dex-based SSO, you can login with LDAP:

```sh
argocd login <server> --sso
```

Authenticate on the browser page Dex shows, the CLI will receive the session after the SSO callback completes.
