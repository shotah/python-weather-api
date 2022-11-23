# python_API Example for Adobe

## Setup

### Requirements

* make or (cmake for windows)
* AWS cli
* AWS sam cli
* docker
* python 3.9
* python packages:
  * pipenv
  * pre-commit

### .env file for local keys

Create a .env file in the root directory and add your keys from weatherunlocked.com to allow API to access the Weather API. Specifically **Weather data** from weatherunlocked.

URL: <https://developer.weatherunlocked.com/>
DOCUMENTATION: <https://developer.weatherunlocked.com/documentation/localweather>

Example: http://api.weatherunlocked.com/api/current/51.50,-0.12?app_id={APP_ID}&app_key={APP_KEY}

```json
# Development settings
WEATHER_API_URL=http://api.weatherunlocked.com/api
WEATHER_API_APP=77...
WEATHER_API_KEY=97c42...
```

### Running Install and Development tools

run install, linting, and unit tests

```bash
make install-dev
make lint
make test
```

### Local Integration testing

To stand up the API as it would be as a lambda behind API gateway use the make start cmd.

```bash
make start
```

To use basic event json files use make with the pre-configured integration test json files.

```bash
make integration
```

## Deployment

After you have done unit testing and local integration testing with `sam local start-api`
You'll need to setup AWS CLI to correctly auth to allow SAM CLI to use its deployment integrations.
