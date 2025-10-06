# convert_to_rdf.py
from __future__ import annotations

import re
import requests
from typing import Dict, Any, List, Optional

# keep your original models import & app/db usage
from ..models import (
    User, Test, Question, Answer, Graph, Node, Edge, Result, StudentAnswer
)


class DatabaseToRDFConverter:
    """
    Converts SQLAlchemy rows to RDF and inserts into Virtuoso.
    - One INSERT per entity (no batching).
    - Escapes quotes/newlines in all string literals.
    - Uses IRIs for emails (foaf:mbox <mailto:...>).
    - Booleans as true/false; numeric score as numeric literal.
    - Ensures the target named graph exists.
    - Compatible with Virtuoso: tries 'application/sparql-update' first,
      then falls back to 'application/x-www-form-urlencoded' with 'update='.
    """

    def __init__(
        self,
        virtuoso_endpoint: str = "http://localhost:8890/sparql",
        default_graph: str = "http://example.org/kst",
        username: Optional[str] = None,  # pass if using /sparql-auth
        password: Optional[str] = None,
        timeout_s: int = 60,
    ) -> None:
        self.virtuoso_endpoint = virtuoso_endpoint
        self.default_graph = default_graph.rstrip("/")
        # instance IRIs will live under <http://example.org/kst#...>
        self.vocab_base = f"{self.default_graph}#"
        self.auth = (username, password) if username and password else None
        self.timeout_s = timeout_s

        self.prefixes = (
            "PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n"
            "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
            "PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>\n"
            "PREFIX lom:  <http://ltsc.ieee.org/rdf/lom/>\n"
            "PREFIX dc:   <http://purl.org/dc/elements/1.1/>\n"
            "PREFIX kst:  <http://example.org/kst#>\n"
            "PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n\n"
        )

    # -------------------------
    # Helpers
    # -------------------------

    def esc(self, s: Any) -> str:
        """Escape a Python value for use as an RDF string literal."""
        if s is None:
            return ""
        return (
            str(s)
            .replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\r\n", "\\n")
            .replace("\n", "\\n")
            .replace("\r", "\\n")
        )

    def clean_uri_component(self, text: Optional[str]) -> str:
        if text is None:
            return "unknown"
        cleaned = re.sub(r"[^\w\s-]", "", text.lower())
        cleaned = re.sub(r"[-\s]+", "_", cleaned)
        return cleaned.strip("_") or "unknown"

    def iri(self, local: str) -> str:
        return f"<{self.vocab_base}{local}>"

    def create_uri(self, entity_type: str, entity_id: Any, title: Optional[str] = None) -> str:
        if title:
            part = f"{entity_type}_{entity_id}_{self.clean_uri_component(title)}"
        else:
            part = f"{entity_type}_{entity_id}"
        return self.iri(part)

    def _wrap_insert(self, triple_block: str) -> str:
        return (
            self.prefixes
            + f"INSERT DATA {{ GRAPH <{self.default_graph}> {{\n"
            + triple_block
            + "\n} }"   # <-- exactly two closing braces: close GRAPH { ... } then INSERT DATA { ... }
        )

    def _exec_update(self, query: str) -> bool:
        """
        Execute a SPARQL UPDATE with two strategies for Virtuoso:
        1) application/sparql-update with raw body
        2) application/x-www-form-urlencoded with 'update='
        """
        try:
            # Try raw SPARQL Update first
            r = requests.post(
                self.virtuoso_endpoint,
                data=query.encode("utf-8"),
                headers={
                    "Content-Type": "application/sparql-update",
                    "Accept": "application/sparql-results+json",
                },
                auth=self.auth,
                timeout=self.timeout_s,
            )
            if r.status_code in (200, 201, 204):
                return True

            # Fallback: Virtuoso also accepts form-encoded 'update='
            r2 = requests.post(
                self.virtuoso_endpoint,
                data={"update": query},
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/sparql-results+json",
                },
                auth=self.auth,
                timeout=self.timeout_s,
            )
            if r2.status_code in (200, 201, 204):
                return True

            print(f"✗ SPARQL update failed [{r.status_code}/{r2.status_code}]:\n"
                  f"{(r.text or '')[:1000]}\n{(r2.text or '')[:1000]}")
            return False

        except Exception as e:
            print(f"✗ Error executing SPARQL update: {e}")
            return False

    def insert_triples(self, triple_block: str, kind: str, entity_id: Any) -> None:
        q = self._wrap_insert(triple_block)
        ok = self._exec_update(q)
        if not ok:
            preview = triple_block.strip().splitlines()[0][:140]
            print(f"✗ {kind} {entity_id}: insert failed. First triple line: {preview!r}")

    def ensure_graph_exists(self) -> None:
        clear_q = self.prefixes + f"CLEAR SILENT GRAPH <{self.default_graph}>"
        self._exec_update(clear_q)
        q = self.prefixes + f"CREATE SILENT GRAPH <{self.default_graph}>"
        # best-effort; ignore failures here (permissions are handled earlier)
        self._exec_update(q)

    # -------------------------
    # Extraction
    # -------------------------

    def get_all_data_from_db(self, app, db) -> Dict[str, List[Any]]:
        with app.app_context():
            data = {
                "teachers": User.query.filter_by(role="teacher").all(),
                "students": User.query.filter_by(role="student").all(),
                "graphs": Graph.query.all(),
                "tests": Test.query.all(),
                "questions": Question.query.all(),
                "answers": Answer.query.all(),
                "nodes": Node.query.all(),
                "edges": Edge.query.all(),
                "results": Result.query.all(),
                "student_answers": StudentAnswer.query.all(),
            }
        return data

    # -------------------------
    # Main conversion
    # -------------------------

    def convert_and_insert(self, app, db) -> None:
        print("Starting conversion of database data to RDF...")
        self.ensure_graph_exists()

        data = self.get_all_data_from_db(app, db)

        user_uris: Dict[int, str] = {}
        graph_uris: Dict[int, str] = {}
        node_uris: Dict[int, str] = {}
        test_uris: Dict[int, str] = {}
        question_uris: Dict[int, str] = {}
        answer_uris: Dict[int, str] = {}

        # Users (teachers)
        for t in data["teachers"]:
            uri = self.create_uri("teacher", t.id, f"{t.first_name}_{t.last_name}")
            user_uris[t.id] = uri
            triples = (
                f"{uri} a kst:Teacher ;\n"
                f'  foaf:firstName "{self.esc(t.first_name)}" ;\n'
                f'  foaf:lastName  "{self.esc(t.last_name)}" ;\n'
                f'  foaf:mbox      <mailto:{self.esc(t.email)}> .'
            )
            self.insert_triples(triples, "Teacher", t.id)

        # Users (students)
        for s in data["students"]:
            uri = self.create_uri("student", s.id, f"{s.first_name}_{s.last_name}")
            user_uris[s.id] = uri
            triples = (
                f"{uri} a kst:Student ;\n"
                f'  foaf:firstName "{self.esc(s.first_name)}" ;\n'
                f'  foaf:lastName  "{self.esc(s.last_name)}" ;\n'
                f'  foaf:mbox      <mailto:{self.esc(s.email)}> .'
            )
            self.insert_triples(triples, "Student", s.id)

        # Graphs
        for g in data["graphs"]:
            g_uri = self.create_uri("graph", g.id, g.title)
            graph_uris[g.id] = g_uri
            triples = (
                f"{g_uri} a kst:KnowledgeGraph ;\n"
                f'  dc:title                  "{self.esc(g.title)}" ;\n'
                f'  dc:description           "{self.esc(g.description)}" ;\n'
                f'  lom:educationalObjective "{self.esc(g.educational_objective)}" ;\n'
                f'  lom:context              "{self.esc(g.context)}" ;\n'
                f'  dc:language             "{self.esc(g.language)}" .'
            )
            self.insert_triples(triples, "Graph", g.id)

        # Nodes
        for n in data["nodes"]:
            n_uri = self.create_uri("node", n.id, n.title)
            node_uris[n.id] = n_uri
            g_uri = graph_uris.get(n.graph_id)
            link_graph = f"  kst:belongsToGraph {g_uri} ;\n" if g_uri else ""
            triples = (
                f"{n_uri} a kst:Node ;\n"
                f'  dc:title "{self.esc(n.title)}" ;\n'
                + link_graph
            ).rstrip(";\n") + " ."
            self.insert_triples(triples, "Node", n.id)

        # Edges
        for e in data["edges"]:
            e_uri = self.create_uri("edge", e.id)
            s_uri = node_uris.get(e.source_id)
            t_uri = node_uris.get(e.target_id)
            if not (s_uri and t_uri):
                print(f"⚠ Skip Edge {e.id}: missing source/target node")
                continue
            triples = (
                f"{e_uri} a kst:Edge ;\n"
                f"  kst:hasSourceNode {s_uri} ;\n"
                f"  kst:hasTargetNode {t_uri} ."
            )
            self.insert_triples(triples, "Edge", e.id)

        # Tests
        for t in data["tests"]:
            t_uri = self.create_uri("test", t.id, t.title)
            test_uris[t.id] = t_uri
            a_uri = user_uris.get(t.author_id)
            g_uri = graph_uris.get(t.graph_id)
            link_a = f"  kst:hasAuthor {a_uri} ;\n" if a_uri else ""
            link_g = f"  kst:usesGraph {g_uri} ;\n"  if g_uri else ""
            triples = (
                f"{t_uri} a kst:Test ;\n"
                f'  dc:title                  "{self.esc(t.title)}" ;\n'
                f'  dc:description           "{self.esc(t.description)}" ;\n'
                f'  lom:educationalObjective "{self.esc(t.educational_objective)}" ;\n'
                f'  lom:typicalLearningTime  "{self.esc(t.typical_learning_time)}" ;\n'
                f'  lom:context              "{self.esc(t.context)}" ;\n'
                f'  dc:language              "{self.esc(t.language)}" ;\n'
                + link_a + link_g
            ).rstrip(";\n") + " ."
            self.insert_triples(triples, "Test", t.id)

        # Questions
        for q in data["questions"]:
            q_uri = self.create_uri("question", q.id, (q.text or "")[:50])
            question_uris[q.id] = q_uri
            t_uri = test_uris.get(q.test_id)
            n_uri = node_uris.get(q.node_id) if q.node_id else None
            link_t = f"  kst:belongsToTest {t_uri} ;\n" if t_uri else ""
            link_n = f"  kst:mapsToNode {n_uri} ;\n"    if n_uri else ""
            triples = (
                f"{q_uri} a kst:Question ;\n"
                f'  dc:title                 "{self.esc(q.text)}" ;\n'
                f'  lom:educationalObjective "{self.esc(q.educational_objective)}" ;\n'
                f'  lom:difficulty           "{self.esc(q.difficulty)}" ;\n'
                f'  lom:typicalLearningTime  "{self.esc(q.typical_learning_time)}" ;\n'
                f"  kst:isMultichoice        {str(bool(q.is_multichoice)).lower()} ;\n"
                + link_n + link_t
            ).rstrip(";\n") + " ."
            self.insert_triples(triples, "Question", q.id)

        # Answers
        for a in data["answers"]:
            a_uri = self.create_uri("answer", a.id, (a.text or "")[:30])
            answer_uris[a.id] = a_uri
            q_uri = question_uris.get(a.question_id)
            link_q = f"  kst:belongsToQuestion {q_uri} ;\n" if q_uri else ""
            triples = (
                f"{a_uri} a kst:Answer ;\n"
                f'  dc:description "{self.esc(a.text)}" ;\n'
                f"  kst:isCorrect  {str(bool(a.is_correct)).lower()} ;\n"
                + link_q
            ).rstrip(";\n") + " ."
            self.insert_triples(triples, "Answer", a.id)

        # Results
        for r in data["results"]:
            r_uri = self.create_uri("result", r.id)
            t_uri = test_uris.get(r.test_id)
            s_uri = user_uris.get(r.student_id)
            timestamp = (
                r.timestamp.strftime("%Y-%m-%dT%H:%M:%S")
                if getattr(r, "timestamp", None) else "2024-01-01T00:00:00"
            )
            link_t = f"  kst:forTest {t_uri} ;\n"         if t_uri else ""
            link_s = f"  kst:belongsToStudent {s_uri} ;\n" if s_uri else ""
            score = float(r.score or 0.0)
            triples = (
                f"{r_uri} a kst:TestResult ;\n"
                + link_t
                + f'  kst:timestamp "{timestamp}"^^xsd:dateTime ;\n'
                + f"  kst:isUsed   {str(bool(r.is_used)).lower()} ;\n"
                + f"  kst:score    {score} ;\n"
                + link_s
            ).rstrip(";\n") + " ."
            self.insert_triples(triples, "Result", r.id)

        # Student Answers
        answers_by_id: Dict[int, Answer] = {a.id: a for a in data["answers"]}
        for sa in data["student_answers"]:
            sa_uri = self.create_uri("student_answer", sa.id)
            r_uri  = self.create_uri("result", sa.result_id)
            a_uri  = answer_uris.get(sa.answer_id)
            q_uri = None
            ans = answers_by_id.get(sa.answer_id)
            if ans is not None:
                q_uri = question_uris.get(ans.question_id)
            if not (r_uri and a_uri and q_uri):
                print(f"⚠ Skip StudentAnswer {sa.id}: missing related URIs")
                continue
            triples = (
                f"{sa_uri} a kst:StudentAnswer ;\n"
                f"  kst:answersQuestion {q_uri} ;\n"
                f"  kst:selectedAnswer  {a_uri} ;\n"
                f"  kst:belongsToResult {r_uri} ."
            )
            self.insert_triples(triples, "StudentAnswer", sa.id)

        print("✓ Conversion completed.")
