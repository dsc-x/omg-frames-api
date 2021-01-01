# iWasAt

This is the backend of the [iWasAt](https://github.com/dsc-x/omg-frames) having the register/login routes, and other related ones. 

Link to the front-end repo: [omg-frames](https://github.com/dsc-x/omg-frames)

Backend is running at: [https://api.iwasat.events/api/v1](https://api.iwasat.events/api/v1/)

All the API endpoints are prefixed by `/api/v1` e.g `https://api.iwasat.events/api/v1/login`

## Technologies used

**Framework :** `Flask` Reason being it is very lightweight and easy to set-up. Since it's a micro-framwork it has better performance and is very scalable.

**Database :** `Firebase realtime database` Easy to set-up and use. 

**Documentation :** `Flasgger` Flask extension that comes with Swagger UI embedded. Link to the repo [here](https://github.com/flasgger/flasgger)

## API Endpoints

For API documentation go to [https://api.iwasat.events/apidocs/](https://api.iwasat.events/apidocs/).

## Development

### Dockerfile

- Run the build command
```bash
make build
```
It will pull the docker image and install all the packages and modules.

- Run the docker instance
```bash
make run
```
By default it will map to port 5000.

- If you want to kill the docker instance
```bash
make kill
```

Then you can visit `http://0.0.0.0/apidocs` for the documentation

### Building from source

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
├── app
│   ├── db.py
│   ├── __init__.py
│   └── routes.py
├── config.py
├── docs
│   ├── deleteframes.yml
│   ├── getframes.yml
│   ├── login.yml
│   ├── postframes.yml
│   ├── register.yml
│   └── updateframes.yml
├── README.md
├── requirements.txt
├── sample.env
└── server.py
```

