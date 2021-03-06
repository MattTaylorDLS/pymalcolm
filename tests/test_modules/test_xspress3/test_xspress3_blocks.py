from mock import Mock

from malcolm.testutil import ChildTestCase
from malcolm.modules.xspress3.blocks import xspress3_detector_manager_block


class TestXmapBlocks(ChildTestCase):
    def test_xspress3_detector_manager_block(self):
        self.create_child_block(
            xspress3_detector_manager_block, Mock(),
            mriPrefix="mriPrefix", pvPrefix="pvPrefix", configDir="/tmp")
