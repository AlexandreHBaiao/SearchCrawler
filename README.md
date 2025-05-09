# SearchCrawler
> az login
> az account set --subscription f1e8678b-1a9a-4645-8c10-c8bfe5f580e2


> curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
> curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
> echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
> kubectl version

> az aks get-credentials --admin --resource-group jerryjo-aks --name moonshot --file config.moonshot
> mkdir ~/.kube/
> mv config.moonshot ~/.kube/
> export KUBECONFIG=~/.kube/config.moonshot
> kubectl get pods -n azs
> kubectl port-forward services/my-first-cluster 9200:9200 -n azs
