import os
import logging
import rdflib as rdf
from pprint import pprint

logger = logging.getLogger(__name__)


class Manager:
    """Rdflib manager for ontologies."""

    def __init__(self):
        self.assets = list(os.walk(os.getcwd().replace("tools", "assets")))

    def get_graph(
        self,
        file_name="schemaorg-all-https.rdf",
        get_from_url=False,
        save=False,
        schema_url="https://schema.org/version/latest/schemaorg-all-https.rdf",
    ):
        """Return ontology file as rdflib graph class. Save file if not available."""

        file = os.path.join(self.assets[0][0], "xml", file_name)
        graph = rdf.Graph()
        if os.path.isfile(file):
            graph.parse(file)
        elif get_from_url:
            logger.warning("Downloading schema from schema.org")
            graph.parse(schema_url, format="xml")
            if save:
                with open(file, "w") as f:
                    text = graph.serialize(format="xml")
                    f.write(text)
                    f.close()

        else:
            raise Exception(
                """Schema.org file not available, if you want to save the file run:

                Manager().get_schema_org(
                    get_from_url=True,
                    save=True,
                )
                """
            )
        return graph


class PresetLoader:
    """Load ontology from assets file"""

    def __init__(self) -> None:
        self.graph = rdf.Graph()
        self.ontology = Manager().get_graph()
        self.graph.bind("sdo", rdf.SDO)
        self.ontology.bind("sdo", rdf.SDO)
        self.dataTypes = self.get_data_types()

    def query(self, query):
        return self.ontology.query(query)

    def get_data_types(self, pred="rdf:type", uri="sdo:DataType"):
        return self.query(
            f"""
            SELECT DISTINCT ?label
            WHERE {{
                ?sub {pred} {uri}.
                ?sub rdfs:label ?label .
            }}
            """
        )

    def mapping(
        self,
        uri="Person",
        relations=["Person", "Place", "Organization", "Event", "PostalAddress"],
    ):
        manager = {"uri": uri, "datatypes": {}, "relations": {}}
        structure = {"relations": relations, "datatypes": self.dataTypes}
        for s in structure:
            for l in structure[s]:
                if not hasattr(l, "label"):
                    datatype = l
                else:
                    datatype = str(l.label)

                manager[s][datatype] = []

        def _includes(dt, s):
            personDataTypesText = f"""
                SELECT DISTINCT ?label
                WHERE {{
                ?sub sdo:domainIncludes sdo:{uri} .
                ?sub sdo:rangeIncludes sdo:{dt} .
                ?sub rdfs:label ?label .
                }}
            """
            for i in self.query(personDataTypesText):
                manager[s][dt].append(str(i.label))

        for s in structure:
            for dt in manager[s]:
                _includes(dt, s)
        return manager


if __name__ == "__main__":
    test = [
        # PresetLoader().mapping(),
        PresetLoader().mapping(uri="Event"),
        # PresetLoader().mapping(uri="Place"),
        # PresetLoader().mapping(uri="Person")
        # PresetLoader().mapping(uri="Organization")
        # PresetLoader().mapping(uri="Offer")
        # PresetLoader().mapping(uri="Demand")
    ]
    pprint(test)
