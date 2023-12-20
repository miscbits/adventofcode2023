from stream_proccessor import (
    parse_message,
    test_condition,
    parse_direction,
)
import unittest


class TestStreamProcessor(unittest.TestCase):
    def test_parse_message(self):
        expected = {"x": 787, "m": 2655, "a": 1222, "s": 2876}
        actual = parse_message("{x=787,m=2655,a=1222,s=2876}")
        self.assertEqual(expected, actual)

    def test_test_condition(self):
        test_message = {"x": 100, "m": 225, "a": 1232, "s": 8}

        self.assertTrue(test_condition(test_message, "x<101"))
        self.assertTrue(test_condition(test_message, "m=225"))
        self.assertTrue(test_condition(test_message, "a>34"))

        self.assertFalse(test_condition(test_message, "s=104"))
        self.assertFalse(test_condition(test_message, "s>8"))
        self.assertFalse(test_condition(test_message, "x<100"))

    def test_parse_direction(self):
        expected = ("pv", [(["a>1716"], "R"), ("default", "A")])
        actual = parse_direction("pv{a>1716:R,A}")

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
