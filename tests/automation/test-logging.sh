kubectl create configmap log-test --from-file=../logging/logging.js -n k6

kubectl create configmap k6-reloader-config --from-file=reload.sh --from-file=../logging/logging.yaml -n k6

kubectl apply -f ./k6-reloader.yaml
