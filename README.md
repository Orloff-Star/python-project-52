<h1>Task Manager</h1>

[Task_manager](https://python-project-52-r60m.onrender.com/) – This is a site that allows you to create and track tasks.

### Hexlet tests and linter status:
[![Actions Status](https://github.com/Orloff-Star/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Orloff-Star/python-project-52/actions)

The application is available at: [https://python-project-52-r60m.onrender.com](https://python-project-52-r60m.onrender.com)

## About

A task management web application built with Python and Django framework. It allows you to set tasks, assign performers and change their statuses. Registration and authentication are required to work with the system.


## Installation


### Prerequisites

#### Python

Before installing the package make sure you have Python version 3.10 or higher installed:

```bash
>> python --version
Python 3.10+
```

#### Poetry

The project uses the Poetry dependency manager. To install Poetry use its [official instruction](https://python-poetry.org/docs/#installation).

#### PostgreSQL / SQLite

There are two main options for using a database management system for this project: **PostgreSQL** and **SQLite**.

PostgreSQL is used as the main database management system. You have to install it first. It can be downloaded from [official website](https://www.postgresql.org/download/) or installed using Homebrew:
```shell
>> brew install postgresql
```

_Alternatively you can skip this step and use **SQLite** database locally._

### Application

To use the application, you need to clone the repository to your computer. This is done using the `git clone` command. Clone the project:

```bash
>> git clone git@github.com:Orloff-Star/python-project-52.git && cd Task_manager
```

After that install all necessary dependencies:

```bash
>> make install
```

Create `.env` file in the root folder and add following variables:
```dotenv
DATABASE_URL=postgresql://{provider}://{user}:{password}@{host}:{port}/{db}
SECRET_KEY={your secret key} # Django will refuse to start if SECRET_KEY is not set
ALLOWED_HOSTS = 'webserver, localhost, 127.0.0.1:8000, 0.0.0.0'
DEBUG = True
```
_If you choose to use **SQLite** DBMS, do not add `DATABASE_URL` variable._

To create the necessary tables in the database, start the migration process:
```bash
>> make migrate
```

---

## Usage

Start the Gunicorn Web-server by running:

```shell
>> make start
```

By default, the server will be available at http://0.0.0.0:8000.

It is also possible to start it local in development mode using:

```shell
>> make dev
```

The dev server will be at http://127.0.0.1:8000.

