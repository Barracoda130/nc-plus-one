# Overview
I have no idea what this does yet - something about booking an event or smth idk

# Setup 
## Database setup
1. With postgres installed locally run the following command to create the database:
```shell
psql -f db/setup.sql
```
2. Run  to create the database tables and seed the database
```shell
python main.py --seed
```

# Run
## Running the main app
To run the application run the following command:
```shell
python main.py
```

## Running the tests
To run the tests type run the following command from within the root directory
```shell
pytest
```
If there is an issue with the tests and you wish to use the VSCode debugger, you can execute the main.py file with the command line arg `--debug-tests`.
