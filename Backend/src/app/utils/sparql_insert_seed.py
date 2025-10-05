# convert_to_rdf.py
from ..models import User, Test, Question, Answer, Graph, Node, Edge, Result, StudentAnswer
import requests
import re

class DatabaseToRDFConverter:
    def __init__(self, virtuoso_endpoint="http://localhost:8890/sparql", default_graph="http://example.org/kst"):
        self.virtuoso_endpoint = virtuoso_endpoint
        self.default_graph = default_graph
        
    def clean_uri_component(self, text):
        """Clean text for use in URIs"""
        if text is None:
            return "unknown"
        cleaned = re.sub(r'[^\w\s-]', '', text.lower())
        cleaned = re.sub(r'[-\s]+', '_', cleaned)
        return cleaned.strip('_')
    
    def create_uri(self, entity_type, entity_id, title=None):
        """Create URI using database ID and optional title for readability"""
        if title:
            clean_title = self.clean_uri_component(title)
            return f"kst:{entity_type}_{entity_id}_{clean_title}"
        else:
            return f"kst:{entity_type}_{entity_id}"
    
    def get_all_data_from_db(self, app, db):
        """Extract ALL data from the SQL database using SQLAlchemy models"""
        print("Extracting data from SQL database...")
        
        with app.app_context():
            # Get all data using your existing models
            data = {
                'teachers': User.query.filter_by(role='teacher').all(),
                'students': User.query.filter_by(role='student').all(),
                'graphs': Graph.query.all(),
                'tests': Test.query.all(),
                'questions': Question.query.all(),
                'answers': Answer.query.all(),
                'nodes': Node.query.all(),
                'edges': Edge.query.all(),
                'results': Result.query.all(),
                'student_answers': StudentAnswer.query.all(),
            }
            
            print(f"Found in database:")
            for key, value in data.items():
                print(f"- {key}: {len(value)}")
            
            return data
    
    def create_insert_queries(self, data):
        """Create SPARQL INSERT queries using actual database IDs"""
        queries = []
        
        # Insert teachers with their actual IDs
        for teacher in data['teachers']:
            teacher_uri = self.create_uri("teacher", teacher.id, f"{teacher.first_name}_{teacher.last_name}")
            query = f"""
            INSERT DATA {{
                 GRAPH <{self.default_graph}> {{
                {teacher_uri} a kst:Teacher ;
                    foaf:firstName "{teacher.first_name}" ;
                    foaf:lastName "{teacher.last_name}" ;
                    foaf:mbox "mailto:{teacher.email}" .
            }} }}
            """
            queries.append(query)
        
        # Insert students with their actual IDs
        for student in data['students']:
            student_uri = self.create_uri("student", student.id, f"{student.first_name}_{student.last_name}")
            query = f"""
            INSERT DATA {{
                GRAPH <{self.default_graph}> {{
                {student_uri} a kst:Student ;
                    foaf:firstName "{student.first_name}" ;
                    foaf:lastName "{student.last_name}" ;
                    foaf:mbox "mailto:{student.email}" .
            }} }}
            """
            queries.append(query)
        
        # Insert knowledge graphs with their actual IDs
        for graph in data['graphs']:
            graph_uri = self.create_uri("graph", graph.id, self.clean_uri_component(graph.title))
            query = f"""
            INSERT DATA {{
                GRAPH <{self.default_graph}> {{
                {graph_uri} a kst:KnowledgeGraph ;
                    dc:title "{graph.title}" ;
                    dc:description "{graph.description}" ;
                    lom:educationalObjective "{graph.educational_objective}" ;
                    lom:context "{graph.context}" ;
                    dc:language "{graph.language}" .
            }} }}
            """
            queries.append(query)
        
        # Create mapping dictionaries for relationships
        user_uris = {}
        graph_uris = {}
        node_uris = {}
        test_uris = {}
        question_uris = {}
        answer_uris = {}
        
        # Store URIs for later use in relationships
        for teacher in data['teachers']:
            user_uris[teacher.id] = self.create_uri("teacher", teacher.id, f"{teacher.first_name}_{teacher.last_name}")
        
        for student in data['students']:
            user_uris[student.id] = self.create_uri("student", student.id, f"{student.first_name}_{student.last_name}")
        
        for graph in data['graphs']:
            graph_uris[graph.id] = self.create_uri("graph", graph.id, self.clean_uri_component(graph.title))
        
        # Insert nodes with their actual IDs
        for node in data['nodes']:
            node_uri = self.create_uri("node", node.id, self.clean_uri_component(node.title))
            node_uris[node.id] = node_uri
            graph_uri = graph_uris.get(node.graph_id)
            
            query = f"""
            INSERT DATA {{
                GRAPH <{self.default_graph}> {{
                {node_uri} a kst:Node ;
                    dc:title "{node.title}" ;
                    kst:belongsToGraph {graph_uri} .
            }} }}
            """
            queries.append(query)
        
        # Insert edges with their actual IDs
        for edge in data['edges']:
            edge_uri = self.create_uri("edge", edge.id)
            source_uri = node_uris.get(edge.source_id)
            target_uri = node_uris.get(edge.target_id)
            graph_uri = graph_uris.get(edge.graph_id)
            
            if source_uri and target_uri:
                query = f"""
                INSERT DATA {{
                    GRAPH <{self.default_graph}> {{
                    {edge_uri} a kst:Edge ;
                        kst:hasSourceNode {source_uri} ;
                        kst:hasTargetNode {target_uri} .
                }} }}
                """
                queries.append(query)
        
        # Insert tests with their actual IDs
        for test in data['tests']:
            test_uri = self.create_uri("test", test.id, self.clean_uri_component(test.title))
            test_uris[test.id] = test_uri
            author_uri = user_uris.get(test.author_id)
            graph_uri = graph_uris.get(test.graph_id)
            
            query = f"""
            INSERT DATA {{
                GRAPH <{self.default_graph}> {{
                {test_uri} a kst:Test ;
                    dc:title "{test.title}" ;
                    dc:description "{test.description}" ;
                    lom:educationalObjective "{test.educational_objective}" ;
                    lom:typicalLearningTime "{test.typical_learning_time}" ;
                    lom:context "{test.context}" ;
                    dc:language "{test.language}" ;
                    kst:hasAuthor {author_uri} ;
                    kst:usesGraph {graph_uri} .
            }} }}
            """
            queries.append(query)
        
        # Insert questions with their actual IDs
        for question in data['questions']:
            question_uri = self.create_uri("question", question.id, self.clean_uri_component(question.text[:50]))
            question_uris[question.id] = question_uri
            test_uri = test_uris.get(question.test_id)
            node_uri = node_uris.get(question.node_id) if question.node_id else None
            
            node_mapping = f"kst:mapsToNode {node_uri} ;" if node_uri else ""
            
            query = f"""
            INSERT DATA {{
                GRAPH <{self.default_graph}> {{
                {question_uri} a kst:Question ;
                    dc:title "{question.text}" ;
                    lom:educationalObjective "{question.educational_objective or ''}" ;
                    lom:difficulty "{question.difficulty or ''}" ;
                    lom:typicalLearningTime "{question.typical_learning_time or ''}" ;
                    kst:isMultichoice "{str(question.is_multichoice).lower()}"^^xsd:boolean ;
                    {node_mapping}
                    kst:belongsToTest {test_uri} .
            }} }}
            """
            queries.append(query)
        
        # Insert answers with their actual IDs
        for answer in data['answers']:
            answer_uri = self.create_uri("answer", answer.id, self.clean_uri_component(answer.text[:30]))
            answer_uris[answer.id] = answer_uri
            question_uri = question_uris.get(answer.question_id)
            
            query = f"""
            INSERT DATA {{
                GRAPH <{self.default_graph}> {{
                {answer_uri} a kst:Answer ;
                    dc:description "{answer.text}" ;
                    kst:isCorrect "{str(answer.is_correct).lower()}"^^xsd:boolean ;
                    kst:belongsToQuestion {question_uri} .
            }} }}
            """
            queries.append(query)
        
        # Insert results with their actual IDs
        for result in data['results']:
            result_uri = self.create_uri("result", result.id)
            test_uri = test_uris.get(result.test_id)
            student_uri = user_uris.get(result.student_id)
            timestamp = result.timestamp.strftime("%Y-%m-%dT%H:%M:%S") if result.timestamp else "2024-01-01T00:00:00"
            
            query = f"""
            INSERT DATA {{
                GRAPH <{self.default_graph}> {{
                {result_uri} a kst:TestResult ;
                    kst:forTest {test_uri} ;
                    kst:timestamp "{timestamp}"^^xsd:dateTime ;
                    kst:isUsed "{str(result.is_used).lower()}"^^xsd:boolean ;
                    kst:score "{result.score or 0.0}"^^xsd:decimal ;
                    kst:belongsToStudent {student_uri} .
            }} }}
            """
            queries.append(query)
        
        # Insert student answers with their actual IDs
        for student_answer in data['student_answers']:
            sa_uri = self.create_uri("student_answer", student_answer.id)
            result_uri = self.create_uri("result", student_answer.result_id)
            answer_uri = answer_uris.get(student_answer.answer_id)
            
            # Find the question ID from the answer
            answer_obj = next((a for a in data['answers'] if a.id == student_answer.answer_id), None)
            question_uri = question_uris.get(answer_obj.question_id) if answer_obj else None
            
            if question_uri:
                query = f"""
                INSERT DATA {{
                    GRAPH <{self.default_graph}> {{
                    {sa_uri} a kst:StudentAnswer ;
                        kst:answersQuestion {question_uri} ;
                        kst:selectedAnswer {answer_uri} ;
                        kst:belongsToResult {result_uri} .
                }} }}
                """
                queries.append(query)
        
        return queries
    
    def execute_sparql_update(self, query):
        """Execute a SPARQL UPDATE query against Virtuoso"""
        headers = {
            'Content-Type': 'application/sparql-update',
            'Accept': 'application/sparql-results+json'
        }
        
        try:
            response = requests.post(
                self.virtuoso_endpoint,
                data=query,
                headers=headers
            )
            
            if response.status_code in [200, 201]:
                print("✓ Query executed successfully")
                return True
            else:
                print(f"✗ Query failed with status {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Error executing query: {e}")
            return False
    
    def convert_and_insert(self, app, db, batch_size=50):
        """Main method to convert data and insert into Virtuoso"""
        print("Starting conversion of database data to RDF...")
        
        # Get all data from database
        data = self.get_all_data_from_db(app, db)
        
        # Create INSERT queries
        queries = self.create_insert_queries(data)
        
        print(f"Generated {len(queries)} SPARQL INSERT queries")
        
        # Execute queries in batches to avoid timeouts
        successful = 0
        for i in range(0, len(queries), batch_size):
            batch = queries[i:i + batch_size]
            print(f"Executing batch {i//batch_size + 1}/{(len(queries)-1)//batch_size + 1}...")
            
            # Combine batch into single query for efficiency
            combined_query = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"
            combined_query += "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
            combined_query += "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n"
            combined_query += "PREFIX lom: <http://ltsc.ieee.org/rdf/lom/>\n"
            combined_query += "PREFIX dc: <http://purl.org/dc/elements/1.1/>\n"
            combined_query += "PREFIX kst: <http://example.org/kst#>\n"
            combined_query += "PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n\n"
            
            for query in batch:
                # Extract the INSERT DATA part from each query
                # insert_part = query.split("INSERT DATA {")[1].rstrip("}")
                combined_query += query
            
            if self.execute_sparql_update(combined_query):
                successful += len(batch)
        
        print(f"Conversion completed: {successful}/{len(queries)} triples inserted successfully")
