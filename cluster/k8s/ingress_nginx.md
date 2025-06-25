# Install Ingress-Nginx Controller

Using `helm`:

```console
$ helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
"ingress-nginx" has been added to your repositories
$ helm pull ingress-nginx/ingress-nginx
$ helm upgrade --install ingress-nginx ingress-nginx-4.12.3.tgz --namespace ingress-nginx --create-namespace
Release "ingress-nginx" does not exist. Installing it now.
NAME: ingress-nginx
LAST DEPLOYED: Mon Jun 23 16:02:46 2025
NAMESPACE: ingress-nginx
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
The ingress-nginx controller has been installed.
It may take a few minutes for the load balancer IP to be available.
You can watch the status by running 'kubectl get service --namespace ingress-nginx ingress-nginx-controller --output wide --watch'

An example Ingress that makes use of the controller:
  apiVersion: networking.k8s.io/v1
  kind: Ingress
  metadata:
    name: example
    namespace: foo
  spec:
    ingressClassName: nginx
    rules:
      - host: www.example.com
        http:
          paths:
            - pathType: Prefix
              backend:
                service:
                  name: exampleService
                  port:
                    number: 80
              path: /
    # This section is only required if TLS is to be enabled for the Ingress
    tls:
      - hosts:
        - www.example.com
        secretName: example-tls

If TLS is enabled for the Ingress, a Secret containing the certificate and key must also be provided:

  apiVersion: v1
  kind: Secret
  metadata:
    name: example-tls
    namespace: foo
  data:
    tls.crt: <base64 encoded cert>
    tls.key: <base64 encoded key>
  type: kubernetes.io/tls
```

A `LoadBalancer` service was created:

```console
$ kubectl get service ingress-nginx-controller --namespace=ingress-nginx
NAME                       TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
ingress-nginx-controller   LoadBalancer   10.110.223.80   <pending>     80:31104/TCP,443:30742/TCP   37m
```

Note the `EXTERNAL-IP` is `<pending>`. This is because our cluster does not provide external IPs automatically, but we can set it mannually to the node IPs:

```console
$ kubectl patch svc ingress-nginx-controller -n ingress-nginx -p '{"spec": {"type": "LoadBalancer", "externalIPs": ["10.225.4.51", "10.220.70.56"]}}'
service/ingress-nginx-controller patched
$ kubectl get service ingress-nginx-controller --namespace=ingress-nginx
NAME                       TYPE           CLUSTER-IP      EXTERNAL-IP                PORT(S)                      AGE
ingress-nginx-controller   LoadBalancer   10.110.223.80   10.225.4.51,10.220.70.56   80:31104/TCP,443:30742/TCP   61m
```

Show the `IngressClass`:

```console
$ kubectl get ingressclass
NAME    CONTROLLER             PARAMETERS   AGE
nginx   k8s.io/ingress-nginx   <none>       62m
```

Now you can create `Ingress` using this class by specify `{"spec": {"ingressClassName": "nginx"}}`.
