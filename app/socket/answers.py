from rdflib import Graph
import os
import json
from app.helpers.find_item import find_item
from app.helpers.random_item import random_item
from app.data.sample_answers import sample_answers, unclear_answers
from wit import Wit
from app.helpers.get_most_common_elements import get_most_common_elements
from rdflib import Graph, Namespace, RDF, URIRef, Literal

def handle_violation(entities):
    message =""
    # print(entities)
    g = Graph()
    g.parse('./app/ontology/luat.rdf', format="application/rdf+xml")
    filter_string = ""
    filters = []
    for entity in entities:
        value = entity["value"]
        name = entity["entity"]
        if name == "hanhvivipham":
            filters.append(f'contains(LCASE(?content),"{value.lower()}") ')
        # if name == "doituongbitacdong":
        #     filters.append(f'contains(LCASE(?content),"{value.lower()}") ')
        if name == "vipham":
            filters.append(f'contains(LCASE(?detail),"{value.lower()}") ')
        # if name == "hanhvi":
        #     filters.append(f'contains(LCASE(?detail),"{value.lower()}") ')

    if len(filters) > 0:
        filter_string += f'filter ({" || ".join(filters)}) \n.'
    query = (
        'PREFIX laws: <http://www.semanticweb.org/pinkk/ontologies/2023/5/luat#>\n'
        'SELECT DISTINCT * WHERE {\n'
        '    ?result laws:Chi_tiết_về_vi_phạm ?content .\n'
        '    ?result laws:hasResolution ?resolution.\n'
        '    ?result laws:relatesToLaw ?law.\n'
        '    ?result laws:hasViolation ?violation.\n'
        '    ?resolution laws:Chi_tiết_về_cách_giải_quyết ?fine.\n'
        '    ?law laws:Chi_tiết_về_pháp_luật ?legal.\n'
        '    ?violation laws:Chi_tiết_hành_vi_vi_phạm ?detail.\n'
        f'     {filter_string}\n'
        '}\n'
        'ORDER by ASC(?content)\n'

    )
    # result = g.query(query)

    print(query)
    result = g.query(query)
    for item in result:
        value = {
            "id": item.get("result").split("#")[1],
            "detail": item.get("detail"),
            "content": item.get("content"),
            "legal": item.get("legal"),
            "fine": item.get("fine"),
        }

        message += f'<div style="margin-bottom: 30px"> <div style="font-weight: 500 ; font-size: 18px" > Theo {value["legal"]} ' \
                   f'</div> <div>***Có nội dung: {value["content"]}</div> ' \
                   f'<div>***Hành vi vi phạm: {value["detail"]}</div>'\
                   f'<div>***{value["fine"]}</div></div>'

    return message

def handle_concept(entities):
    message = ""
    # Tạo Graph
    g = Graph()
    g.parse('./app/ontology/luat.rdf', format="application/rdf+xml")

    filter_string = ""
    filters = []

    for entity in entities:
        value = entity['value']
        name = entity["entity"]
        # filters.append(f'''(LCASE(?name) =  "{value.lower()}")''')
        if name == "khainiem":
            filters.append(f'''(LCASE(?name) =  "{value.lower()}")''')

    if len(filters) > 0:
        filter_string = f'filter ({" || ".join(filters)}) \n'
    query = (
        'PREFIX laws: <http://www.semanticweb.org/pinkk/ontologies/2023/5/luat#>\n'
        'SELECT * WHERE {\n'
        '?result laws:Ten ?name. \n'
        '?result laws:YNghia ?meaning.\n'
        f'     {filter_string}\n'
        '}\n'
    )

    print(query)
    result = g.query(query)

    for item in result:
        value = {
            "id": item.get("result").split("#")[1],
            "name": item.get("name"),
            "meaning": item.get("meaning"),
        }
        message = f'{value["name"]} là  {value["meaning"]}</div>'
    return message

def get_answer(text):
    message = ""
    # try:
    # print("TOKEN=", os.getenv("SERVER_ACCESS_TOKEN"))
    client = Wit(os.getenv("SERVER_ACCESS_TOKEN"))
    data = client.get_message(text)
    print(data)
    intents = []
    if "intent" in data["outcomes"][0]["entities"]:
        intents = data["outcomes"][0]["entities"]["intent"]
    entities = []
    keys = data["outcomes"][0]["entities"].keys()
    for key in keys:
        if key != "intent":
            for obj in data["outcomes"][0]["entities"][key]:
                split_key = key.split(":")
                entity = {
                    "value": obj["value"],
                    "entity": split_key[0] if len(split_key) > 0 else key
                }

                entities.append(entity)

    if len(intents) > 0:
        intent_high_confidence = intents[0]
        label = intent_high_confidence['value']
        if label in sample_answers:
            message = random_item(sample_answers[label])
        elif label == "xemvipham":
            message = handle_violation(entities)
        elif label == "xemkhainiem":
            message = handle_concept(entities)
        # elif label in sample_answers:
        #     message = random_item(sample_answers[label])
        # elif label == "xem_muc_phat":
        #     message = handle_violation(entities)

    if message == '':
        return random_item(unclear_answers)
    return message