# Copyright (c) 2016-2018 Alexander Roessler
# NGCWriter is released under the terms of the AGPLv3 or higher.

from UM.Mesh.MeshWriter import MeshWriter
from UM.Logger import Logger
from UM.PluginRegistry import PluginRegistry

import io #For StringIO to write the g-code to a buffer.
import os
import sys
path = os.path.dirname(os.path.realpath(__file__))
if path not in sys.path:
    sys.path.append(path)
from converter.gcode2ngc import GCode2Ngc
from converter.ngc2ve import Ngc2Ve


class NGCWriter(MeshWriter):
    version = 3

    def __init__(self):
        super().__init__()

    def write(self, stream, nodes, mode=MeshWriter.OutputMode.TextMode):
        if mode != MeshWriter.OutputMode.TextMode:
            Logger.log("e", "NGC Writer does not support non-text mode.")
            return False

        # Get the g-code.
        gcode = io.StringIO()
        PluginRegistry.getInstance().getPluginObject("GCodeWriter").write(gcode, None)
        gcode = gcode.getvalue()

        gcodeConverter = GCode2Ngc()
        veConverter = Ngc2Ve()
        gcode = gcodeConverter.process(gcode)
        gcode = veConverter.process(gcode)

        stream.write(gcode)

        return True
