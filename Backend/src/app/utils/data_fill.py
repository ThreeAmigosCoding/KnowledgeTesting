from ..models import User, Test, Question, Answer, Graph, Node, Edge, Result, StudentAnswer


def init_data(app, db):
    with app.app_context():
        db.drop_all()
        db.create_all()

        professor = User(
            first_name="Marko",
            last_name="Marković",
            email="marko.markovic@school.com",
            role="teacher",
            password="hashed_password"
        )

        student1 = User(
            first_name="Jovan",
            last_name="Jovanović",
            email="jovan.jovanovic@school.com",
            role="student",
            password="hashed_password"
        )
        student2 = User(
            first_name="Ana",
            last_name="Anić",
            email="ana.anic@school.com",
            role="student",
            password="hashed_password"
        )
        student3 = User(
            first_name="Milan",
            last_name="Milić",
            email="milan.milic@school.com",
            role="student",
            password="hashed_password"
        )

        db.session.add_all([professor, student1, student2, student3])
        db.session.commit()

        graph = Graph(title="Prostor znanja - Matematika")
        db.session.add(graph)
        db.session.flush()

        node_linear = Node(title="Linearna jednačina", graph_id=graph.id)
        node_quadratic = Node(title="Kvadratna jednačina", graph_id=graph.id)
        node_cubic = Node(title="Kubna jednačina", graph_id=graph.id)

        db.session.add_all([node_linear, node_quadratic, node_cubic])
        db.session.flush()

        edge1 = Edge(source_id=node_linear.id, target_id=node_quadratic.id, graph_id=graph.id)
        edge2 = Edge(source_id=node_quadratic.id, target_id=node_cubic.id, graph_id=graph.id)

        db.session.add_all([edge1, edge2])
        db.session.flush()

        test = Test(title="Matematika - Jednačine", author=professor, graph_id=graph.id)
        db.session.add(test)
        db.session.flush()

        questions = []
        answers = []
        question_data_list = [
            {
                "text": "Reši x + 5 = 10",
                "node_id": node_linear.id,
                "answers": [
                    {"text": "x = 5", "is_correct": True},
                    {"text": "x = 10", "is_correct": False},
                    {"text": "x = 0", "is_correct": False},
                ]
            },
            {
                "text": "Reši x^2 - 4 = 0",
                "node_id": node_quadratic.id,
                "answers": [
                    {"text": "x = ±2", "is_correct": True},
                    {"text": "x = ±4", "is_correct": False},
                    {"text": "x = 0", "is_correct": False},
                ]
            },
            {
                "text": "Reši x^3 - 8 = 0",
                "node_id": node_cubic.id,
                "answers": [
                    {"text": "x = 2", "is_correct": True},
                    {"text": "x = -2", "is_correct": False},
                    {"text": "x = 0", "is_correct": False},
                ]
            }
        ]

        for question_data in question_data_list:
            question = Question(
                text=question_data["text"],
                is_multichoice=False,
                test_id=test.id,
                node_id=question_data["node_id"]
            )
            db.session.add(question)
            db.session.flush()
            questions.append(question)

            for answer_data in question_data["answers"]:
                answer = Answer(
                    text=answer_data["text"],
                    is_correct=answer_data["is_correct"],
                    question_id=question.id
                )
                db.session.add(answer)
                db.session.flush()
                answers.append(answer)

        db.session.commit()
        results = []
        student_answers = [
            # Student 1: tačno odgovara na sva pitanja
            {
                "student": student1,
                "answers": [1, 4, 7]  # IDs odgovora
            },
            # Student 2: greši jedno pitanje
            {
                "student": student2,
                "answers": [1, 4, 8]  # IDs odgovora
            },
            # Student 3: greši dva pitanja
            {
                "student": student3,
                "answers": [1, 5, 8]  # IDs odgovora
            }
        ]

        for sa in student_answers:
            result = Result(test_id=test.id, student_id=sa["student"].id)
            db.session.add(result)
            db.session.flush()
            results.append(result)

            # Dodaj odgovore za svakog studenta u tabelu student_answers
            for answer_id in sa["answers"]:
                student_answer = StudentAnswer(result_id=result.id, answer_id=answer_id)
                db.session.add(student_answer)

        db.session.commit()
        # print("Podaci uspešno ubačeni!")
