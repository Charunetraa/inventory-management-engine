Inventory Management Engine

Overview

An object-oriented Python inventory management system demonstrating inheritance, encapsulation, polymorphism, custom exceptions, file persistence, and automated unit testing.

Features

- Add, search, update, list, and remove products.
- Support for physical and digital product types.
- Validate product data and stock operations.
- Handle invalid operations using custom exceptions.
- Persist inventory records in JSON and CSV formats.
- Automated tests using pytest.
- Code coverage measurement using pytest-cov.

Technologies

- Python 3.11+
- pytest
- pytest-cov
- JSON and CSV

Project Structure

- "main.py" — application entry point
- "inventory/models.py" — product hierarchy and validation
- "inventory/exceptions.py" — custom exception classes
- "inventory/manager.py" — inventory operations
- "inventory/storage.py" — JSON and CSV persistence
- "tests/test_inventory.py" — automated tests
- "requirements.txt" — testing dependencies

Installation

Install Python 3.11 or later, then install the dependencies:

python -m pip install -r requirements.txt

Run the Application

python main.py

Run Tests and Measure Coverage

python -m pytest --cov=inventory --cov-report=term-missing

Test Results

The current local test run passed all 16 tests and reported 97% coverage of the "inventory" package. Results may vary if the code or tests change.

Learning Outcomes

This project demonstrates object-oriented design, data validation, custom exceptions, JSON and CSV persistence, automated testing, and code coverage analysis.