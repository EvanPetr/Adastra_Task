# Adastra Task

## Getting Started
The Service Consists of several components:
- Flask web application which serves an API.
- PostgresSQL database which handles persistence.
- Nginx which serves as a proxy.

### Run App
```
$ make run
```

### Connect to database
Creds:
- user: postgres
- password: pass
- db: adastra

```
$ make db.shell
```

### Stop App
```
$ make stop
```

### Run linter
```
$ make lint
```

### Run tests
```
$ make test
```

### Run tests coverage
```
$ make test.coverage
```