from ..models import User, Test, Question, Answer, Graph, Node, Edge, Result, StudentAnswer
from datetime import datetime, timedelta


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

        # Create Knowledge Graphs
        # Graph 1: Mathematics - Equations
        math_graph = Graph(title="Prostor znanja - Matematika - Jednačine")
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
        physics_graph = Graph(title="Prostor znanja - Fizika - Mehanika")
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
        chemistry_graph = Graph(title="Prostor znanja - Hemija - Organska hemija")
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

        # Create Tests
        tests_data = [
            {
                "title": "Matematika - Jednačine",
                "author": teachers[0],
                "graph_id": math_graph.id,
                "questions": [
                    {
                        "text": "Reši x + 5 = 10",
                        "node_id": math_nodes["linear"].id,
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
                "questions": [
                    {
                        "text": "Koja je formula za brzinu?",
                        "node_id": physics_nodes["kinematics"].id,
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
                "author": teachers[2],
                "graph_id": chemistry_graph.id,
                "questions": [
                    {
                        "text": "Koja je formula za metan?",
                        "node_id": chemistry_nodes["alkanes"].id,
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

        # Create tests and questions
        all_tests = []
        all_questions = []
        all_answers = []

        for test_data in tests_data:
            test = Test(
                title=test_data["title"],
                author=test_data["author"],
                graph_id=test_data["graph_id"]
            )
            db.session.add(test)
            db.session.flush()
            all_tests.append(test)

            for question_data in test_data["questions"]:
                question = Question(
                    text=question_data["text"],
                    is_multichoice=False,
                    test_id=test.id,
                    node_id=question_data["node_id"]
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

        # Create results and student answers
        # Simulate different student performance patterns with timestamps
        yesterday = datetime.now() - timedelta(days=1)
        today = datetime.now()
        
        student_results = [
            # Students who took tests YESTERDAY - difficulty-based results
            # Student 1 - Yesterday, good at easy topics, struggles with advanced
            {"student": students[0], "timestamp": yesterday, "test_results": [
                {"test_index": 0, "correct_answers": [1, 5, 9]},  # Math - easy topics (linear, quadratic, cubic) correct
                {"test_index": 1, "correct_answers": [25, 29, 33]},  # Physics - easy topics (kinematics) correct
                {"test_index": 2, "correct_answers": [49, 53, 57]}   # Chemistry - easy topics (alkanes, alkenes, alkanes) correct
            ]},
            # Student 2 - Yesterday, good at easy and medium topics
            {"student": students[1], "timestamp": yesterday, "test_results": [
                {"test_index": 0, "correct_answers": [1, 5, 9, 13]},  # Math - easy + medium (rational) correct
                {"test_index": 1, "correct_answers": [25, 29, 33, 37]},  # Physics - easy + medium (energy) correct
                {"test_index": 2, "correct_answers": [49, 53, 57, 61]}   # Chemistry - easy + medium (alcohols) correct
            ]},
            # Student 3 - Yesterday, excellent at easy topics, good at medium
            {"student": students[2], "timestamp": yesterday, "test_results": [
                {"test_index": 0, "correct_answers": [1, 5, 9, 13, 17]},  # Math - easy + medium + advanced (exponential) correct
                {"test_index": 1, "correct_answers": [25, 29, 33, 37, 41]},  # Physics - easy + medium + advanced (momentum) correct
                {"test_index": 2, "correct_answers": [49, 53, 57, 61, 65]}   # Chemistry - easy + medium + advanced (aldehydes) correct
            ]},
            # Student 4 - Yesterday, good at easy topics, struggles with advanced
            {"student": students[3], "timestamp": yesterday, "test_results": [
                {"test_index": 0, "correct_answers": [1, 5, 9, 13]},  # Math - easy + medium correct
                {"test_index": 1, "correct_answers": [25, 29, 33, 37]},  # Physics - easy + medium correct
                {"test_index": 2, "correct_answers": [49, 53, 57, 61]}   # Chemistry - easy + medium correct
            ]},
            # Student 5 - Yesterday, excellent at everything
            {"student": students[4], "timestamp": yesterday, "test_results": [
                {"test_index": 0, "correct_answers": [1, 5, 9, 13, 17, 21]},  # Math - all correct
                {"test_index": 1, "correct_answers": [25, 29, 33, 37, 41, 45]},  # Physics - all correct
                {"test_index": 2, "correct_answers": [49, 53, 57, 61, 65, 69]}   # Chemistry - all correct
            ]},
            # Student 6 - Yesterday, poor at everything
            {"student": students[5], "timestamp": yesterday, "test_results": [
                {"test_index": 0, "correct_answers": [1, 5]},  # Math - 2/6 correct
                {"test_index": 1, "correct_answers": [25, 29]},  # Physics - 2/6 correct
                {"test_index": 2, "correct_answers": [49, 53]}   # Chemistry - 2/6 correct
            ]},
            # Student 7 - Yesterday, good at math, poor at physics and chemistry
            {"student": students[6], "timestamp": yesterday, "test_results": [
                {"test_index": 0, "correct_answers": [1, 5, 9, 13, 17, 21]},  # Math - all correct
                {"test_index": 1, "correct_answers": [25, 29]},  # Physics - 2/6 correct
                {"test_index": 2, "correct_answers": [49, 53]}   # Chemistry - 2/6 correct
            ]},
            # Student 8 - Yesterday, good at physics, poor at math and chemistry
            {"student": students[7], "timestamp": yesterday, "test_results": [
                {"test_index": 0, "correct_answers": [1, 5]},  # Math - 2/6 correct
                {"test_index": 1, "correct_answers": [25, 29, 33, 37, 41, 45]},  # Physics - all correct
                {"test_index": 2, "correct_answers": [49, 53]}   # Chemistry - 2/6 correct
            ]},
            # Student 9 - Yesterday, good at chemistry, poor at math and physics
            {"student": students[8], "timestamp": yesterday, "test_results": [
                {"test_index": 0, "correct_answers": [1, 5]},  # Math - 2/6 correct
                {"test_index": 1, "correct_answers": [25, 29]},  # Physics - 2/6 correct
                {"test_index": 2, "correct_answers": [49, 53, 57, 61, 65, 69]}   # Chemistry - all correct
            ]},
            # Student 10 - Yesterday, average at everything
            {"student": students[9], "timestamp": yesterday, "test_results": [
                {"test_index": 0, "correct_answers": [1, 5, 9, 13]},  # Math - 4/6 correct
                {"test_index": 1, "correct_answers": [25, 29, 33, 37]},  # Physics - 4/6 correct
                {"test_index": 2, "correct_answers": [49, 53, 57, 61]}   # Chemistry - 4/6 correct
            ]},
            
            # Students who took tests TODAY - mixed results
            # Student 11 - Today, poor at everything
            {"student": students[10], "timestamp": today, "test_results": [
                {"test_index": 0, "correct_answers": [1, 5]},  # Math - 2/6 correct
                {"test_index": 1, "correct_answers": [25, 29]},  # Physics - 2/6 correct
                {"test_index": 2, "correct_answers": [49, 53]}   # Chemistry - 2/6 correct
            ]},
            # Student 12 - Today, excellent at everything
            {"student": students[11], "timestamp": today, "test_results": [
                {"test_index": 0, "correct_answers": [1, 5, 9, 13, 17, 21]},  # Math - all correct
                {"test_index": 1, "correct_answers": [25, 29, 33, 37, 41, 45]},  # Physics - all correct
                {"test_index": 2, "correct_answers": [49, 53, 57, 61, 65, 69]}   # Chemistry - all correct
            ]},
            # Student 13 - Today, good at math and physics, poor at chemistry
            {"student": students[12], "timestamp": today, "test_results": [
                {"test_index": 0, "correct_answers": [1, 5, 9, 13, 17, 21]},  # Math - all correct
                {"test_index": 1, "correct_answers": [25, 29, 33, 37, 41, 45]},  # Physics - all correct
                {"test_index": 2, "correct_answers": [49, 53]}   # Chemistry - 2/6 correct
            ]},
            # Student 14 - Today, average at everything
            {"student": students[13], "timestamp": today, "test_results": [
                {"test_index": 0, "correct_answers": [1, 5, 9, 13]},  # Math - 4/6 correct
                {"test_index": 1, "correct_answers": [25, 29, 33, 37]},  # Physics - 4/6 correct
                {"test_index": 2, "correct_answers": [49, 53, 57, 61]}   # Chemistry - 4/6 correct
            ]},
            # Student 15 - Today, good at math, poor at physics and chemistry
            {"student": students[14], "timestamp": today, "test_results": [
                {"test_index": 0, "correct_answers": [1, 5, 9, 13, 17, 21]},  # Math - all correct
                {"test_index": 1, "correct_answers": [25, 29]},  # Physics - 2/6 correct
                {"test_index": 2, "correct_answers": [49, 53]}   # Chemistry - 2/6 correct
            ]},
            # Student 16 - Today, good at physics, poor at math and chemistry
            {"student": students[15], "timestamp": today, "test_results": [
                {"test_index": 0, "correct_answers": [1, 5]},  # Math - 2/6 correct
                {"test_index": 1, "correct_answers": [25, 29, 33, 37, 41, 45]},  # Physics - all correct
                {"test_index": 2, "correct_answers": [49, 53]}   # Chemistry - 2/6 correct
            ]},
            # Student 17 - Today, good at chemistry, poor at math and physics
            {"student": students[16], "timestamp": today, "test_results": [
                {"test_index": 0, "correct_answers": [1, 5]},  # Math - 2/6 correct
                {"test_index": 1, "correct_answers": [25, 29]},  # Physics - 2/6 correct
                {"test_index": 2, "correct_answers": [49, 53, 57, 61, 65, 69]}   # Chemistry - all correct
            ]},
            # Student 18 - Today, good at easy topics, struggles with advanced
            {"student": students[17], "timestamp": today, "test_results": [
                {"test_index": 0, "correct_answers": [1, 5, 9]},  # Math - easy topics correct
                {"test_index": 1, "correct_answers": [25, 29, 33]},  # Physics - easy topics correct
                {"test_index": 2, "correct_answers": [49, 53, 57]}   # Chemistry - easy topics correct
            ]},
            # Student 19 - Today, good at easy and medium topics
            {"student": students[18], "timestamp": today, "test_results": [
                {"test_index": 0, "correct_answers": [1, 5, 9, 13]},  # Math - easy + medium correct
                {"test_index": 1, "correct_answers": [25, 29, 33, 37]},  # Physics - easy + medium correct
                {"test_index": 2, "correct_answers": [49, 53, 57, 61]}   # Chemistry - easy + medium correct
            ]},
            # Student 20 - Today, excellent at easy topics, good at medium
            {"student": students[19], "timestamp": today, "test_results": [
                {"test_index": 0, "correct_answers": [1, 5, 9, 13, 17]},  # Math - easy + medium + advanced correct
                {"test_index": 1, "correct_answers": [25, 29, 33, 37, 41]},  # Physics - easy + medium + advanced correct
                {"test_index": 2, "correct_answers": [49, 53, 57, 61, 65]}   # Chemistry - easy + medium + advanced correct
            ]}
        ]

        # Create results and student answers
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

                for answer_id in test_result["correct_answers"]:
                    student_answer = StudentAnswer(result_id=result.id, answer_id=answer_id)
                    db.session.add(student_answer)

        db.session.commit()
