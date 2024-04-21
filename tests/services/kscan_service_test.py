import logging

from actions.services.kscan_service import KScanService


def test_scan():
    targets = "127.0.0.1,192.168.31.1"
    service = KScanService()
    result = service.scan(targets)
    md_result = service.json_to_markdown(result)
    logging.info(md_result)
