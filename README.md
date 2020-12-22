# omg-frames-api

This is the backend of the [OMG Frames](https://github.com/dsc-x/omg-frames) having the register/login routes, and other related ones. 

Link to the front-end repo: [omg-frames](https://github.com/dsc-x/omg-frames)

Backend is running at: [http://104.236.25.178/api/v1](http://104.236.25.178/api/v1)

All the API endpoints are prefixed by `/api/v1` e.g `http://104.236.25.178/api/v1/login`

## Technologies used

**Framework :** `Flask` Reason being it is very lightweight and easy to set-up. Since it's a micro-framwork it has better performance and is very scalable.

**Database :** `Firebase realtime database` Easy to set-up and use. 

**Documentation :** `Flasgger` Flask extension that comes with Swagger UI embedded. Link to the repo [here](https://github.com/flasgger/flasgger)

## API Endpoints

For API documentation go to [http://104.236.25.178/apidocs/](http://104.236.25.178/apidocs/).

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

```
    omg-frames-api
    .
    ├── app
    │   ├── db.py
    │   ├── __init__.py
    │   └── routes.py
    ├── config.py
    ├── docs
    │   ├── getframes.yml
    │   ├── login.yml
    │   ├── postframes.yml
    │   └── register.yml
    ├── README.md
    ├── requirements.txt
    ├── sample.env
    └── server.py
```

