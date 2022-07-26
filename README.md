# E-commerce inventory management API

## Terminal commands

To run Makefile, you need to have the make command installed:

```
sudo apt-get install build-essential
```

Then simply run `make install` to initialize the environment (only necessary the first time you're running the app, or after installation requirements change).

To restart the app, run `make restart`.

To view logs, such as error messages, run `make logs`.

## Endpoints

Access http://localhost:5000/api/estoque to start using the API.

Postman is recommended for API testing.

## TODO next

- Validate that user login is not duplicated before sending to DB
