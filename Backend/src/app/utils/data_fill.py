from ..models import User, Test, Question, Answer, Graph, Node, Edge, Result, StudentAnswer
from datetime import datetime, timedelta
from .sparql_insert_seed import DatabaseToRDFConverter


def init_data(app, db):
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create teachers
        teachers = [
            User(
                first_name="Marko",
                last_name="Marković",
                email="marko.markovic@school.com",
                role="teacher",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Jelena",
                last_name="Petrović",
                email="jelena.petrovic@school.com",
                role="teacher",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Dragan",
                last_name="Nikolić",
                email="dragan.nikolic@school.com",
                role="teacher",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            )
        ]

        # Create students
        students = [
            User(
                first_name="Jovan",
                last_name="Jovanović",
                email="jovan.jovanovic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Ana",
                last_name="Anić",
                email="ana.anic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Milan",
                last_name="Milić",
                email="milan.milic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Sara",
                last_name="Stojanović",
                email="sara.stojanovic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Petar",
                last_name="Pavlović",
                email="petar.pavlovic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Marija",
                last_name="Marinković",
                email="marija.marinkovic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Stefan",
                last_name="Stefanović",
                email="stefan.stefanovic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Jovana",
                last_name="Jovanović",
                email="jovana.jovanovic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Nikola",
                last_name="Nikolić",
                email="nikola.nikolic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Elena",
                last_name="Elić",
                email="elena.elic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Dragan",
                last_name="Draganić",
                email="dragan.draganic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Jelena",
                last_name="Jelenić",
                email="jelena.jelenic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Aleksandar",
                last_name="Aleksić",
                email="aleksandar.aleksic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Tamara",
                last_name="Tomić",
                email="tamara.tomic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Bojan",
                last_name="Bojić",
                email="bojan.bojic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Katarina",
                last_name="Katić",
                email="katarina.katic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Vladimir",
                last_name="Vladić",
                email="vladimir.vladic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Nina",
                last_name="Ninić",
                email="nina.ninic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Marko",
                last_name="Markić",
                email="marko.markic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Sofija",
                last_name="Sofić",
                email="sofija.sofic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Luka",
                last_name="Lukić",
                email="luka.lukic@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            ),
            User(
                first_name="Teodora",
                last_name="Teodorić",
                email="teodora.teodoric@school.com",
                role="student",
                password="$2a$12$nhLsLmGCtqSuCfWj4V5lteOR7LWIyB2Y3N1VfD7jMSwipMsBjqbem"
            )
        ]

        all_users = teachers + students
        db.session.add_all(all_users)
        db.session.commit()

        # Create Knowledge Graphs with LOM properties
        # Graph 1: Mathematics - Equations
        math_graph = Graph(
            title="Prostor znanja - Matematika - Jednačine",
            description="Prostor znanja za matematičke jednačine od osnovnih do naprednih koncepata",
            educational_objective="Razumevanje i rešavanje različitih tipova matematičkih jednačina",
            context="school",
            language="sr"
        )
        db.session.add(math_graph)
        db.session.flush()

        # Nodes for Math Graph
        math_nodes = {
            "linear": Node(title="Linearna jednačina", graph_id=math_graph.id),
            "quadratic": Node(title="Kvadratna jednačina", graph_id=math_graph.id),
            "cubic": Node(title="Kubna jednačina", graph_id=math_graph.id),
            "rational": Node(title="Racionalna jednačina", graph_id=math_graph.id),
            "exponential": Node(title="Eksponencijalna jednačina", graph_id=math_graph.id),
            "logarithmic": Node(title="Logaritamska jednačina", graph_id=math_graph.id)
        }

        db.session.add_all(math_nodes.values())
        db.session.flush()

        # Edges for Math Graph
        math_edges = [
            Edge(source_id=math_nodes["linear"].id, target_id=math_nodes["quadratic"].id, graph_id=math_graph.id),
            Edge(source_id=math_nodes["quadratic"].id, target_id=math_nodes["cubic"].id, graph_id=math_graph.id),
            Edge(source_id=math_nodes["linear"].id, target_id=math_nodes["rational"].id, graph_id=math_graph.id),
            Edge(source_id=math_nodes["quadratic"].id, target_id=math_nodes["exponential"].id, graph_id=math_graph.id),
            Edge(source_id=math_nodes["exponential"].id, target_id=math_nodes["logarithmic"].id, graph_id=math_graph.id),
            Edge(source_id=math_nodes["rational"].id, target_id=math_nodes["exponential"].id, graph_id=math_graph.id)
        ]

        db.session.add_all(math_edges)
        db.session.flush()

        # Graph 2: Physics - Mechanics
        physics_graph = Graph(
            title="Prostor znanja - Fizika - Mehanika",
            description="Prostor znanja za mehaničke koncepte u fizici",
            educational_objective="Razumevanje osnovnih principa mehanike i njihove primene",
            context="school",
            language="sr"
        )
        db.session.add(physics_graph)
        db.session.flush()

        # Nodes for Physics Graph
        physics_nodes = {
            "kinematics": Node(title="Kinematika", graph_id=physics_graph.id),
            "dynamics": Node(title="Dinamika", graph_id=physics_graph.id),
            "energy": Node(title="Energija", graph_id=physics_graph.id),
            "momentum": Node(title="Impuls", graph_id=physics_graph.id),
            "circular": Node(title="Kružno kretanje", graph_id=physics_graph.id),
            "oscillations": Node(title="Oscilacije", graph_id=physics_graph.id),
            "gravitation": Node(title="Gravitacija", graph_id=physics_graph.id)
        }

        db.session.add_all(physics_nodes.values())
        db.session.flush()

        # Edges for Physics Graph
        physics_edges = [
            Edge(source_id=physics_nodes["kinematics"].id, target_id=physics_nodes["dynamics"].id, graph_id=physics_graph.id),
            Edge(source_id=physics_nodes["dynamics"].id, target_id=physics_nodes["energy"].id, graph_id=physics_graph.id),
            Edge(source_id=physics_nodes["energy"].id, target_id=physics_nodes["momentum"].id, graph_id=physics_graph.id),
            Edge(source_id=physics_nodes["kinematics"].id, target_id=physics_nodes["circular"].id, graph_id=physics_graph.id),
            Edge(source_id=physics_nodes["circular"].id, target_id=physics_nodes["oscillations"].id, graph_id=physics_graph.id),
            Edge(source_id=physics_nodes["dynamics"].id, target_id=physics_nodes["gravitation"].id, graph_id=physics_graph.id),
            Edge(source_id=physics_nodes["energy"].id, target_id=physics_nodes["oscillations"].id, graph_id=physics_graph.id)
        ]

        db.session.add_all(physics_edges)
        db.session.flush()

        # Graph 3: Chemistry - Organic Chemistry
        chemistry_graph = Graph(
            title="Prostor znanja - Hemija - Organska hemija",
            description="Prostor znanja za organsku hemiju i funkcionalne grupe",
            educational_objective="Razumevanje osnovnih principa organske hemije i struktura molekula",
            context="school",
            language="sr"
        )
        db.session.add(chemistry_graph)
        db.session.flush()

        # Nodes for Chemistry Graph
        chemistry_nodes = {
            "alkanes": Node(title="Alkani", graph_id=chemistry_graph.id),
            "alkenes": Node(title="Alkeni", graph_id=chemistry_graph.id),
            "alkynes": Node(title="Alkini", graph_id=chemistry_graph.id),
            "alcohols": Node(title="Alkoholi", graph_id=chemistry_graph.id),
            "aldehydes": Node(title="Aldehidi", graph_id=chemistry_graph.id),
            "ketones": Node(title="Ketoni", graph_id=chemistry_graph.id),
            "carboxylic": Node(title="Karboksilne kiseline", graph_id=chemistry_graph.id),
            "esters": Node(title="Estri", graph_id=chemistry_graph.id)
        }

        db.session.add_all(chemistry_nodes.values())
        db.session.flush()

        # Edges for Chemistry Graph
        chemistry_edges = [
            Edge(source_id=chemistry_nodes["alkanes"].id, target_id=chemistry_nodes["alkenes"].id, graph_id=chemistry_graph.id),
            Edge(source_id=chemistry_nodes["alkenes"].id, target_id=chemistry_nodes["alkynes"].id, graph_id=chemistry_graph.id),
            Edge(source_id=chemistry_nodes["alkanes"].id, target_id=chemistry_nodes["alcohols"].id, graph_id=chemistry_graph.id),
            Edge(source_id=chemistry_nodes["alcohols"].id, target_id=chemistry_nodes["aldehydes"].id, graph_id=chemistry_graph.id),
            Edge(source_id=chemistry_nodes["aldehydes"].id, target_id=chemistry_nodes["ketones"].id, graph_id=chemistry_graph.id),
            Edge(source_id=chemistry_nodes["aldehydes"].id, target_id=chemistry_nodes["carboxylic"].id, graph_id=chemistry_graph.id),
            Edge(source_id=chemistry_nodes["carboxylic"].id, target_id=chemistry_nodes["esters"].id, graph_id=chemistry_graph.id),
            Edge(source_id=chemistry_nodes["alcohols"].id, target_id=chemistry_nodes["esters"].id, graph_id=chemistry_graph.id)
        ]

        db.session.add_all(chemistry_edges)
        db.session.flush()

        # Create Tests with LOM properties
        tests_data = [
            {
                "title": "Matematika - Jednačine",
                "author": teachers[0],
                "graph_id": math_graph.id,
                "description": "Test iz matematičkih jednačina različite složenosti",
                "educational_objective": "Provera znanja o rešavanju različitih tipova jednačina",
                "typical_learning_time": "PT30M",
                "context": "school",
                "language": "sr",
                "questions": [
                    {
                        "text": "Reši x + 5 = 10",
                        "node_id": math_nodes["linear"].id,
                        "educational_objective": "Razumevanje osnovnih linearnih jednačina",
                        "difficulty": "very easy",
                        "typical_learning_time": "PT5M",
                        "answers": [
                            {"text": "x = 5", "is_correct": True},
                            {"text": "x = 10", "is_correct": False},
                            {"text": "x = 0", "is_correct": False},
                            {"text": "x = 15", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Reši x^2 - 4 = 0",
                        "node_id": math_nodes["quadratic"].id,
                        "educational_objective": "Rešavanje kvadratnih jednačina",
                        "difficulty": "easy",
                        "typical_learning_time": "PT5M",
                        "answers": [
                            {"text": "x = ±2", "is_correct": True},
                            {"text": "x = ±4", "is_correct": False},
                            {"text": "x = 0", "is_correct": False},
                            {"text": "x = ±1", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Reši x^3 - 8 = 0",
                        "node_id": math_nodes["cubic"].id,
                        "educational_objective": "Rešavanje kubnih jednačina",
                        "difficulty": "medium",
                        "typical_learning_time": "PT5M",
                        "answers": [
                            {"text": "x = 2", "is_correct": True},
                            {"text": "x = -2", "is_correct": False},
                            {"text": "x = 0", "is_correct": False},
                            {"text": "x = 4", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Reši (x+2)/(x-1) = 3",
                        "node_id": math_nodes["rational"].id,
                        "educational_objective": "Rešavanje racionalnih jednačina",
                        "difficulty": "medium",
                        "typical_learning_time": "PT5M",
                        "answers": [
                            {"text": "x = 2.5", "is_correct": True},
                            {"text": "x = 1.5", "is_correct": False},
                            {"text": "x = 3", "is_correct": False},
                            {"text": "x = 0", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Reši 2^x = 8",
                        "node_id": math_nodes["exponential"].id,
                        "educational_objective": "Rešavanje eksponencijalnih jednačina",
                        "difficulty": "difficult",
                        "typical_learning_time": "PT5M",
                        "answers": [
                            {"text": "x = 3", "is_correct": True},
                            {"text": "x = 2", "is_correct": False},
                            {"text": "x = 4", "is_correct": False},
                            {"text": "x = 1", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Reši log₂(x) = 4",
                        "node_id": math_nodes["logarithmic"].id,
                        "educational_objective": "Rešavanje logaritamskih jednačina",
                        "difficulty": "difficult",
                        "typical_learning_time": "PT5M",
                        "answers": [
                            {"text": "x = 16", "is_correct": True},
                            {"text": "x = 8", "is_correct": False},
                            {"text": "x = 4", "is_correct": False},
                            {"text": "x = 32", "is_correct": False}
                        ]
                    }
                ]
            },
            {
                "title": "Fizika - Mehanika",
                "author": teachers[1],
                "graph_id": physics_graph.id,
                "description": "Test iz mehaničkih koncepata u fizici",
                "educational_objective": "Provera razumevanja osnovnih principa mehanike",
                "typical_learning_time": "PT25M",
                "context": "school",
                "language": "sr",
                "questions": [
                    {
                        "text": "Koja je formula za brzinu?",
                        "node_id": physics_nodes["kinematics"].id,
                        "educational_objective": "Razumevanje koncepta brzine",
                        "difficulty": "very easy",
                        "typical_learning_time": "PT3M",
                        "answers": [
                            {"text": "v = s/t", "is_correct": True},
                            {"text": "v = a*t", "is_correct": False},
                            {"text": "v = m*a", "is_correct": False},
                            {"text": "v = F/m", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Koja je formula za ubrzanje?",
                        "node_id": physics_nodes["kinematics"].id,
                        "educational_objective": "Razumevanje koncepta ubrzanja",
                        "difficulty": "very easy",
                        "typical_learning_time": "PT3M",
                        "answers": [
                            {"text": "a = Δv/Δt", "is_correct": True},
                            {"text": "a = v/t", "is_correct": False},
                            {"text": "a = s/t²", "is_correct": False},
                            {"text": "a = F/m", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Koja je formula za put kod jednoliko ubrzanog kretanja?",
                        "node_id": physics_nodes["kinematics"].id,
                        "educational_objective": "Primena formula za put",
                        "difficulty": "easy",
                        "typical_learning_time": "PT4M",
                        "answers": [
                            {"text": "s = v₀t + at²/2", "is_correct": True},
                            {"text": "s = vt", "is_correct": False},
                            {"text": "s = at", "is_correct": False},
                            {"text": "s = v²/2a", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Koja je formula za kinetičku energiju?",
                        "node_id": physics_nodes["energy"].id,
                        "educational_objective": "Razumevanje kinetičke energije",
                        "difficulty": "easy",
                        "typical_learning_time": "PT3M",
                        "answers": [
                            {"text": "E_k = mv²/2", "is_correct": True},
                            {"text": "E_k = mgh", "is_correct": False},
                            {"text": "E_k = Fs", "is_correct": False},
                            {"text": "E_k = ma", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Koja je formula za potencijalnu energiju?",
                        "node_id": physics_nodes["energy"].id,
                        "educational_objective": "Razumevanje potencijalne energije",
                        "difficulty": "easy",
                        "typical_learning_time": "PT3M",
                        "answers": [
                            {"text": "E_p = mgh", "is_correct": True},
                            {"text": "E_p = mv²/2", "is_correct": False},
                            {"text": "E_p = Fs", "is_correct": False},
                            {"text": "E_p = ma", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Koja je formula za impuls?",
                        "node_id": physics_nodes["momentum"].id,
                        "educational_objective": "Razumevanje koncepta impulsa",
                        "difficulty": "medium",
                        "typical_learning_time": "PT4M",
                        "answers": [
                            {"text": "p = mv", "is_correct": True},
                            {"text": "p = ma", "is_correct": False},
                            {"text": "p = Fs", "is_correct": False},
                            {"text": "p = mgh", "is_correct": False}
                        ]
                    }
                ]
            },
            {
                "title": "Hemija - Organska hemija",
                "author": teachers[0],
                "graph_id": chemistry_graph.id,
                "description": "Test iz organske hemije i funkcionalnih grupa",
                "educational_objective": "Provera znanja o organskim jedinjenjima",
                "typical_learning_time": "PT20M",
                "context": "training",
                "language": "sr",
                "questions": [
                    {
                        "text": "Koja je formula za metan?",
                        "node_id": chemistry_nodes["alkanes"].id,
                        "educational_objective": "Prepoznavanje strukture alkana",
                        "difficulty": "very easy",
                        "typical_learning_time": "PT2M",
                        "answers": [
                            {"text": "CH₄", "is_correct": True},
                            {"text": "C₂H₄", "is_correct": False},
                            {"text": "C₂H₆", "is_correct": False},
                            {"text": "C₃H₈", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Koja je formula za etilen?",
                        "node_id": chemistry_nodes["alkenes"].id,
                        "educational_objective": "Prepoznavanje strukture alkena",
                        "difficulty": "very easy",
                        "typical_learning_time": "PT2M",
                        "answers": [
                            {"text": "C₂H₄", "is_correct": True},
                            {"text": "CH₄", "is_correct": False},
                            {"text": "C₂H₆", "is_correct": False},
                            {"text": "C₃H₆", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Koja je formula za etan?",
                        "node_id": chemistry_nodes["alkanes"].id,
                        "educational_objective": "Prepoznavanje strukture alkana",
                        "difficulty": "very easy",
                        "typical_learning_time": "PT2M",
                        "answers": [
                            {"text": "C₂H₆", "is_correct": True},
                            {"text": "CH₄", "is_correct": False},
                            {"text": "C₂H₄", "is_correct": False},
                            {"text": "C₃H₈", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Koja je formula za metanol?",
                        "node_id": chemistry_nodes["alcohols"].id,
                        "educational_objective": "Prepoznavanje strukture alkohola",
                        "difficulty": "easy",
                        "typical_learning_time": "PT3M",
                        "answers": [
                            {"text": "CH₃OH", "is_correct": True},
                            {"text": "C₂H₅OH", "is_correct": False},
                            {"text": "CH₃CHO", "is_correct": False},
                            {"text": "C₂H₅CHO", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Koja je formula za formaldehid?",
                        "node_id": chemistry_nodes["aldehydes"].id,
                        "educational_objective": "Prepoznavanje strukture aldehida",
                        "difficulty": "medium",
                        "typical_learning_time": "PT4M",
                        "answers": [
                            {"text": "CH₃CHO", "is_correct": True},
                            {"text": "CH₃OH", "is_correct": False},
                            {"text": "C₂H₅OH", "is_correct": False},
                            {"text": "C₂H₅CHO", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Koja je formula za etanol?",
                        "node_id": chemistry_nodes["alcohols"].id,
                        "educational_objective": "Prepoznavanje strukture alkohola",
                        "difficulty": "easy",
                        "typical_learning_time": "PT3M",
                        "answers": [
                            {"text": "C₂H₅OH", "is_correct": True},
                            {"text": "CH₃OH", "is_correct": False},
                            {"text": "CH₃CHO", "is_correct": False},
                            {"text": "C₂H₅CHO", "is_correct": False}
                        ]
                    }
                ]
            }
        ]
        additional_tests = [
            {
                "title": "Algebra Extensions — Linear & Quadratic Mix",
                "author": teachers[0],
                "graph_id": math_graph.id,
                "description": "Mixed practice on linear and quadratic equations.",
                "educational_objective": "Strengthen solving skills for linear/quadratic forms.",
                "typical_learning_time": "PT25M",
                "context": "school",
                "language": "en",
                "questions": [
                    {
                        "text": "Solve 3x − 9 = 0",
                        "node_id": math_nodes["linear"].id,
                        "educational_objective": "Apply basic linear equation isolation.",
                        "difficulty": "very easy",
                        "typical_learning_time": "PT3M",
                        "answers": [
                            {"text": "x = 3", "is_correct": True},
                            {"text": "x = −3", "is_correct": False},
                            {"text": "x = 9", "is_correct": False},
                            {"text": "x = 0", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Solve x² − 9x = 0",
                        "node_id": math_nodes["quadratic"].id,
                        "educational_objective": "Factor simple quadratic expressions.",
                        "difficulty": "easy",
                        "typical_learning_time": "PT4M",
                        "answers": [
                            {"text": "x = 0 or x = 9", "is_correct": True},
                            {"text": "x = 3 or x = 6", "is_correct": False},
                            {"text": "x = 9 only", "is_correct": False},
                            {"text": "No real solution", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Solve 2x + 7 = 1",
                        "node_id": math_nodes["linear"].id,
                        "educational_objective": "Manipulate linear expressions.",
                        "difficulty": "very easy",
                        "typical_learning_time": "PT3M",
                        "answers": [
                            {"text": "x = −3", "is_correct": True},
                            {"text": "x = 3", "is_correct": False},
                            {"text": "x = −4", "is_correct": False},
                            {"text": "x = 0", "is_correct": False}
                        ]
                    }
                ]
            },
            {
                "title": "Exponentials & Logarithms — Basics",
                "author": teachers[0],
                "graph_id": math_graph.id,
                "description": "Fundamentals of exponential and logarithmic equations.",
                "educational_objective": "Relate exponential and logarithmic forms.",
                "typical_learning_time": "PT20M",
                "context": "training",
                "language": "de",
                "questions": [
                    {
                        "text": "Löse 5^x = 25",
                        "node_id": math_nodes["exponential"].id,
                        "educational_objective": "Exponentials as repeated multiplication.",
                        "difficulty": "very easy",
                        "typical_learning_time": "PT3M",
                        "answers": [
                            {"text": "x = 2", "is_correct": True},
                            {"text": "x = 5", "is_correct": False},
                            {"text": "x = 1", "is_correct": False},
                            {"text": "x = −2", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Bestimme x: log₁₀(x) = 3",
                        "node_id": math_nodes["logarithmic"].id,
                        "educational_objective": "Inverse relationship of log and exp.",
                        "difficulty": "easy",
                        "typical_learning_time": "PT4M",
                        "answers": [
                            {"text": "x = 1000", "is_correct": True},
                            {"text": "x = 300", "is_correct": False},
                            {"text": "x = 10", "is_correct": False},
                            {"text": "x = 1/1000", "is_correct": False}
                        ]
                    }
                ]
            },
            {
                "title": "Cubic Equations — Roots & Structure",
                "author": teachers[0],
                "graph_id": math_graph.id,
                "description": "Intro to simple cubic equations with integer roots.",
                "educational_objective": "Recognize perfect cube patterns.",
                "typical_learning_time": "PT20M",
                "context": "higher education",
                "language": "it",
                "questions": [
                    {
                        "text": "Risolvi x³ − 27 = 0",
                        "node_id": math_nodes["cubic"].id,
                        "educational_objective": "Find cube roots.",
                        "difficulty": "easy",
                        "typical_learning_time": "PT4M",
                        "answers": [
                            {"text": "x = 3", "is_correct": True},
                            {"text": "x = −3", "is_correct": False},
                            {"text": "x = 9", "is_correct": False},
                            {"text": "Nessuna soluzione reale", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Risolvi x³ = 0",
                        "node_id": math_nodes["cubic"].id,
                        "educational_objective": "Zero-product principle.",
                        "difficulty": "very easy",
                        "typical_learning_time": "PT2M",
                        "answers": [
                            {"text": "x = 0", "is_correct": True},
                            {"text": "x = 1", "is_correct": False},
                            {"text": "x = 3", "is_correct": False},
                            {"text": "x = −1", "is_correct": False}
                        ]
                    }
                ]
            },
            {
                "title": "Rational Equations — Domain & Solutions",
                "author": teachers[0],
                "graph_id": math_graph.id,
                "description": "Practice solving rational equations and checking domains.",
                "educational_objective": "Avoid extraneous solutions in rational forms.",
                "typical_learning_time": "PT30M",
                "context": "other",
                "language": "sr",
                "questions": [
                    {
                        "text": "Reši (2x − 1)/(x − 3) = 1",
                        "node_id": math_nodes["rational"].id,
                        "educational_objective": "Cross-multiplication & restrictions.",
                        "difficulty": "medium",
                        "typical_learning_time": "PT6M",
                        "answers": [
                            {"text": "x = 4", "is_correct": True},
                            {"text": "x = 3", "is_correct": False},
                            {"text": "x = 2", "is_correct": False},
                            {"text": "x = 0", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Odredi domen izraza 1/(x − 5)",
                        "node_id": math_nodes["rational"].id,
                        "educational_objective": "Domain restrictions.",
                        "difficulty": "easy",
                        "typical_learning_time": "PT4M",
                        "answers": [
                            {"text": "x ∈ ℝ \\ {5}", "is_correct": True},
                            {"text": "x ∈ ℝ", "is_correct": False},
                            {"text": "x > 5", "is_correct": False},
                            {"text": "x < 5", "is_correct": False}
                        ]
                    }
                ]
            },
            {
                "title": "Kinematics Refresher — Speed & Acceleration",
                "author": teachers[0],
                "graph_id": physics_graph.id,
                "description": "Core relations in 1D kinematics.",
                "educational_objective": "Connect displacement, velocity, and acceleration.",
                "typical_learning_time": "PT20M",
                "context": "school",
                "language": "en",
                "questions": [
                    {
                        "text": "Which equation gives average speed?",
                        "node_id": physics_nodes["kinematics"].id,
                        "educational_objective": "Average vs instantaneous concepts.",
                        "difficulty": "easy",
                        "typical_learning_time": "PT3M",
                        "answers": [
                            {"text": "v = s / t", "is_correct": True},
                            {"text": "v = a · t", "is_correct": False},
                            {"text": "v = F / m", "is_correct": False},
                            {"text": "v = m · a", "is_correct": False}
                        ]
                    },
                    {
                        "text": "For constant acceleration a, which holds?",
                        "node_id": physics_nodes["kinematics"].id,
                        "educational_objective": "Use SUVAT relations.",
                        "difficulty": "medium",
                        "typical_learning_time": "PT5M",
                        "answers": [
                            {"text": "v² = v₀² + 2as", "is_correct": True},
                            {"text": "v = s/t + at²", "is_correct": False},
                            {"text": "s = v²/2a + t", "is_correct": False},
                            {"text": "a = s/v", "is_correct": False}
                        ]
                    }
                ]
            },
            {
                "title": "Dynamics & Forces — Newton Basics",
                "author": teachers[0],
                "graph_id": physics_graph.id,
                "description": "Quick check on Newton’s laws and force relations.",
                "educational_objective": "Relate net force with acceleration.",
                "typical_learning_time": "PT20M",
                "context": "training",
                "language": "de",
                "questions": [
                    {
                        "text": "Welcher Ausdruck beschreibt das zweite Newtonsche Gesetz korrekt?",
                        "node_id": physics_nodes["dynamics"].id,
                        "educational_objective": "Netto-Kraft und Beschleunigung.",
                        "difficulty": "very easy",
                        "typical_learning_time": "PT2M",
                        "answers": [
                            {"text": "F = m · a", "is_correct": True},
                            {"text": "F = m / a", "is_correct": False},
                            {"text": "F = a / m", "is_correct": False},
                            {"text": "F = m · v", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Ein Körper (m) erfährt konstante Kraft F. Was gilt für a?",
                        "node_id": physics_nodes["dynamics"].id,
                        "educational_objective": "Proportionalität a ∝ F, a ∝ 1/m.",
                        "difficulty": "easy",
                        "typical_learning_time": "PT3M",
                        "answers": [
                            {"text": "a = F/m", "is_correct": True},
                            {"text": "a = m/F", "is_correct": False},
                            {"text": "a = F·m", "is_correct": False},
                            {"text": "a = F²/m", "is_correct": False}
                        ]
                    }
                ]
            },
            {
                "title": "Energy & Work — Conservation",
                "author": teachers[0],
                "graph_id": physics_graph.id,
                "description": "Work–energy theorem and potential energy.",
                "educational_objective": "Apply energy conservation in simple systems.",
                "typical_learning_time": "PT25M",
                "context": "higher education",
                "language": "it",
                "questions": [
                    {
                        "text": "Quale formula esprime l'energia cinetica?",
                        "node_id": physics_nodes["energy"].id,
                        "educational_objective": "Kinetic energy definition.",
                        "difficulty": "very easy",
                        "typical_learning_time": "PT2M",
                        "answers": [
                            {"text": "E_k = ½ m v²", "is_correct": True},
                            {"text": "E_k = m g h", "is_correct": False},
                            {"text": "E_k = F s", "is_correct": False},
                            {"text": "E_k = m a", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Il lavoro netto su un corpo equivale a…",
                        "node_id": physics_nodes["energy"].id,
                        "educational_objective": "Work–energy theorem.",
                        "difficulty": "medium",
                        "typical_learning_time": "PT5M",
                        "answers": [
                            {"text": "variazione di energia cinetica", "is_correct": True},
                            {"text": "variazione di massa", "is_correct": False},
                            {"text": "variazione di impulso", "is_correct": False},
                            {"text": "variazione di carica", "is_correct": False}
                        ]
                    }
                ]
            },
            {
                "title": "Hydrocarbons — Basics",
                "author": teachers[0],
                "graph_id": chemistry_graph.id,
                "description": "Recognize formulas for simple hydrocarbons.",
                "educational_objective": "Differentiate alkanes, alkenes, alkynes.",
                "typical_learning_time": "PT20M",
                "context": "other",
                "language": "en",
                "questions": [
                    {
                        "text": "Which is an alkane?",
                        "node_id": chemistry_nodes["alkanes"].id,
                        "educational_objective": "Classification by saturation.",
                        "difficulty": "very easy",
                        "typical_learning_time": "PT2M",
                        "answers": [
                            {"text": "C₃H₈", "is_correct": True},
                            {"text": "C₂H₄", "is_correct": False},
                            {"text": "C₂H₂", "is_correct": False},
                            {"text": "CH₂O", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Select the correct formula for ethyne.",
                        "node_id": chemistry_nodes["alkynes"].id,
                        "educational_objective": "Triple bond recognition.",
                        "difficulty": "easy",
                        "typical_learning_time": "PT3M",
                        "answers": [
                            {"text": "C₂H₂", "is_correct": True},
                            {"text": "C₂H₄", "is_correct": False},
                            {"text": "C₂H₆", "is_correct": False},
                            {"text": "C₃H₆", "is_correct": False}
                        ]
                    }
                ]
            },
            {
                "title": "Functional Groups — Alcohols & Aldehydes",
                "author": teachers[0],
                "graph_id": chemistry_graph.id,
                "description": "Identify common functional groups and simple examples.",
                "educational_objective": "Map formulas to functional group families.",
                "typical_learning_time": "PT25M",
                "context": "training",
                "language": "de",
                "questions": [
                    {
                        "text": "Welcher Stoff ist ein Alkohol?",
                        "node_id": chemistry_nodes["alcohols"].id,
                        "educational_objective": "OH-Gruppe erkennen.",
                        "difficulty": "easy",
                        "typical_learning_time": "PT3M",
                        "answers": [
                            {"text": "C₂H₅OH", "is_correct": True},
                            {"text": "CH₃CHO", "is_correct": False},
                            {"text": "C₂H₅CHO", "is_correct": False},
                            {"text": "CH₃COOH", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Formaldehyd (Methanal) hat die Formel…",
                        "node_id": chemistry_nodes["aldehydes"].id,
                        "educational_objective": "Aldehyd-Grundformel.",
                        "difficulty": "very easy",
                        "typical_learning_time": "PT2M",
                        "answers": [
                            {"text": "CH₂O (oder HCHO)", "is_correct": True},
                            {"text": "C₂H₅OH", "is_correct": False},
                            {"text": "C₂H₅COOH", "is_correct": False},
                            {"text": "C₂H₆", "is_correct": False}
                        ]
                    }
                ]
            },
            {
                "title": "Carboxylic Acids, Esters & Ketones",
                "author": teachers[0],
                "graph_id": chemistry_graph.id,
                "description": "Intro recognition of carboxylic acids, esters, and ketones.",
                "educational_objective": "Relate functional groups to typical formulas.",
                "typical_learning_time": "PT20M",
                "context": "higher education",
                "language": "it",
                "questions": [
                    {
                        "text": "Qual è la formula generale di un acido carbossilico?",
                        "node_id": chemistry_nodes["carboxylic"].id,
                        "educational_objective": "RCOOH identification.",
                        "difficulty": "medium",
                        "typical_learning_time": "PT5M",
                        "answers": [
                            {"text": "R–COOH", "is_correct": True},
                            {"text": "R–CHO", "is_correct": False},
                            {"text": "R–COOR'", "is_correct": False},
                            {"text": "R–OH", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Un estere ha tipicamente la forma…",
                        "node_id": chemistry_nodes["esters"].id,
                        "educational_objective": "Recognize ester linkage.",
                        "difficulty": "easy",
                        "typical_learning_time": "PT3M",
                        "answers": [
                            {"text": "R–COOR'", "is_correct": True},
                            {"text": "R–COOH", "is_correct": False},
                            {"text": "R–CHO", "is_correct": False},
                            {"text": "R–OH", "is_correct": False}
                        ]
                    },
                    {
                        "text": "Un chetone semplice si può scrivere come…",
                        "node_id": chemistry_nodes["ketones"].id,
                        "educational_objective": "Carbonyl placement in ketones.",
                        "difficulty": "easy",
                        "typical_learning_time": "PT3M",
                        "answers": [
                            {"text": "R–CO–R'", "is_correct": True},
                            {"text": "R–COOH", "is_correct": False},
                            {"text": "R–O–R'", "is_correct": False},
                            {"text": "R–CHO", "is_correct": False}
                        ]
                    }
                ]
            }
        ]
        tests_data+=additional_tests

        # Create tests and questions
        all_tests = []
        all_questions = []
        all_answers = []

        for test_data in tests_data:
            test = Test(
                title=test_data["title"],
                author=test_data["author"],
                graph_id=test_data["graph_id"],
                description=test_data["description"],
                educational_objective=test_data["educational_objective"],
                typical_learning_time=test_data["typical_learning_time"],
                context=test_data["context"],
                language=test_data["language"]
            )
            db.session.add(test)
            db.session.flush()
            all_tests.append(test)

            for question_data in test_data["questions"]:
                question = Question(
                    text=question_data["text"],
                    is_multichoice=False,
                    test_id=test.id,
                    node_id=question_data["node_id"],
                    educational_objective=question_data["educational_objective"],
                    difficulty=question_data["difficulty"],
                    typical_learning_time=question_data["typical_learning_time"]
                )
                db.session.add(question)
                db.session.flush()
                all_questions.append(question)

                for answer_data in question_data["answers"]:
                    answer = Answer(
                        text=answer_data["text"],
                        is_correct=answer_data["is_correct"],
                        question_id=question.id
                    )
                    db.session.add(answer)
                    db.session.flush()
                    all_answers.append(answer)

        db.session.commit()

        yesterday = datetime.now() - timedelta(days=1)
        today = datetime.now()

        # Updated student results structure with "answers" field containing ALL attempted answers
        student_results = [
            # Students who took tests YESTERDAY
            {"student": students[0], "timestamp": yesterday, "test_results": [
                {"test_index": 0, "answers": [1, 6, 9, 14, 18, 22]},  # Math - mix of correct and incorrect
                {"test_index": 1, "answers": [25, 29, 33, 38, 42, 46]},  # Physics - mix of correct and incorrect
                {"test_index": 2, "answers": [49, 55, 57, 62, 66, 70]}   # Chemistry - mix of correct and incorrect
            ]},
            {"student": students[1], "timestamp": yesterday, "test_results": [
                {"test_index": 0, "answers": [1, 5, 9, 13, 18, 22]},  # Math
                {"test_index": 1, "answers": [25, 29, 33, 37, 42, 46]},  # Physics
                {"test_index": 2, "answers": [49, 53, 57, 61, 66, 70]}   # Chemistry
            ]},
            {"student": students[2], "timestamp": yesterday, "test_results": [
                {"test_index": 0, "answers": [1, 5, 9, 13, 17, 22]},  # Math
                {"test_index": 1, "answers": [25, 29, 33, 37, 41, 46]},  # Physics
                {"test_index": 2, "answers": [49, 53, 57, 61, 65, 70]}   # Chemistry
            ]},
            {"student": students[3], "timestamp": yesterday, "test_results": [
                {"test_index": 0, "answers": [1, 5, 9, 13, 18, 21]},  # Math
                {"test_index": 1, "answers": [25, 29, 33, 37, 42, 45]},  # Physics
                {"test_index": 2, "answers": [49, 53, 57, 61, 66, 69]}   # Chemistry
            ]},
            {"student": students[4], "timestamp": yesterday, "test_results": [
                {"test_index": 0, "answers": [1, 5, 9, 13, 17, 21]},  # Math - all correct
                {"test_index": 1, "answers": [25, 29, 33, 37, 41, 45]},  # Physics - all correct
                {"test_index": 2, "answers": [49, 53, 57, 61, 65, 69]}   # Chemistry - all correct
            ]},
            {"student": students[5], "timestamp": yesterday, "test_results": [
                {"test_index": 0, "answers": [2, 6, 10, 14, 19, 23]},  # Math - mostly incorrect
                {"test_index": 1, "answers": [26, 30, 34, 38, 41, 45]},  # Physics - mostly incorrect
                {"test_index": 2, "answers": [50, 53, 58, 62, 67, 71]}   # Chemistry - mostly incorrect
            ]},
            {"student": students[6], "timestamp": yesterday, "test_results": [
                {"test_index": 0, "answers": [1, 5, 9, 13, 17, 21]},  # Math - all correct
                {"test_index": 1, "answers": [26, 30, 34, 38, 43, 47]},  # Physics - mostly incorrect
                {"test_index": 2, "answers": [50, 54, 58, 62, 67, 71]}   # Chemistry - mostly incorrect
            ]},
            {"student": students[7], "timestamp": yesterday, "test_results": [
                {"test_index": 0, "answers": [2, 6, 10, 14, 19, 23]},  # Math - mostly incorrect
                {"test_index": 1, "answers": [25, 29, 33, 37, 41, 45]},  # Physics - all correct
                {"test_index": 2, "answers": [50, 54, 58, 62, 67, 71]}   # Chemistry - mostly incorrect
            ]},
            {"student": students[8], "timestamp": yesterday, "test_results": [
                {"test_index": 0, "answers": [2, 6, 10, 14, 19, 23]},  # Math - mostly incorrect
                {"test_index": 1, "answers": [26, 30, 34, 38, 43, 47]},  # Physics - mostly incorrect
                {"test_index": 2, "answers": [49, 53, 57, 61, 65, 69]}   # Chemistry - all correct
            ]},
            {"student": students[9], "timestamp": yesterday, "test_results": [
                {"test_index": 0, "answers": [1, 5, 10, 13, 18, 22]},  # Math - mixed
                {"test_index": 1, "answers": [25, 29, 34, 37, 42, 46]},  # Physics - mixed
                {"test_index": 2, "answers": [49, 53, 58, 61, 66, 70]}   # Chemistry - mixed
            ]},
            
            # Students who took tests TODAY
            {"student": students[10], "timestamp": today, "test_results": [
                {"test_index": 0, "answers": [2, 6, 10, 14, 19, 23]},  # Math - mostly incorrect
                {"test_index": 1, "answers": [26, 30, 34, 38, 43, 47]},  # Physics - mostly incorrect
                {"test_index": 2, "answers": [50, 54, 58, 62, 67, 71]}   # Chemistry - mostly incorrect
            ]},
            {"student": students[11], "timestamp": today, "test_results": [
                {"test_index": 0, "answers": [1, 5, 9, 13, 17, 21]},  # Math - all correct
                {"test_index": 1, "answers": [25, 29, 33, 37, 41, 45]},  # Physics - all correct
                {"test_index": 2, "answers": [49, 53, 57, 61, 65, 69]}   # Chemistry - all correct
            ]},
            {"student": students[12], "timestamp": today, "test_results": [
                {"test_index": 0, "answers": [1, 5, 9, 13, 17, 21]},  # Math - all correct
                {"test_index": 1, "answers": [25, 29, 33, 37, 41, 45]},  # Physics - all correct
                {"test_index": 2, "answers": [50, 54, 58, 62, 67, 71]}   # Chemistry - mostly incorrect
            ]},
            {"student": students[13], "timestamp": today, "test_results": [
                {"test_index": 0, "answers": [1, 5, 10, 13, 18, 22]},  # Math - mixed
                {"test_index": 1, "answers": [25, 29, 34, 37, 42, 46]},  # Physics - mixed
                {"test_index": 2, "answers": [49, 53, 58, 61, 66, 70]}   # Chemistry - mixed
            ]},
            {"student": students[14], "timestamp": today, "test_results": [
                {"test_index": 0, "answers": [1, 5, 9, 13, 17, 21]},  # Math - all correct
                {"test_index": 1, "answers": [26, 30, 34, 38, 43, 47]},  # Physics - mostly incorrect
                {"test_index": 2, "answers": [50, 54, 58, 62, 67, 71]}   # Chemistry - mostly incorrect
            ]},
            {"student": students[15], "timestamp": today, "test_results": [
                {"test_index": 0, "answers": [2, 6, 10, 14, 19, 23]},  # Math - mostly incorrect
                {"test_index": 1, "answers": [25, 29, 33, 37, 41, 45]},  # Physics - all correct
                {"test_index": 2, "answers": [50, 54, 58, 62, 67, 71]}   # Chemistry - mostly incorrect
            ]},
            {"student": students[16], "timestamp": today, "test_results": [
                {"test_index": 0, "answers": [2, 6, 10, 14, 19, 23]},  # Math - mostly incorrect
                {"test_index": 1, "answers": [26, 30, 34, 38, 43, 47]},  # Physics - mostly incorrect
                {"test_index": 2, "answers": [49, 53, 57, 61, 65, 69]}   # Chemistry - all correct
            ]},
            {"student": students[17], "timestamp": today, "test_results": [
                {"test_index": 0, "answers": [1, 6, 9, 14, 19, 22]},  # Math - mixed
                {"test_index": 1, "answers": [25, 30, 33, 38, 43, 46]},  # Physics - mixed
                {"test_index": 2, "answers": [49, 54, 57, 62, 67, 70]}   # Chemistry - mixed
            ]},
            {"student": students[18], "timestamp": today, "test_results": [
                {"test_index": 0, "answers": [1, 5, 9, 13, 18, 22]},  # Math
                {"test_index": 1, "answers": [25, 29, 33, 37, 42, 46]},  # Physics
                {"test_index": 2, "answers": [49, 53, 57, 61, 66, 70]}   # Chemistry
            ]},
            {"student": students[19], "timestamp": today, "test_results": [
                {"test_index": 0, "answers": [1, 5, 9, 13, 17, 22]},  # Math
                {"test_index": 1, "answers": [25, 29, 33, 37, 41, 46]},  # Physics
                {"test_index": 2, "answers": [49, 53, 57, 61, 65, 70]}   # Chemistry
            ]}
        ]

        # Create results and student answers - storing ALL answers
        for student_data in student_results:
            for test_result in student_data["test_results"]:
                test = all_tests[test_result["test_index"]]
                result = Result(
                    test_id=test.id, 
                    student_id=student_data["student"].id,
                    timestamp=student_data["timestamp"]
                )
                db.session.add(result)
                db.session.flush()

                # Store ALL answers for this test (both correct and incorrect)
                for answer_id in test_result["answers"]:
                    student_answer = StudentAnswer(result_id=result.id, answer_id=answer_id)
                    db.session.add(student_answer)

        db.session.commit()
        
        # Convert database data to RDF and insert into Virtuoso
        print("Starting SPARQL conversion...")
        try:
            converter = DatabaseToRDFConverter()
            converter.convert_and_insert(app, db)
            print("SPARQL conversion completed successfully!")
        except Exception as e:
            print(f"SPARQL conversion failed: {e}")
            # Don't fail the entire data initialization if SPARQL conversion fails
