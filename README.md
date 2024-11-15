# TfUtility

[![Validate](https://github.com/eieste/tfutility/actions/workflows/validate.yml/badge.svg)](https://github.com/eieste/tfutility/actions/workflows/validate.yml)


Documentation:

tfutility allows performing commands on terraform/tofu files.
This commands can be different things. Currently, there are possibilities to check if a module block has remote sources.
Or  import or moved blocks have creation dates on them.

It also allows TF-Stack Developers to swap the sources of marked modules.

For all of these Functions, show the Samples Below or read the [Documentation](https://eieste.github.io/tfutility/)



## Setup

### Install via PIP

Install tfutility via pip

```
$ pip install tfutility
```
Run tfutility in command line
```
$ tfutility
```
for detailed Examples visit the [Documentation](https://eieste.github.io/tfutility/)

### Use with Docker
```
docker run -it --rm -v $(pwd):/workspace ghcr.io/eieste/tfutility:1.0.9 forcedremotesource /workspace
```

### Use with pre-commit



## Quick-Reference

The following Options are currently available

### @importdate

The importdate decorator should help you to keep your code clean.
You should be able to delete imports after the stack has been successfully rolled out. this decorator is useful to avoid removing import blocks too early or forgetting them

Example:
```terraform

    # @importdate(create="01-12-1970", expire="05-01-1971)
    import {
        ...
    }

```

Execute the following command to check if the import was "expired"
```bash
tfutility importdate /workspace
```

you can also overwrite the expire date with your own duration like:
```bash
tfutility importdate --expire-after 60 /workspace
```
The `--expire-after` value is in Days.

If --allow-failure is not set the Application wil exit with `exitcode` 1
and without --silent it logs all expired imports


### @moveddate

This has the same Reason like @importdate

Decorator in Terraform

```terraform

    # @moveddate(create="01-12-1970", expire="05-01-1971)
    moved {
        ...
    }

```

Execute the following command to check if the moved was "expired"
```bash
tfutility moveddate /workspace
```


### @sourceswap

This command allows to swap between remote and local sources.

```terraform

    # @sourceswap(remote_version="0.0.1", remote_source="example.com/examplemodule/local", source="../../examplemodule")
    module {
        source = "../../examplemodule"
    }

```

To Swap all Sources in your workspace you can execute the following command

```bash
tfutility sourceswap --swap-to local /workspace
tfutility sourceswap --swap-to remote /workspace
```



### @forcedremotesource


Decorator in Terraform

```terraform

    # @forceremotecheck
    module {
        source = "../
    }

```

Execute the following command to check if all module blocks has an remote source.
```bash
tfutility forcedremotesource /workspace
```
