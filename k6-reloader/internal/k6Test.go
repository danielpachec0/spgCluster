package internal

import (
	v1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

type K6Test struct {
	ApiVersion string        `json:"apiVersion"`
	Kind       string        `json:"kind"`
	Metadata   v1.ObjectMeta `json:"metadata"`
	Spec       K6TestSpec    `json:"spec"`
}

type K6TestSpec struct {
	Parallelism int      `json:"parallelism"`
	Script      K6script `json:"script"`
	Runner      K6Runner `json:"runner"`
}

type K6script struct {
	ConfigMap ScriptConfig `json:"configMap"`
}

type ScriptConfig struct {
	Name string `json:"name"`
	File string `json:"file"`
}

type K6Runner struct {
	Image string     `json:"image"`
	Env   []K6EnvVar `json:"env"`
}

type K6EnvVar struct {
	Name  string `json:"name"`
	Value string `json:"value"`
}

type r struct {
	Stage string `json:"stage"`
}
