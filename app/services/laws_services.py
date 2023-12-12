from rdflib import Graph, Namespace, RDF, URIRef, Literal

def search_by_content(args):
    keyword = args.get('keyword')
    g = Graph()
    g.parse('./app/ontology/luat.rdf', format="application/rdf+xml")

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
        f'    filter contains(LCASE(?content),"{keyword.lower()}") .\n'
        # '    OPTIONAL{?resolution laws:Hình_phạt_bổ_sung ?fines.}\n'
        '}\n'
        'ORDER by ASC(?content)\n'

    )
    data = []
    print(query)
    result= g.query(query)
    for item in result:
        value ={
            "id": item.get("result").split("#")[1],
            "detail": item.get("detail"),
            "content": item.get("content"),
            "legal": item.get("legal"),
            "fine": item.get("fine"),
        }
        data.insert(0,value)

    return data
