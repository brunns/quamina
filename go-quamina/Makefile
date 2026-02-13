.PHONY: all clean darwin linux windows

all: darwin

# Build for macOS (current platform for development)
darwin:
	go build -buildmode=c-shared -o libquamina.dylib wrapper.go

# Build for Linux
linux:
	GOOS=linux GOARCH=amd64 go build -buildmode=c-shared -o libquamina.so wrapper.go

# Build for Windows
windows:
	GOOS=windows GOARCH=amd64 go build -buildmode=c-shared -o libquamina.dll wrapper.go

clean:
	rm -f libquamina.dylib libquamina.so libquamina.dll libquamina.h
