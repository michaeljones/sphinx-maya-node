
from docutils.parsers.rst import Directive
from docutils.statemachine import ViewList

import docutils.nodes
import sphinx.addnodes
import textwrap
import re

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


class RstContentCreator(object):

    def __init__(self, list_type, dedent):

        self.list_type = list_type
        self.dedent = dedent

    def __call__(self, text):

        # Remove the first line
        text = "\n".join(text.split(u"\n")[1:])

        # Remove starting whitespace
        text = self.dedent(text)

        # Inspired by autodoc.py in Sphinx
        result = self.list_type()
        for line in text.split("\n"):
            result.append(line, "<sphinxmayaae>")

        return result



class LabelConverter(object):

    def __init__(self, expr):

        self.expr = expr

    def convert(self, name):

        # Split on capitals
        name = self.expr.sub(r"\1 \2", name)

        # Capitalize first letter
        name = "%s%s" % (name[0].upper(), name[1:])

        return name

class MayaHandle(object):

    def __init__(self, cmds):

        self.cmds = cmds

    def editorTemplate( self, *args, **kwargs ):

        self.cmds.editorTemplate( *args, **kwargs )


class DocHandle(object):

    def __init__(self, node_factory, label_converter, content_creator, state):

        self.node_list_stack = [[]]
        self.node_factory = node_factory
        self.label_converter = label_converter
        self.content_creator = content_creator
        self.state = state

    def editorTemplate(self, *args, **kwargs):

        self.dispatch("addControl", self.add_control, args, kwargs)
        self.dispatch("beginLayout", self.begin_layout, args, kwargs)
        self.dispatch("endLayout", self.end_layout, args, kwargs)

    def dispatch(self, name, function, args, kwargs):

        try:
            test = kwargs[ name ]
        except KeyError:
            return

        if test:
            function(args, kwargs)

    def add_control(self, args, kwargs):

        parameter_name = args[0]
        label = self.label_converter.convert(parameter_name)
        title = self.node_factory.Text("%s (%s)" % (label, parameter_name))

        try:
            annotation = kwargs["annotation"]
        except KeyError:
            pass

        # Parent node for the generated node subtree
        annotation_node = self.node_factory.paragraph()
        annotation_node.document = self.state.document

        if annotation:

            rst = self.content_creator(annotation)

            # Generate node subtree
            self.state.nested_parse(rst, 0, annotation_node)

        self.append(
                self.node_factory.definition_list_item(
                    "",
                    self.node_factory.term("", "", self.node_factory.Text(title)),
                    self.node_factory.definition("", annotation_node)
                    )
                )

    def begin_layout(self, args, kwargs):

        layout_name = kwargs["beginLayout"]
        self.append(
                self.node_factory.rubric(
                    "",
                    "",
                    self.node_factory.Text(layout_name)
                    )
                )

        self.push([])

    def end_layout(self, args, kwargs):

        contents = self.pop()

        self.append(self.node_factory.definition_list("", *contents))

    def pop(self):

        return self.node_list_stack.pop()

    def push(self, list):

        self.node_list_stack.append(list)

    def append(self, node):

        # Append the node to the end of the top list in the stack
        #
        self.node_list_stack[-1].append(node)

    def nodes(self):

        assert(len(self.node_list_stack) == 1)

        return self.node_list_stack[0]


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

        node_factory = NodeFactory(docutils.nodes, sphinx.addnodes)

        expr = re.compile(r"([a-z0-9])([A-Z])")
        label_converter = LabelConverter(expr)

        rst_content_creator = RstContentCreator(ViewList, textwrap.dedent)

        doc_handle = DocHandle(node_factory, label_converter, rst_content_creator, self.state)

        function("examplenode", doc_handle)

        return doc_handle.nodes()


# Setup
# -----

def setup(app):

    app.add_directive(
            "mayanode",
            MayaNodeDirective,
            )

