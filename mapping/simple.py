# {"field_mappings": [
#         {
#             "field-name": "TIPO_IDENTIFICACION",
#             "description": "Identification type. For this dataset, it is always '2' (NIT)",
#             "optional": false,
#             "mapping": {
#                 "type": "simple",
#                 "default-value": "2"
#             }
#         },
#         {
#             "field-name": "_TIPO_ENTIDAD",
#             "description": "Internal use only. Entity type. It is used to build the URL to get the identification number.",
#             "optional": false,
#             "mapping": {
#                 "type": "simple",
#                 "rules": {
#                     "element": "$this.tipo_entidad"
#                 },
#                 "default-value": null
#             }
#         },
# ]}

def simple(mapping):
    """
    Simple mapping function. 
    """
    # If the mapping does not have rules, it is a constant value defined in default-value
    if not mapping.get('rules'):
        return mapping.get('default-value')
    # If the mapping has rules, it is a jsonpath expression
    else:
        return jsonpath.@jsonpath(mapping.get('rules'), mapping.get('element'))[0]