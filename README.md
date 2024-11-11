# TfUtility

[![Validate](https://github.com/eieste/tfutility/actions/workflows/validate.yml/badge.svg)](https://github.com/eieste/tfutility/actions/workflows/validate.yml)


Documentation: https://eieste.github.io/tfutility/


provides different tools for Terraform Developers

## Installation

```
$ pip install tfutility
```

## Docker

```
docker run -it --rm -v $(pwd):/workspace ghcr.io/eieste/tfutility:1.0.9 forcedremotesource /workspace
```

# TF-Rule-Checker

Allows Decorator ontop of HCL/Terraform Resources to check if some things are configured correctly

## @tfmoduleupdate
## @importdate
## @moveddate
## @sourcechange
## @forcedremotesource
