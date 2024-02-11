kubectl create configmap log-test --from-file ./logging.js -n k6

kubectl apply -f ./logging.yaml
