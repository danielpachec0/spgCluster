package internal

import (
	"context"
	"encoding/json"
	"fmt"
	v1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/apis/meta/v1/unstructured"
	"k8s.io/apimachinery/pkg/runtime/schema"
	"k8s.io/client-go/dynamic"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/clientcmd"
	"k8s.io/client-go/util/homedir"
	"path/filepath"
)

type K8sClient struct {
	client *dynamic.DynamicClient
}

func GetKubeConfig() (*rest.Config, error) {
	var config *rest.Config
	var err error
	config, err = rest.InClusterConfig()
	if err != nil {
		var kubeconfig string
		if home := homedir.HomeDir(); home != "" {
			kubeconfig = filepath.Join(home, ".kube", "config")
		}
		fmt.Println(kubeconfig)
		config, err = clientcmd.BuildConfigFromFlags("", kubeconfig)
		if err != nil {
			return nil, err
		}
	}
	return config, nil
}

func GetClient() (*K8sClient, error) {
	config, err := GetKubeConfig()
	if err != nil {
		return nil, err
	}

	dnc, err := dynamic.NewForConfig(config)
	if err != nil {
		return nil, err
	}
	cfg := K8sClient{
		client: dnc,
	}
	return &cfg, nil
}

func (c K8sClient) ApplyTest(test *unstructured.Unstructured) error {
	scm := schema.GroupVersionResource{
		Group:    "k6.io",
		Version:  "v1alpha1",
		Resource: "k6s",
	}

	_, err := c.client.Resource(scm).Namespace("k6").Create(context.TODO(), test, v1.CreateOptions{})
	if err != nil {
		return err
	}
	return nil
}

func (c K8sClient) CleanUp(testName string) error {
	scm := schema.GroupVersionResource{
		Group:    "k6.io",
		Version:  "v1alpha1",
		Resource: "k6s",
	}

	return c.client.Resource(scm).Namespace("k6").Delete(context.TODO(), testName, v1.DeleteOptions{})
}

func (c K8sClient) GetTestStatus(testName string) (string, error) {
	scm := schema.GroupVersionResource{
		Group:    "k6.io",
		Version:  "v1alpha1",
		Resource: "k6s",
	}

	test, err := c.client.Resource(scm).Namespace("k6").Get(context.TODO(), testName, v1.GetOptions{})
	if err != nil {
		return "", err
	}
	statusJSON, err := json.Marshal(test.Object["status"])
	if err != nil {
		return "", err
	}
	var statusStruct r
	err = json.Unmarshal(statusJSON, &statusStruct)
	if err != nil {
		return "", err
	}
	return statusStruct.Stage, nil
}
