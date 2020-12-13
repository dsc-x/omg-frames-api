# omg-frames-api

This is the backend of the [OMG Frames](https://github.com/dsc-x/omg-frames) having the register/login routes, and other related ones. 

## Technologies used

**Framework :** `Flask` Reason being it is very lightweight and easy to set-up. Since it's a micro-framwork it has better performance and is very scalable.

**Database :** `Firebase realtime database` Easy to set-up and use. 

## Development

- Clone the repo. 
```bash
$ git clone https://github.com/dsc-x/omg-frames-api
$ cd omg-frames-api
```

- Setup a python virtual environment (optional).
```bash
$ python3 -m venv venv/
$ source ./venv/bin/activate # activate the virtual environment
```

- Install the modules and libraries that will be used.
```bash
$ pip3 install -r requirements.txt
```

- Create a `.env` file in root of the project. You can refer to [sample.env](sample.env). 

- Finally run the command
```
$ flask run
```

This will start the local server in port 5000. 

## Project structure

    omg-frames-api
    ├── app
    |   ├── __init__.py
    │   └── routes.py
    ├── config.py
    ├── db.py
    ├── README.md
    ├── requirements.txt
    ├── sample.env
    └── server.py

## API Endpoints


| URL | METHOD | REQUEST BODY | RESPONSE | DESCRIPTION |
|---|---|---|---|---|
| `/register` | POST | JSON that has three field `name`, `email`, `password`. | - | If the email is not in the database then the email will be added with the password hashed. |
| `/login` | POST | JSON with `email` and `password` | JSON with a key `token` | Returns a `token` if the email and password matches else `401` |

>add `/api/v1` as prefix to the URL