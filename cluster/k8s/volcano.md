# volcano

<https://volcano.sh/en/>

Install with helm:

```console
$ helm repo add volcano-sh https://volcano-sh.github.io/helm-charts
"volcano-sh" has been added to your repositories
$ helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "volcano-sh" chart repository
Update Complete. ⎈Happy Helming!⎈
$ helm install volcano volcano-sh/volcano -n volcano-system --create-namespace
NAME: volcano
LAST DEPLOYED: Tue Apr 22 03:47:04 2025
NAMESPACE: volcano-system
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Thank you for installing volcano.

Your release is named volcano.

For more information on volcano, visit:
https://volcano.sh/
```

Show the installed release:

```console
$ helm list -n volcano-system
NAME    NAMESPACE       REVISION    UPDATED                                 STATUS      CHART           APP VERSION
volcano volcano-system  1           2025-04-22 03:47:04.391250411 +0000 UTC deployed    volcano-1.11.1  1.11.1
```
