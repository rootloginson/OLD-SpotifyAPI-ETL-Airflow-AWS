import logging
import requests
import time


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
formatter.converter = time.gmtime
file_handler = logging.FileHandler("spotify_app.log")
file_handler.setFormatter(formatter)
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(file_handler)


def trigger_starttime_log():
    """Logging time is GMT 0"""
    time_format_name = formatter.converter.__name__
    logger.info("Spotify App executed. (time format: %s)", time_format_name)


class CustomRequestExceptionCheck(object):

    def request_call_with_exception_check(self, f):
        """
        Request object.__bool__ returns:
                True (success): if 200 <= status < 400
                False (error) : else

       ! Logging time is GMT 0

        Arguments:
            API request
                r = request_call_with_exception_check(
                lambda: requests.get(url, headers=headers),
                )

        Returns :
            If no exception raise returns a "request object".
            If exception catched returns "None".
        """
        request_from = f.__qualname__.split(".")[:-2]
        request_from = ".".join(request_from)
        request_from = "=".join(["request_from", request_from])
        # request_form format e.g.: "request_from:
        error_body = "".join(["request_status=FAILED",
                              ", ",
                              "requests.exception="]
                            )
        try:
            r = f()
            r.raise_for_status()
        except requests.exceptions.ConnectionError:
            logger.error("%s%s, %s", error_body, 'ConnectionError', request_from)
        except requests.exceptions.Timeout:
            logger.error("%s%s, %s", error_body, 'Timeout', request_from)
        except requests.exceptions.HTTPError:
            logger.error("%s%s, %s", error_body, 'HTTPError', request_from)
        except requests.exceptions.ProxyError:
            logger.error("%s%s, %s", error_body, 'ProxyError', request_from)
        except requests.exceptions.SSLError:
            logger.error("%s%s, %s", error_body, 'SSLError', request_from)
        except requests.exceptions.RequestException as e:
            logger.error("%s%s, %s", error_body, e, request_from)
        else:
            # Authentication Error Object Check
            try:
                _ = r.json()['error']
            except KeyError:
                logger.info("%s, %s=%s, %s",
                            "request_status=SUCCESS",
                            "status_code", r.status_code,
                            request_from,
                            )
                return r
            else:
                logger.error("%s, %s=%s, %s=%s, %s",
                             "request_status=ERROR",
                             "status_code", r.status_code,
                             "error", r.json(),
                             request_from
                             )
                return r
        return None
