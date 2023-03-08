# Dashboard
A simple design for a plotly-dash app with sklearn running within a docker container deployed using CI/CD.
 
- Docker base image: Python 3.11-buster
- Framework: Dash
- Server: Gunicorn

 
### Using [pre-commit-hooks](https://pre-commit.com/)
- [flake8](https://github.com/pycqa/flake8)
- [black](https://github.com/ambv/black)
- [isort](https://github.com/pycqa/isort)
- [detect-private-key](https://github.com/pre-commit/pre-commit-hooks#detect-private-key)
- [bandit](https://github.com/PyCQA/bandit)

### Structure
```
├── .github
│   └── workflows
│        └── main.yml
│
├── project
│   ├── app
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── functions.py
│   │   └── assets
│   ├── tests
│   │   └── test_functions.py
│   ├── Dockerfile
│   ├── Dockerfile.prod
│   └── requirements.txt
│
├── setup.cfg
├── .pre-commit-config.yaml
├── .gitignore
│
└── README.md
```

### Setup github secrets

Start by setting up the [Github Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) needed for the deployment pipeline:

**GCP_EMAIL**: the email from the service account you created, formatted like: $ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com

**GCP_PROJECT_ID**: your project name

**GCP_CREDENTIALS**: your key.json (copy paste the content)

**GCP_APP_NAME**: the name of your app (for within the GCRe)

With these secrets we can build the CI/CD workflow through Github Actions.

### Deploy to google cloud run through github actions - steps
1. build a Docker image
2. push container 
2. write deployment part in pipeline
3. limit billing and cleanup

#### Limit billing through cleanups

For the app to run I have activated multiple services. 
Take a look at the services described below and how to monitor and limit costs.
Google Cloud Storage ([GCS](https://cloud.google.com/storage/pricing#europe)) costs, GCRe is storing the images of your containers within GCS. With a GB costing around 2 cents per month (in Europe) this should not cost you much if you keep the GCRe clean. We can make sure no old images linger in your GCRe by adding the following line that removes images without the ‘latest’ tag:

`name: Clean up old images` in main.yml

### Improvements that could be done

- **Load Balancing and Scaling**: Depending on the traffic demand, we can set up a load balancer to distribute the traffic to multiple instances of the serverless service to handle the load. This helps in ensuring high availability and reliability of the app. Additionally, we can configure auto-scaling policies to scale up or down the instances based on the traffic demand.
- **Security**: Security is critical for any production-ready app. We can use tools like OWASP ZAP to conduct security scans and identify any vulnerabilities in the app. Additionally, we can use SSL/TLS encryption to secure the communication between the clients and the server.
- **Logging and Monitoring**: We can set up a centralized logging and monitoring system to track the performance and behavior of the app in production. This helps in identifying any potential issues or errors in real-time and ensures the app's smooth functioning
- **Code Reviews**: One of the best practices to ensure code quality is to conduct code reviews before merging any code changes into the production branch. This can be done using pull requests or code reviews in Github. This helps in catching any potential issues or bugs before they reach the production environment.
- **End to end testing**: We could write end to end tests (not just unit tests) using dash.testing, cypress and with web driver etc
- Using **multi-step** building can speed up deployment.
- The docker image can be made **smaller** with the right tweaks, meaning faster building and deployment (Alpine base image, skip pip cache etc.).

By following these best practices, we can ensure the quality, reliability, and security of the app in production.

### Run locally
To run the image locally, cd into the dashboard folder and:
```
docker build -t dashboard project/.
```
And run the container
```
docker run -p 8050:8050 dashboard
```
You can find to the app on your local machine http://localhost:8050/ (or localhost:8050). This way the image is created using the Dockerfile, instead of the Dockerfile.prod.