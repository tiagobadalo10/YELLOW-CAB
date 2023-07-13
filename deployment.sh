kubectl create secret generic yellow-cab-secret --from-file=service-account-key=./authorization.txt --dry-run=client -o yaml | kubectl apply -f -
kubectl create secret tls yellow-cab-tls-secret --cert=./cert.crt --key=./key.key --dry-run=client -o yaml | kubectl apply -f -
kubectl create configmap prometheus-cm --from-file app/prometheus/prometheus-cm.yaml --dry-run=client -o yaml | kubectl apply -f -

kubectl delete -f app/k8s-config

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.6.4/deploy/static/provider/cloud/deploy.yaml
kubectl wait --namespace ingress-nginx \
 --for=condition=ready pod \
 --selector=app.kubernetes.io/component=controller \
 --timeout=60s

kubectl apply -f app/k8s-config/configmap.yaml
kubectl apply -f app/k8s-config/deployment.yaml 
kubectl apply -f app/k8s-config/services.yaml 
kubectl apply -f app/k8s-config/ingress.yaml
kubectl apply -f app/k8s-config/prometheus.yaml 
kubectl apply -f app/k8s-config/horizontalpodautoscaler.yaml

