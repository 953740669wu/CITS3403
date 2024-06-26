# Pet Forum Web Application

## Purpose
This web application serves as a dynamic forum for pet lovers, providing a platform for sharing stories, asking questions, and organizing pet-related events. It's designed to facilitate community interaction and support among pet owners, leveraging a user-friendly interface with functionalities such as event postings, comment sections, and user profiles.

## Team Members

| UWA ID     | Name        | GitHub Username           |
|------------|-------------|---------------------------|
| 22823318   | Junyi Wu    | [953740669wu](https://github.com/953740669wu) |
| 22935319  | Xincheng Li | [xinchengli1112](https://github.com/xinchengli1112) |
| 23701834   | Shuai Shao  | [ShuaiShao20010902](https://github.com/ShuaiShao20010902) |
| 23950897   | Yunhao Jin  | [YunhaoJin02](https://github.com/YunhaoJin02) |

## Launch Instructions
To launch the application:
1. Clone the repository
2. Navigate to the project directory
3. Set up virtual environment properly: for instance, using MacOS. Perform following command: `python3 -m venv venv` and then `source venv/bin/activate`
4. Install dependencies: `pip install -r requirement.txt`
6. Start the server: `flask run`
7. Access the application via `http://localhost:5000` in your web browser.

## Solution for possible issue with database
- `flask db init` initializes the migration scripts.
- `flask db migrate` detects changes in the models and creates migration scripts.
- `flask db upgrade` applies the migration scripts to the database.

## Testing Instructions
To run the tests:
1. Ensure you are in the project root directory.
2. Run the tests using the command as follows:
3. `python -m unittest tests.test_models`
4. `python -m unittest tests.test_routes`

These instructions provide a comprehensive guide to getting the application up and running on a local development environment and ensuring its functionality through tests.
