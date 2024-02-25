kubectl create configmap tracing-test-config --from-file=../tracing/tracingTest01.js -n k6

kubectl create configmap k6-reloader-config --from-file=./reloader/reload.sh --from-file=../tracing/tracing.yaml -n k6

kubectl apply -f ./reloader/deployment.yaml
