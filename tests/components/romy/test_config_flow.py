"""Test the ROMY config flow."""
from unittest.mock import patch

from homeassistant import config_entries, data_entry_flow
from homeassistant.components import zeroconf
from homeassistant.components.romy.const import DOMAIN
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PASSWORD, CONF_PORT
from homeassistant.core import HomeAssistant

MOCK_IP = "1.2.3.4"
VALID_CONFIG = {CONF_HOST: MOCK_IP, CONF_PORT: 8080, CONF_NAME: "myROMY"}
VALID_CONFIG_WITH_PASS = {
    CONF_HOST: MOCK_IP,
    CONF_PORT: 8080,
    CONF_NAME: "myROMY",
    CONF_PASSWORD: "password",
}


# def _create_mocked_romy():
#    mocked_romy = MagicMock()
#    return mocked_romy


async def test_show_user_form(hass: HomeAssistant) -> None:
    """Test that the user set up form is served."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
    )

    assert result["step_id"] == "user"
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM


DISCOVERY_INFO = zeroconf.ZeroconfServiceInfo(
    host="1.2.3.4",
    hostname="myROMY",
    port=8080,
    type="mock_type",
    addresses="addresse",
    name="myROMY",
    properties={zeroconf.ATTR_PROPERTIES_ID: "romy-blubF"},
)


# @pytest.fixture(name="mock_socket")
# def fixture_mock_socket():
#    """Mock socket fixture."""
#    with patch("socket.socket") as mock_socket:
#        yield mock_socket

# def test_explicitly_enable_socket(socket_enabled):
#    assert socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# @pytest.mark.enable_socket
# @pytest.mark.allow_hosts(['1.2.3.4'])
async def test_zero_conf(hass: HomeAssistant) -> None:
    """Test zeroConf."""

    # assert socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # assert socket.socket.connect(('1.2.3.4', 8080))

    with patch(
        "homeassistant.components.romy.utils.async_query",
        return_value=async_return(True, ""),
    ):
        with patch(
            "homeassistant.components.romy.utils.async_query_with_http_status",
            return_value=async_return(True, ""),
        ):
            result = await hass.config_entries.flow.async_init(
                DOMAIN,
                data=DISCOVERY_INFO,
                context={"source": config_entries.SOURCE_ZEROCONF},
            )

    assert result["step_id"] == "user"
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM


# https://snyk.io/advisor/python/asynctest/functions/asynctest.mock.patch

# async def test_connect(self):
#        with amock.patch("aiohttp.ClientSession.get") as patched_request:
#            mockresponse = amock.CoroutineMock()
#            mockresponse.status = 200
#            mockresponse.json = amock.CoroutineMock(return_value={"login": "opsdroid"})
#            patched_request.return_value = asyncio.Future()
#            patched_request.return_value.set_result(mockresponse)
#            await self.connector.connect()


# pytest ./tests/components/romy/ --cov=homeassistant.components.romy --cov-report term-missing -v
# python -m trace -c -m -C . /home/nios/gits/core/venv/bin/pytest  ./tests/components/romy/ --cov=homeassistant.components.romy --cov-report term-missing -v
