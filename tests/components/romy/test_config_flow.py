"""Test the ROMY config flow."""
import asyncio
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

async def test_show_user_form(hass: HomeAssistant) -> None:
    """Test that the user set up form is served."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
    )

    assert result["errors"] is not None
    assert result["step_id"] == "user"
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM


MOCK_IP = "1.2.3.4"
CONFIG = {CONF_HOST: MOCK_IP, CONF_PORT: 8080, CONF_NAME: "myROMY"}

INPUT_CONFIG = {
    CONF_HOST: CONFIG[CONF_HOST],
    CONF_PORT: CONFIG[CONF_PORT],
    CONF_NAME: CONFIG[CONF_NAME],    
}

async def test_show_user_form_with_config(hass: HomeAssistant) -> None:
    """Test that the user set up form with config."""

    # patch for set robot name call
    with patch(
        "homeassistant.components.romy.config_flow.async_query",
        return_value=(True, '{}'),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
            data=INPUT_CONFIG,
        )

    assert "errors" not in result
    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY

INPUT_EMPTY_CONFIG = {}

async def test_show_user_form_with_empty_config(hass: HomeAssistant) -> None:
    """Test that the user set up form with empty config."""

    # patch for set robot name call
    with patch(
        "homeassistant.components.romy.config_flow.async_query",
        return_value=(True, '{}'),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
            data=INPUT_EMPTY_CONFIG,
            local_http_interface_is_locked=True
        )

    assert result["errors"] is not None
    assert result["step_id"] == "user"
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM

async def test_show_user_form_with_config_locked_robot(hass: HomeAssistant) -> None:
    """Test that the user set up form with config."""

    # patch for set robot name call
    with patch(
        "homeassistant.components.romy.config_flow.async_query",
        return_value=(True, '{}'),
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
            data=INPUT_CONFIG,
        )

    assert "errors" not in result
    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY

DISCOVERY_INFO = zeroconf.ZeroconfServiceInfo(
    host="1.2.3.4",
    hostname="myROMY",
    port=8080,
    type="mock_type",
    addresses="addresse",
    name="myROMY",
    properties={zeroconf.ATTR_PROPERTIES_ID: "aicu-aicgsbksisfapcjqmqjq"},
)

async def test_zero_conf_unlocked_interface_robot(hass: HomeAssistant) -> None:
    """Test zerconf with already unlocked robot"""

    with patch(
        "homeassistant.components.romy.config_flow.async_query",
        return_value=(True, '{"name": "myROMY"}'),
    ):
        with patch(
            "homeassistant.components.romy.config_flow.async_query_with_http_status",
            return_value=(True, "", 200),
        ):
            result = await hass.config_entries.flow.async_init(
                DOMAIN,
                data=DISCOVERY_INFO,
                context={"source": config_entries.SOURCE_ZEROCONF},
            )

    assert result["step_id"] == "user"
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM

async def test_zero_conf_locked_interface_robot(hass: HomeAssistant) -> None:
    """Test zerconf with locked local http interface robot"""

    with patch(
        "homeassistant.components.romy.config_flow.async_query",
        return_value=(True, '{"name": "myROMY"}'),
    ):
        with patch(
            "homeassistant.components.romy.config_flow.async_query_with_http_status",
            return_value=(False, "", 403),
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
