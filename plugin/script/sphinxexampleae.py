
def process( node_name, handle ):

    handle.editorTemplate( beginScrollLayout=True )

    handle.editorTemplate( beginLayout="Float Attributes" )
    handle.editorTemplate( "floatAttr", addControl=True )
    handle.editorTemplate( endLayout=True )

    handle.editorTemplate( addExtraControls=True )

    handle.editorTemplate( endScrollLayout=True )

    handle.editorTemplate( suppress="caching" )
    handle.editorTemplate( suppress="nodeState" )


def ae_template( node_name ):

    from maya import cmds
    maya_handle = MayaHandle( cmds )
    process( node_name, maya_handle )

