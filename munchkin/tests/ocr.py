from apps.knowledge_mgmt.utils.pdf import pdf2text

# table_engine = RapidTable(model_path='../models/PPStructure/table/ch_ppstructure_mobile_v2_SLANet.onnx', )
# ocr_engine = RapidOCR()
# viser = VisTable()
rs = pdf2text('./tests/asserts/test_doc.pdf')
print(rs)
