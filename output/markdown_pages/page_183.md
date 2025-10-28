## Audit:

1. Install theetcd CLl (etcdctl) version 3 or later 

ca 



export ETCDCTL 」API=3

3. Run the ibmcloud ks cluster config command and include the --admin option,which downloads the etcd certificates and keys for your cluster, and the --output zip > <cluster_name_or_ID>.zip option, which saves your cluster configuration files to a compressed folder.



ibmcloud ks cluster config -c <cluster_name_or_ID> --admin --output zip <cluster name_or_ID>.zip 



4. Decompress the compressed folder.

5. Get the server field for your cluster. In the output, copy only the master URL,without https:// and the node port.



cat ./<cluster name or ID>/kube-config.yaml /grep server 

6. Get the etcdPort for your cluster.

ibmcloud ks  cluster get -c <cluster name or ID>—-output json I grep etcdPort 

7. Get the name of a secret in your cluster.

kubectl get secrets [-n <namespace>]

8. Confirm that the Kubernetes secrets for the cluster are encrypted. Replace the secret_name, master_url, and etcd_portfields with the values that you previously retrieved, and replace <cluster_name_or_ID> with the name of the cluster in your compressed folder file path.



etcdctl get /registry/secrets/<secret_namespace>/<secret_name> --endpoints https://<master_url>:<etcd_port> --key="./<cluster_name_or_Id>/admin-key.pem"—-cert="./<cluster_name_or_Id>/admin.pem"cacert=./<cluster_name_or_ID>/ca.pem"

9. Ensure the output is unreadable and scrambled, indicating that it is encrypted.

## Remediation:

## From Console:

1. Log in to your IBM Cloud account.

[aab]

