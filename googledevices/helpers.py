"""Googledevices helpers.

All methods are prefixed with 'gdh_' for (GoogleDevicesHelpers).
"""


def gdh_loop():
    """Asyncio loop."""
    from asyncio import get_event_loop

    return get_event_loop()


def gdh_session():
    """Aiohttp clientsession."""
    from aiohttp import ClientSession

    return ClientSession()


async def gdh_sleep(seconds=5):
    """Asyncio sleep."""
    from asyncio import sleep

    await sleep(seconds)


async def gdh_request(
    host,
    schema=None,
    port=None,
    token=None,
    endpoint=None,
    json=True,
    session=None,
    loop=None,
    headers=None,
    data=None,
    json_data=None,
    params=None,
    method="get",
):
    """Web request."""
    import asyncio
    import aiohttp
    import async_timeout
    from socket import gaierror
    from googledevices.utils.const import API
    import googledevices.utils.log as log

    if schema is None:
        schema = "http"
    port = ":{port}".format(port=port) if port is not None else ""
    url = API.format(schema=schema, host=host, port=port, endpoint=endpoint)
    result = None
    if token is not None:
        if headers is None:
            headers = {}
        headers["cast-local-authorization-token"] = token

    if session is None:
        session = gdh_session()
    if loop is None:
        loop = gdh_loop()
    try:
        async with async_timeout.timeout(8, loop=loop):
            if method == "post":
                webrequest = await session.post(
                    url, json=json_data, data=data, params=params, headers=headers, ssl=False
                )
            else:
                webrequest = await session.get(
                    url, json=json_data, data=data, params=params, headers=headers, ssl=False
                )
            result = await webrequest.json() if json else webrequest
    except (TypeError, KeyError, IndexError) as error:
        log.error(f"Error parsing information - {error}")
    except asyncio.TimeoutError:
        log.error(f"Timeout contacting {url}")
    except asyncio.CancelledError:
        log.error(f"Cancellation error contacting {url}")
    except aiohttp.ClientError as error:
        log.error(f"ClientError contacting {url} - {error}")
    except gaierror as error:
        log.error(f"I/O error contacting {url} - {error}")
    except Exception as error:  # pylint: disable=W0703
        log.error(f"Unexpected error contacting {url} - {error}")
    return result
