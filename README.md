# Python Weather API

## API Developement Guide

### Installation Requirements

---

- make or (cmake for windows)
- AWS cli
- AWS sam cli
- docker
- python 3.9
- python packages:
  - pipenv
  - pre-commit

### Connection keys file

---

Here we are using a json file so we can use it in the deployment and creation of our AWS services. Create a env.json file in the root directory to be read by your tests and to be used for local integration testing with SAM CLI. You **MUST** create a env.json file to be able to use this package.

- [Weather Unlocked HomePage](https://developer.weatherunlocked.com)
- [Weather Unlocked API Documentation](https://developer.weatherunlocked.com/documentation/localweather)

Json file example of env.json example after you update the app ID and Keys.

```json
{
  "Function": {
    "WEATHER_API_URL": "http://api.weatherunlocked.com/api",
    "WEATHER_API_APP": "77....",
    "WEATHER_API_KEY": "9d67f2...."
  }
}
```

### Running, Installing, and Developing

---

Use make and the makefile to easily setup and test the service.

```bash
make install-dev
make lint
make test
```

### Local Integration testing

---

With SAM CLI we have the ability to standup a local API and run REST requests.

```bash
make start
```

This is a basic curl command that can be run locally.

```bash
curl 'http://127.0.0.1:3000/weather?latitude=47.58&longitude=-122.30&days=3'
```

Here is an example response from the working service.

```bash
StatusCode        : 200
StatusDescription : OK
Content           : {"47.58, -122.3":[{"24/11/2022":{"announcement":"Brr, it's cold.","high":17.5,"low":9.0,"weather":"Overcast skies"}},{"25/11/2022":{"announcement":"Brr, it's cold.","high":23.2,"low":4.2,"weather":"Lig...
RawContent        : ...
```

### Using pregenerated Event Json files

---

TODO: Spend more time vetting event.json files

To use basic event json files use make with the pre-configured integration test json files. This is currently more of a work in progress.

```bash
make integration
```

## Deployment

---

TODO: Deploy requires a full AWS account and AWS CLI setup to successfully deploy the Lambda.

After you have done unit testing and local integration testing with `sam local start-api`
You'll need to setup AWS CLI to correctly auth to allow SAM CLI to use its deployment integrations.

```bash
make deploy
```
