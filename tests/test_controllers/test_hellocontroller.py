import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import setup_malcolm_paths

import unittest
from mock import Mock

from malcolm.controllers.hellocontroller import HelloController


class TestHelloController(unittest.TestCase):
    def test_init(self):
        block = Mock()
        c = HelloController(block)
        self.assertIs(block, c.block)
        self.assertEquals(c.say_hello.Method, block.add_method.call_args[0][0])

    def test_say_hello(self):
        c = HelloController(Mock())
        args = {"name":"test_name"}
        expected = {"greeting":"Hello test_name"}
        self.assertEquals(expected, c.say_hello(args))

if __name__ == "__main__":
    unittest.main(verbosity=2)
