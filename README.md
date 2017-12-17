## interviewDB API

A simple API for accessing interview questions, answers, hints, and categories. See [interviewdb](https://github.com/nginth/interviewdb) for the front-end.

### Installation

```bash
virtualenv venv
. venv/bin/activate
pip3 install -r requirements.txt
python3 main.py
```

### Testing

Create a postgresql database called "interviewdbtest" and have it accessible at port 5432 on localhost.

```bash
./run_tests.py
```
