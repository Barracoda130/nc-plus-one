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