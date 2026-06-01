"""Protocol 测试。"""

from pylab03.protocols import Config, JsonSerializable, Printable, display, serialize


class TestProtocols:
    def test_config_is_json_serializable(self):
        c = Config({"key": "value"})
        assert isinstance(c, JsonSerializable)

    def test_config_is_printable(self):
        c = Config({"key": "value"})
        assert isinstance(c, Printable)

    def test_serialize(self):
        c = Config({"x": 1})
        result = serialize(c)
        assert '"x": 1' in result

    def test_display(self):
        c = Config({"x": 1})
        result = display(c)
        assert "Config" in result

    def test_non_conforming_not_json_serializable(self):
        class Plain:
            pass

        assert not isinstance(Plain(), JsonSerializable)
