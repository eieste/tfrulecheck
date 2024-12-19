==========
Moved Date
==========




Terraform
=========


.. code-block:: hcl
   :linenos:

   moved {
      to = ""
      from = ""
   }



.. code-block:: hcl
   :linenos:

   # @moveddate(start="01-01-1970")
   moved {
      to = ""
      from = ""
   }



.. code-block:: hcl
   :linenos:

   # @moveddate(start="01-01-1970", expire="19-01-2038")
   import {
      to = ""
      from = ""
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
   :path: moveddate

