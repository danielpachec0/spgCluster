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
	"strconv"
	"strings"
	"time"
)

func main() {
	//curl -X POST localhost:8080/upload -F "video=@/mnt/c/Users/Daniel.Pacheco/Videos/input.gif" -O  -F "command=-movflags faststart -pix_fmt yuv420p"
	http.HandleFunc("POST /upload", func(w http.ResponseWriter, r *http.Request) {
		uploadVideo(w, r)
	})
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal(err)
	}
}

// func ffmpeg(args []string) error {
func ffmpeg(inputPath string, outputPath string, commandStr string) error {
	args := []string{"-i", inputPath}
	args = append(args, strings.Split(commandStr, " ")...)
	args = append(args, outputPath)

	cmd := exec.Command("ffmpeg", args...)
	var cmdStdOut, cmdStdErr bytes.Buffer
	cmd.Stdout = &cmdStdOut
	cmd.Stderr = &cmdStdErr
	if err := cmd.Run(); err != nil {
		fmt.Println("stdout:", cmdStdOut.String())
		fmt.Println("stderr:", cmdStdErr.String())
		log.Println(err)
		return err
	}
	if true {
		log.Println("stdout:", cmdStdOut.String(), "stderr:", cmdStdErr.String())
	}
	return nil
}

func uploadVideo(w http.ResponseWriter, r *http.Request) {
	id := strconv.FormatInt(time.Now().UnixNano(), 10)
	inputPath := "uploads/" + id + ".gif"
	outputPath := "outputs/" + id + ".mp4"

	if r.Method != "POST" {
		http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
		return
	}

	err := r.ParseForm()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Parse the multipart form, with a max memory of 32 MB
	err = r.ParseMultipartForm(32 << 20)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	command := r.FormValue("command")

	formFile, _, err := r.FormFile("video")
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	defer func(file multipart.File) {
		err := file.Close()
		if err != nil {
			log.Fatalf("Failed to close formFile: %s", err)
		}
	}(formFile)

	inputFile, err := os.Create(inputPath)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer func(dst *os.File) {
		err := dst.Close()
		if err != nil {

		}
		err = os.Remove(inputPath)
		if err != nil {
			log.Printf("Failed to remove formFile: %s", err)
		}
	}(inputFile)

	_, err = io.Copy(inputFile, formFile)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	err = ffmpeg(inputPath, outputPath, command)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	outputFile, err := os.Open(outputPath)
	defer func(outputFile *os.File) {
		err := outputFile.Close()
		if err != nil {
			log.Fatal("F")
		}
		err = os.Remove(outputPath)
		if err != nil {
			log.Printf("Failed to remove formFile: %s", err)
		}
	}(outputFile)
	if err != nil {
		http.Error(w, "File not found.", 404)
		return
	}

	stat, err := outputFile.Stat() // Get the file info
	if err != nil {
		http.Error(w, "Could not obtain stat", http.StatusInternalServerError)
		return
	}

	// Set the headers
	w.Header().Set("Content-Disposition", "attachment; filename=vid.mp4")
	w.Header().Set("Content-Type", "video/mp4")
	w.Header().Set("Content-Length", fmt.Sprint(stat.Size()))

	// Serve the formFile
	http.ServeContent(w, r, outputPath, stat.ModTime(), outputFile)
}
