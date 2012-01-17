
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

import sys

class SphinxExampleNode(OpenMayaMPx.MPxNode):

    floatAttr = OpenMaya.MObject()


def nodeCreator():

    return OpenMayaMPx.asMPxPtr( SphinxExampleNode() )


def nodeInitializer():
    
    nAttr = OpenMaya.MFnNumericAttribute()

    # Create attributes
    SphinxExampleNode.floatAttr = nAttr.create( "floatAttr", "fa", OpenMaya.MFnNumericData.kFloat, 0.0 )

    # Add attributes
    SphinxExampleNode.addAttribute( SphinxExampleNode.floatAttr )
    


sphinxExampleNodeId = OpenMaya.MTypeId(0x87000)

def initializePlugin(mobject):

    mplugin = OpenMayaMPx.MFnPlugin(mobject)

    try:
        mplugin.registerNode( "sphinxExample", sphinxExampleNodeId, nodeCreator, nodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: SphinxExample" )
        raise

def uninitializePlugin(mobject):

    mplugin = OpenMayaMPx.MFnPlugin(mobject)

    try:
        mplugin.deregisterNode( sphinxExampleNodeId )
    except:
        sys.stderr.write( "Failed to deregister node: SphinxExample" )
        raise
    
