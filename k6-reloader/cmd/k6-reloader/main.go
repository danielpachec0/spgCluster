package main

import (
	"k6-reloader/internal"
	"log"
	"strconv"
	"time"
)

func main() {
	client, err := internal.GetClient()
	if err != nil {
		panic(err.Error())
	}

	cfg, err := internal.ReadConfig()
	if err != nil {
		panic(err.Error())
	}

	if err != nil {
		log.Fatal(err)
	}

	tn := cfg.Iterations
	te := 0
	for te < tn {
		test, testId, err := cfg.CreateTest(te)
		if err != nil {
			log.Fatal(err)
		}

		log.Println("Creating test " + testId)
		err = client.ApplyTest(test)
		if err != nil {
			log.Fatal(err)
		}
		testRunning := true
		podsRunning := true
		var status string
		for testRunning && podsRunning {
			time.Sleep(1 * time.Second)
			status, err = client.GetTestStatus("test")
			if err != nil {
				log.Fatal(err)
			}
			if status == "error" || status == "finished" {
				log.Println("Test '" + testId + "' finished with status: " + status)
				testRunning = false
			}

			podsRunning, err = client.CheckPods()
			if err != nil {
				log.Fatal(err)
			}
		}
		if status == "finished" {
			te++
		}
		log.Println("Cleaning up test " + testId)
		err = client.CleanUp("test")
		if err != nil {
			log.Fatal(err)
		}
		log.Println("Cooling down for " + strconv.Itoa(cfg.CoolDown) + " seconds")
		time.Sleep(time.Duration(cfg.CoolDown) * time.Second)
	}
}
