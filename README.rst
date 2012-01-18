
sphinx-maya-node
================

A Sphinx extension which provides a directive to automatically extract a node's
documentation from an appropriately written Attribute Editor Template.

The directive is designed to extract and format the per-control annotations from
the Attribute Editor and can only work if the Attribute Editor Template has been
written in Python.

Status
------

The code is in early stages and hasn't be tested with complex production
plugins.

Why?
----

It is always a shame to document something twice, so if you have complete
annotations on your Attribute Editor controls then it makes sense to reuse them
for the project's official documentation.

How?
----

You use the ``mayanode`` directive in you Sphinx docs in the following way::

   .. mayanode:: <module>:<function>

Where ``<module>`` is the name of the module in which your Attribute Editor
Template code is written and ``<function>`` is the entry function in which it
resides.


