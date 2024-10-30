# TFUtils provides different tools for Terraform Developers

## Installation

```
$ pip install -r requirements.txt

$ python setup.py install
```

## Development

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

### Environment Setup

The following demonstrates setting up and working with a development environment:

```
### create a virtualenv for development

$ make virtualenv

$ source env/bin/activate


### run tfutils cli application

$ tfutils --help


### run pytest / coverage

$ make test
```


### Releasing to PyPi

Before releasing to PyPi, you must configure your login credentials:

**~/.pypirc**:

```
[pypi]
username = YOUR_USERNAME
password = YOUR_PASSWORD
```

Then use the included helper function via the `Makefile`:

```
$ make dist

$ make dist-upload
```

## Deployments

### Docker

Included is a basic `Dockerfile` for building and distributing `TF-Utils`,
and can be built with the included `make` helper:

```
$ make docker

$ docker run -it tfutils --help
```





# TF-Rule-Checker

Allows Decorator ontop of HCL/Terraform Resources to check if some things are configured correctly

## @tfmoduleupdate
## @importdate
## @moveddate
## @sourcechange
## @forcedremotesource

ID: TF01

```

# @forcedremotesource
module "sample" {
    source = "../../asamplemodule"
}

```