package internal

import (
	"fmt"
	"gopkg.in/yaml.v2"
	v1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/apis/meta/v1/unstructured"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/util/uuid"
	"os"
	"strconv"
)

type TestConfig struct {
	Iterations  int         `yaml:"iterations"`
	CoolDown    int         `yaml:"cool-down"`
	Parallelism int         `yaml:"parallelism"`
	Vars        []VarConfig `yaml:"vars"`
}

type VarConfig struct {
	Name  string       `yaml:"name"`
	Value varInterface `yaml:"value"`
}

type varInterface interface {
	getValue(i int) string
}

type stringImpl struct {
	value string
}

func (s stringImpl) getValue(_ int) string {
	return s.value
}

type sliceImpl struct {
	values []string
}

func (s sliceImpl) getValue(i int) string {
	return s.values[i]
}

func (vc *VarConfig) UnmarshalYAML(unmarshal func(interface{}) error) error {
	var err error
	var aux struct {
		Name  string      `yaml:"name"`
		Value interface{} `yaml:"value"`
	}

	if err := unmarshal(&aux); err != nil {
		return err
	}

	vc.Name = aux.Name

	switch v := aux.Value.(type) {
	case []interface{}:
		var values []string
		for _, iv := range v {
			str, ok := iv.(string)
			if !ok {
				return err
			}
			values = append(values, str)
		}
		vc.Value = sliceImpl{values}
	case string:
		vc.Value = stringImpl{v}
	default:
		return err // Handle the unexpected type
	}

	return nil
}

func ReadConfig() (TestConfig, error) {
	var config TestConfig
	//yamlData, err := os.ReadFile("/reloader/test.yaml")
	yamlData, err := os.ReadFile("/home/daniel/Projects/spgCluster/k6-reloader/test.yaml")

	if err != nil {
		return config, err
	}
	err = yaml.Unmarshal(yamlData, &config)
	if err != nil {
		return config, err
	}
	return config, nil
}

func (config TestConfig) CreateTest(iteration int, p int) (*unstructured.Unstructured, string, error) {
	testIdentifier := string(uuid.NewUUID())
	env := []K6EnvVar{
		{"TEST_IDENTIFIER", testIdentifier},
		{"K6_VUS", strconv.Itoa(p)},
	}
	var err error
	for _, v := range config.Vars {
		env = append(env, K6EnvVar{Name: v.Name, Value: v.Value.getValue(iteration)})
	}

	fmt.Println(env)

	test := K6Test{
		ApiVersion: "k6.io/v1alpha1",
		Kind:       "K6",
		Metadata:   v1.ObjectMeta{Name: "test"},
		Spec: K6TestSpec{
			Parallelism: p,
			Script: K6script{
				ConfigMap: ScriptConfig{
					Name: "log-test",
					File: "logging.js",
				},
			},
			Runner: K6Runner{
				Image: "dap5/custom_k6:v2",
				Env:   env,
			},
		},
	}
	//log.Fatalln("T")
	k6TestMap, err := runtime.DefaultUnstructuredConverter.ToUnstructured(&test)
	if err != nil {
		return nil, testIdentifier, err
	}

	k6TestUnstructured := &unstructured.Unstructured{Object: k6TestMap}
	return k6TestUnstructured, testIdentifier, nil
}
