# refive-backend-challenge

1. Receipt create API only accepts `.txt` file extension.
2. Necessary model has been provided to store parsed receipt, for .txt to pdf conversion used a 3rd party support.
3. Authentication has been done with TokenAuthorization based approach. Could have gone with simpleJWT but didn't want to complicate it.
4. `Poetry` has been used for dependency management as it is sctrict to version overlaping issues.
5. No luck with binary data upload I am only accepting text files.
6. New separator can be added to the function parameter easily.
7. Necessary unit tests code has been provided.

# Setup

1. Install poetry, go to the repo and write `poetry shell` and then `poetry install`.
2. Create a super user as `python manage.py createsuperuser`.
3. Run the server as `python manage.py runserver 0.0.0.0:8000`.
4. For test run `python manage.py test`.
5. Import postman collection from the repo and test. You can also see the admin panel from `localhost:8000/admin`

Enjoy!
