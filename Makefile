# Default target
.DEFAULT_GOAL := run

# Run the FastAPI server
run:
	uvicorn app.main:app --reload

# Format code (example: using black)
format:
	black app

# Run tests
test:
	pytest -v

# Install dependencies (using uv or pip)
install:
	uv pip install -r requirements.txt

# Clean up __pycache__
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +