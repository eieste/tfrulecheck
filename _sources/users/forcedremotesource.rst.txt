====================
Forced Remote Source
====================

This Decorator enforces that  `module <TF_MODULE_BLOCK_>`_. have remote sources.
It is usefull in pre-commit hooks and development scenatios.
   


**Szenario:**

You are developing a large terraform/tofu project with different modules thre are pushed to an terraform module registry.
But for development purposes you linked the module localy together.

With this Decorator you can ensure only a version of the remote source module are pushed to git.
( If you use the check for this decorator in your pre-commit settings )


Terraform
=========

Write the following Decorator above modules to enforce this module must have a local path to his source.

This decorator works only above `module` blocks. It has no additional parameters

Example usage
``# @forcedremotesource``


The following Code tells tfutility this module should have an remote source.
But as you can see the module has an local path 

.. code-block:: hcl
   :linenos:
   :caption: test.tf

   # @forcedremotesource
   module "samplemodule" {
      source = "../local/path"
   }

shell:

.. code-block:: bash
   :linenos:

   tfutility forcedremotesource test.tf
   ERROR: Module Block had no Version Defined in main.tf:4
   ERROR: Module Block has no Remote Source in main.tf:4



so the following command loggs error and exit the whole application with an exit code 1

.. code-block:: hcl
   :linenos:
   :caption: test.tf

   # @forcedremotesource
   module "samplemodule" {
      source = "remoteurl@example.com"
   }

This raises an version missing error

.. code-block:: sh
   :linenos:

   $ tfutility forcedremotesource test.tf
   2024-11-18 23:05:25 ERROR: Module Block has no Remote Source in test.tf:4


Its possible to prevent error messages or exit 1 status codes with the --silent and --allow-failure arguments


Command Line Arguments
======================


Usage in Terraform


.. argparse::
   :module: tfutility.main
   :func: _get_parser_only
   :prog: tfutility
   :path: forcedremotesource



.. _TF_MODULE_BLOCK: https://developer.hashicorp.com/terraform/language/modules
    