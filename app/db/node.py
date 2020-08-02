from pydantic import BaseModel
from neo4j.work.simple import Session

class Node(BaseModel):
    _session: Session

    
    @staticmethod
    def serialize_node(node_attr):
        return {i: node_attr[i] for i in node_attr.keys()}

    @staticmethod
    def serialize_node_relation(relation_type, relation):
        return {relation_type: relation}

    def query_all_node(self):
        def match_all_node(self, tx):
            result = tx.run("MATCH (a:%s ) RETURN a" % self.__class__.__name__)
            return {"list_item": sorted([self.serialize_node(record["a"])["name"] for record in result], key=len,
                                        reverse=True)}

        return self._session.read_transaction(match_all_node)

    
    def delete_node(self, name):
        def delete_node(tx, name):
            tx.run("MATCH (a:%s {name: $name}) "
                   "DETACH DELETE a" % self.__class__.__name__, name=name)

        self._session.write_transaction(delete_node, name)

