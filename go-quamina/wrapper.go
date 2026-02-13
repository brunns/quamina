package main

/*
#include <stdlib.h>
*/
import "C"
import (
	"encoding/json"
	"sync"
	"unsafe"

	"quamina.net/go/quamina"
)

// Global state for managing Quamina instances
var (
	instances   = make(map[int]*quamina.Quamina)
	nextHandle  = 1
	instancesMu sync.RWMutex
)

// QuaminaNew creates a new Quamina instance and returns a handle to it.
// Returns 0 on error.
//
//export QuaminaNew
func QuaminaNew() C.int {
	q, err := quamina.New(quamina.WithPatternDeletion(true))
	if err != nil {
		return 0
	}

	instancesMu.Lock()
	defer instancesMu.Unlock()

	handle := nextHandle
	nextHandle++
	instances[handle] = q

	return C.int(handle)
}

// QuaminaFree destroys a Quamina instance.
//
//export QuaminaFree
func QuaminaFree(handle C.int) {
	instancesMu.Lock()
	defer instancesMu.Unlock()
	delete(instances, int(handle))
}

// QuaminaAddPattern adds a pattern to the Quamina instance.
// Returns NULL on success, or an error message that must be freed with QuaminaFreeString.
//
//export QuaminaAddPattern
func QuaminaAddPattern(handle C.int, patternID *C.char, patternJSON *C.char) *C.char {
	instancesMu.RLock()
	q, exists := instances[int(handle)]
	instancesMu.RUnlock()

	if !exists {
		return C.CString("invalid handle")
	}

	id := C.GoString(patternID)
	pattern := C.GoString(patternJSON)

	err := q.AddPattern(id, pattern)
	if err != nil {
		return C.CString(err.Error())
	}

	return nil
}

// QuaminaDeletePatterns removes all patterns with the given ID.
// Returns NULL on success, or an error message that must be freed with QuaminaFreeString.
//
//export QuaminaDeletePatterns
func QuaminaDeletePatterns(handle C.int, patternID *C.char) *C.char {
	instancesMu.RLock()
	q, exists := instances[int(handle)]
	instancesMu.RUnlock()

	if !exists {
		return C.CString("invalid handle")
	}

	id := C.GoString(patternID)

	err := q.DeletePatterns(id)
	if err != nil {
		return C.CString(err.Error())
	}

	return nil
}

// QuaminaMatchesForEvent matches an event against all patterns.
// Returns a JSON array of matching pattern IDs, or NULL on error.
// The returned string must be freed with QuaminaFreeString.
//
//export QuaminaMatchesForEvent
func QuaminaMatchesForEvent(handle C.int, eventJSON *C.char) *C.char {
	instancesMu.RLock()
	q, exists := instances[int(handle)]
	instancesMu.RUnlock()

	if !exists {
		return C.CString("[]")
	}

	event := []byte(C.GoString(eventJSON))

	matches, err := q.MatchesForEvent(event)
	if err != nil {
		return C.CString("[]")
	}

	// Handle nil or empty matches
	if matches == nil || len(matches) == 0 {
		return C.CString("[]")
	}

	// Convert matches to JSON array
	result, err := json.Marshal(matches)
	if err != nil {
		return C.CString("[]")
	}

	return C.CString(string(result))
}

// QuaminaFreeString frees a string returned by the library.
//
//export QuaminaFreeString
func QuaminaFreeString(str *C.char) {
	C.free(unsafe.Pointer(str))
}

// main is required for building a shared library
func main() {}
