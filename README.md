# Bracket Picker

Fill out a March Madness Bracket with a prompt.

## Setup

If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

1. Clone this repository

2. Navigate into the project directory

   ```bash
   $ cd bracket-picker
   ```

3. Create a new virtual environment

   ```bash
   $ virtualenv virt
   $ source virt/bin/activate
   ```

4. Install the requirements

   ```bash
   $ pip install -r requirements.txt
   ```

5. Make a copy of the example environment variables file

   ```bash
   $ cp .env.example .env
   ```

6. Add your OpenAI API key to the newly created .env file

## CLI

1. Run the application

    ```bash
    $ ./cli.sh
    ```

## Lambda Deployment

1. Build docker image

   ``` bash
   $ docker build --platform linux/arm64 -t ${DOCKER_IMAGE} .
   ```

2. Run docker image

   ```bash
   $ docker run --platform linux/arm64 --env-file=.env -p 9000:8080 --name ${DOCKER_CONTAINER} ${DOCKER_IMAGE}
   ```

3. Test function

   ```bash
   $ curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
   ```

4. Login to aws ecr

   ```bash
   $ aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
   ```

5. Create docker tag

   ```bash
   $ docker tag ${DOCKER_IMAGE}:latest ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${DOCKER_IMAGE_REPO}:latest
   ```

6. Push docker image

   ```bash
   $ docker push ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${DOCKER_IMAGE_REPO}:latest
   ```

For more information on deployments, refer to the [deployment docs](https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-create).

## Contributing

All contributions are welcome! Reach out for more information.