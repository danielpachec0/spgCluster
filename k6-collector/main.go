package main

import (
	"database/sql"
	"encoding/json"
	_ "github.com/mattn/go-sqlite3"
	"io"
	"log"
	"net/http"
)

type Test struct {
	UUID  string `json:"uuid"`
	Start string `json:"start"`
	End   string `json:"end"`
	Data  string
}

func initializeMap(db *sql.DB) map[string]bool {
	testsMap := make(map[string]bool)
	tests, err := queryTests(db)
	if err != nil {
		log.Fatal(err)
	}
	for _, test := range tests {
		testsMap[test.UUID] = true
	}
	return testsMap
}

func initializeDB() (*sql.DB, error) {
	db, err := sql.Open("sqlite3", "db.db")
	if err != nil {
		return nil, err
	}

	_, err = db.Exec(
		"CREATE TABLE IF NOT EXISTS tests (uuid TEXT PRIMARY KEY,start TEXT NOT NULL, end TEXT NOT NULL, data BLOB)")
	if err != nil {
		return nil, err
	}
	return db, nil
}

func main() {

	db, err := initializeDB()
	if err != nil {
		log.Fatal(err)
	}

	testsMap := initializeMap(db)

	http.HandleFunc("POST /tests", func(w http.ResponseWriter, r *http.Request) {
		postTest(w, r, db, testsMap)
	})
	http.HandleFunc("GET /tests", func(w http.ResponseWriter, r *http.Request) {
		getTests(w, r, db)
	})

	log.Println("Server starting on port 8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal(err)
	}
}
func postTest(w http.ResponseWriter, r *http.Request, db *sql.DB, dict map[string]bool) {
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error reading request body", http.StatusInternalServerError)
		return
	}
	defer func(Body io.ReadCloser) {
		err = Body.Close()
		if err != nil {
			log.Println(err)
		}
	}(r.Body)

	var test Test
	if err := json.Unmarshal(body, &test); err != nil {
		http.Error(w, "Error parsing JSON body", http.StatusBadRequest)
		return
	}

	if !dict[test.UUID] {
		dict[test.UUID] = true
		go func() {
			err = storeTest(test, db)
			if err != nil {
				log.Println(err)
			}
		}()
	}

	_, err = w.Write([]byte("ok"))
	if err != nil {
		http.Error(w, "Internal error", http.StatusBadRequest)
	}
}

func storeTest(test Test, db *sql.DB) error {
	insertSQL := `INSERT INTO tests(uuid, start, end) VALUES (?, ?, ?)`
	statement, err := db.Prepare(insertSQL)
	if err != nil {
		return err
	}

	defer func(statement *sql.Stmt) {
		err = statement.Close()
		if err != nil {
			log.Println(err)
		}
	}(statement)

	_, err = statement.Exec(test.UUID, test.Start, test.End)
	if err != nil {
		return err
	}
	return nil
}

func queryTests(db *sql.DB) ([]Test, error) {
	rows, err := db.Query("SELECT uuid, start, end FROM tests")
	if err != nil {
		return nil, err
	}
	defer func(rows *sql.Rows) {
		err = rows.Close()
		if err != nil {
			log.Println(err)
		}
	}(rows)

	var tests []Test
	for rows.Next() {
		var test Test
		if err := rows.Scan(&test.UUID, &test.Start, &test.End); err != nil {
			return nil, err
		}
		tests = append(tests, test)
	}
	if err = rows.Err(); err != nil {
		return nil, err
	}
	return tests, nil
}

func getTests(w http.ResponseWriter, r *http.Request, db *sql.DB) {
	tests, err := queryTests(db)
	response := ""
	for _, test := range tests {
		response = response + "(\"" + test.Start + "\", \"" + test.End + "\"),\n"
	}
	_, err = w.Write([]byte(response))
	if err != nil {
		http.Error(w, "Internal error", http.StatusBadRequest)
	}
}
