
from docutils.parsers.rst import Directive

import docutils.nodes
import sphinx.addnodes

class NodeNotFoundError(Exception):
    pass

class NodeFactory(object):

    def __init__(self, *args):

        self.sources = args

    def __getattr__(self, node_name):

        for source in self.sources:
            try:
                return getattr(source, node_name)
            except AttributeError:
                pass

        raise NodeNotFoundError(node_name)

class MayaHandle(object):

    def __init__(self, cmds):

        self.cmds = cmds

    def editorTemplate( self, *args, **kwargs ):

        self.cmds.editorTemplate( *args, **kwargs )


class DocHandle(object):

    def __init__( self, node_factory ):

        self.nodelist = []
        self.node_factory = node_factory

    def editorTemplate(self, *args, **kwargs):

        try:
            add_control = kwargs[ "addControl" ]
        except KeyError:
            return

        if add_control:
            parameter_name = args[0]
            self.nodelist.append( self.node_factory.Text( parameter_name ) )

    def nodes(self):

        return self.nodelist


class MayaNodeDirective(Directive):

    required_arguments = 1

    def run(self):

        try:
            module_name, function_name = self.arguments[0].split(":")
        except ValueError:
            # No ":" separator
            return []

        module = __import__( module_name )

        function = getattr( module, function_name )

        node_factory = NodeFactory( docutils.nodes, sphinx.addnodes )
        doc_handle = DocHandle( node_factory )
        function( "examplenode", doc_handle )

        return doc_handle.nodes()


# Setup
# -----

def setup(app):

    app.add_directive(
            "mayanode",
            MayaNodeDirective,
            )

