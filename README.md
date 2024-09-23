# TF-Rule-Checker

Allows Decorator ontop of HCL/Terraform Resources to check if some things are configured correctly


## @forcedremotesource

ID: TF01

```

# @forcedremotesource
module "sample" {
    source = "../../asamplemodule"
}

```