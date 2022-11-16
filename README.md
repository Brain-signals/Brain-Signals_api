# Brain-Signals API

## Use the API online [here.](https://brain-signals-api-rxbyapf3mq-ew.a.run.app)

Our API is available online through google cloud run.
Here are the different endpoints :

`-/list` - See all avalaible models

- _requires no query parameters_

`-/model` - See settings of a selected model

- **model_id** _to specify a model id (ex : 20220902_142838_ONBJ)_

`-/predict` - Select a model and make a prediction using a nifti file

- **model_id** _to specify a model id (ex : 20220902_142838_ONBJ)_
- you also need to provide a nifti file (unavalaible via HTTP, use FastApi UI at `/docs` endpoint)


***

## Use the API locally.

<details>
  <summary>Setup</summary>
<br/>

Please follow this guidelines to setup everything you need after you cloned the project.

### Create the virtualenv

```
pyenv virtualenv brain-signals-api && pyenv local brain-signals-api
```
### Registry folder

If it doesn't exist, create a `.registry` directory that will contain all trained models. Then create an `LOCAL_REGISTRY_PATH` environment variable pointing to this directory. (No slash at the end.)

Example .env file :
```
LOCAL_REGISTRY_PATH=/home/<user>/code/<githubuser>/Brain-Signals/.registry
```
### Run the API

You can now start the api using :
```
make run_api
```
And use it via the default local [link.](http://127.0.0.1:8000/)
