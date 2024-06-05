package main

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"mime/multipart"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
)

func main() {
	http.HandleFunc("GET /ffmpeg", func(w http.ResponseWriter, r *http.Request) {
		getFfmpeg(w, r)
	})
	http.HandleFunc("POST /upload", func(w http.ResponseWriter, r *http.Request) {
		uploadVideo(w, r)
	})
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal(err)
	}
}

func getFfmpeg(w http.ResponseWriter, r *http.Request) {
	//args := []string{"-i transparent.gif -c:v libvpx -pix_fmt yuva420p -auto-alt-ref 0 transparent.webm"}
	cmd := exec.Command("ffmpeg", "-i", "input.gif", "-c:v", "libvpx", "-pix_fmt", "yuva420p", "-auto-alt-ref", "0", "transparent.webm")
	var cmdStdOut, cmdStdErr bytes.Buffer
	cmd.Stdout = &cmdStdOut
	cmd.Stderr = &cmdStdErr
	if err := cmd.Run(); err != nil {
		fmt.Println("stdout:", cmdStdOut.String())
		fmt.Println("stderr:", cmdStdErr.String())
		log.Println(err)
		w.WriteHeader(http.StatusInternalServerError)
	}
	if true {
		log.Println("stdout:", cmdStdOut.String(), "stderr:", cmdStdErr.String())
	}
	w.WriteHeader(http.StatusOK)
}

func uploadVideo(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
		return
	}

	// Parse the multipart form, with a max memory of 32 MB
	err := r.ParseMultipartForm(32 << 20)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Retrieve the file from form data
	file, handler, err := r.FormFile("video")
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	defer func(file multipart.File) {
		err := file.Close()
		if err != nil {

		}
	}(file)

	// Create a destination file
	dst, err := os.Create(filepath.Join("uploads", handler.Filename))
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer func(dst *os.File) {
		err := dst.Close()
		if err != nil {

		}
	}(dst)

	// Copy the uploaded file to the destination file
	_, err = io.Copy(dst, file)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	fmt.Println("File uploaded successfully")
}
