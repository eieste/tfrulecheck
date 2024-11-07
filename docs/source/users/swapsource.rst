===========
Swap Source
===========



Terraform
=========


.. code-block:: hcl
   :lineos:
   :caption:

   @swapsource(remote_source="", remote_version="", local_source="")
   module {
      source = ""
   }


.. code-block:: hcl
   :lineos:
   :caption:

   @swapsource(remote_source="", remote_version="", local_source="")
   module {
      source = ""
      version = ""
   }





.. argparse::
   :module: tfutils.main
   :func: _get_parser_only
   :prog: tfutils
   :path: sourceswap