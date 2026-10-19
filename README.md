# Overview
I have no idea what this does yet - something about booking an event or smth idk

# Setup
## Database setup
With postgres installed locally run the following commands to create and setup the database:
```shell
createdb nc_plus_one
psql -d nc_plus_one -f db/setup.sql
```