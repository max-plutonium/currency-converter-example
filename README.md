# Currency converter example


Getting started
---------------


- Create a Python virtual environment.

    ``pyenv local 3.9.0``

    ``pip install --upgrade pip``

    ``pip install poetry``


- Install the project

    ``poetry install --no-root``


- Run tests

    ``APILAYER_API_KEY={your apilayer apikey value} poetry run pytest``


- Start the app

    ``APILAYER_API_KEY={your apilayer apikey value} poetry run start``


- [Get the swagger documentation](http://localhost:8000/docs)


- Build Docker image

    ``docker image build
        --build-arg GIT_COMMIT=$(git rev-parse --short HEAD) --build-arg IMAGE_TAG=$IMAGE_TAG
        -t $IMAGE_NAME:$IMAGE_TAG -f run/Dockerfile.app .``


- Run Docker image

    ``docker run --name converter --rm 
        -e APILAYER_API_KEY={your apilayer apikey value}
        -p 80:80/tcp
        $IMAGE_NAME:$IMAGE_TAG --host 0.0.0.0 --port 80``
