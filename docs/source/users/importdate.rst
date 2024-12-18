===========
Import Date
===========

This command check if every tf `import <TF_IMPORT_BLOCK_>`_ block has an defined decorator above
This decorator must contain an date when the block was created.
It allows the detection of old import blocks which can be remoted at a certain point in time


**Szenario**

If you want to import already existing cloud resources into your terraform you can use import blocks in your code.
If this blocks are used it is a good idea to remove them after a specific time or after it could be ensured that these blocks are taken by terraform.
By using the first option ( after a specific time ) this Command can help you.

By executing ``tfutility importdate .`` it can be ensured every import block has an decorator which contains a create date.
If these create date are expired ( defined by an additional expire date or an duration command line argument ) these checks will be fail until this import block is removed


Terraform
=========

.. code-block:: hcl
   :linenos:

   #$ cat test.tf
   import {
      to = "resource.aws_s3_bucket.example"
      id = "arandoms3bucket"
   }

.. code-block:: hcl
   :linenos:

   # @importdate(start="01-01-1970")
   import {
      to = ""
      id = ""
   }

.. code-block:: hcl
   :linenos:

   # @importdate(start="01-01-1970", expire="19-01-2038")
   import {
      to = ""
      id = ""
   }

you can also overwrite the expire date with your own duration like:
```bash
tfutility moveddate --expire-after 60 /workspace
```
The `--expire-after` value is in Days.

If --allow-failure is not set the Application wil exit with `exitcode` 1
and without --silent it logs all expired moved blocks



.. argparse::
   :module: tfutility.main
   :func: _get_parser_only
   :prog: tfutility
   :path: importdate


.. _TF_IMPORT_BLOCK: https://developer.hashicorp.com/terraform/language/import