
float_attr_help = """
This is the *annotation* for the floatAttr attribute

Here are some bullet points pertaining to this attribute

- The help is written in rst
- I don't know what else to put in the list

"""

string_attr_help = """
This is the *annotation* for the stringAttr attribute
"""

def process( node_name, handle ):

    handle.editorTemplate( beginScrollLayout=True )

    handle.editorTemplate( beginLayout="Float Attributes" )
    handle.editorTemplate( "floatAttr", addControl=True, annotation=float_attr_help )
    handle.editorTemplate( endLayout=True )

    handle.editorTemplate( beginLayout="String Attributes" )
    handle.editorTemplate( "stringAttr", addControl=True, annotation=string_attr_help )
    handle.editorTemplate( endLayout=True )

    handle.editorTemplate( addExtraControls=True )

    handle.editorTemplate( endScrollLayout=True )

    handle.editorTemplate( suppress="caching" )
    handle.editorTemplate( suppress="nodeState" )


def ae_template( node_name ):

    from maya import cmds
    maya_handle = MayaHandle( cmds )
    process( node_name, maya_handle )

