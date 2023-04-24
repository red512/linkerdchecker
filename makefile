.PHONY: clean build

# Remove the dist directory
clean:
	rm -rf dist
	rm -rf build

# Build the binary using PyInstaller
build:
	pyinstaller --onefile main.py