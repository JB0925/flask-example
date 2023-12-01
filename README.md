# Flask-Example

Thanks for checking out Flask-Example. The sole purpose of this app is to be a demo app for Springboard students. It is purposely silly, so don't focus too much on the subject matter!

My hope is that this app will show how to:

- Use logging
- Use proper Python import order
- Show testing
- Show how to create modules
- Show how to use type annotations
- Show one way to structure and organize an app
- Show other best practices, such as using constants instead of raw strings, and custom errors that are more explicit.

Had I more time, I might have:

- Added more tests
- Used `Pydantic` for runtime type checking
- Used `mypy` for static type checking
- And probably more.

## What is this app about?

The app allows users to create "animals" via an API, but only some animals are Pets. Only pets can be saved to the database. Did I mention that this was a silly app? :)

## How can I run this app?

This app was built using Python 3.12.0. Most likely, any version of Python 3.10.\* + will work. To run it.

- Create a `.env` file. In it, you need to have the following keys: `SECRET_KEY=whatever you want` and `SQLALCHEMY_DATABASE_URI=postgresql:///pets_demo`
- Create a virtual environment via `python3 -m venv venv`
- Activate it. On Unix systems, that can be done via `source venv/bin/activate`.
- Install the dependencies via `pip install -r requirements.txt`.
- Ensure that you have a running Postgres instance.
- Create a database called `pets_demo`.
- Run `flask run` in your terminal.

## How can I run the tests?

- From the root of the repo, simply type `pytest` and press enter/return.

## Sample curl calls

To create a pet, you can run:

```
curl -v http://localhost:5000/pets -H 'content-type: application/json' -d '{"name": "Al", "age": 5, "species": "DOG"}'
```

To get one pet, you can run:
Note that the `<id>` is the ID returned from
the previous command.

```
curl -v http://localhost:5000/pets/<id> -H 'content-type: application/json'
```

To get all pets, you can run:
Note: If you do not have `jq`, you can cut out the `| jq .` part. It just makes the JSON prettier.

```
curl -v http://localhost:5000/pets -H 'content-type: application/json' | jq .
```

To get the oldest pet, you can run:

```
curl -v http://localhost:5000/pets/oldest -H 'content-type: application/json'
```
