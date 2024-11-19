===========
Swap Source
===========



Terraform
=========


.. code-block:: hcl
   :linenos:

   # @swapsource(remote_source="", remote_version="", local_source="")
   module {
      source = ""
   }


.. code-block:: hcl
   :linenos:

   # @swapsource(remote_source="", remote_version="", local_source="")
   module {
      source = ""
      version = ""
   }

.. argparse::
   :module: tfutility.main
   :func: _get_parser_only
   :prog: tfutility
   :path: sourceswap