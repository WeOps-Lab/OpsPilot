import time

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

from actions.constants.server_settings import server_settings


class OcrService:

    def extract_content(self, img_path) -> str:
        content = ''
        if server_settings.ocr_service == 'Azure':
            computervision_client = ComputerVisionClient(server_settings.azure_ocr_endpoint,
                                                         CognitiveServicesCredentials(
                                                             server_settings.azure_ocr_key))
            read_image = open(img_path, "rb")
            read_response = computervision_client.read_in_stream(read_image, raw=True)
            read_image.close()
            read_operation_location = read_response.headers["Operation-Location"]
            operation_id = read_operation_location.split("/")[-1]
            while True:
                read_result = computervision_client.get_read_result(operation_id)
                if read_result.status not in ['notStarted', 'running']:
                    break
                time.sleep(1)

            if read_result.status == OperationStatusCodes.succeeded:
                for text_result in read_result.analyze_result.read_results:
                    for line in text_result.lines:
                        content += line.text + ' '
        return content
