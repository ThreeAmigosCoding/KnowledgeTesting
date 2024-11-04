from ..models import User, Test, Question, Answer


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

        student = User(
            first_name="Jovan",
            last_name="Jovanović",
            email="jovan.jovanovic@school.com",
            role="student",
            password="hashed_password"
        )

        db.session.add(professor)
        db.session.add(student)
        db.session.commit()


        tests = [
            {
                "title": "Matematika - Osnovni nivo",
                "questions": [
                    {
                        "text": "Koliko je 2 + 2?",
                        "is_multichoice": False,
                        "answers": [
                            {"text": "4", "is_correct": True},
                            {"text": "3", "is_correct": False},
                            {"text": "5", "is_correct": False},
                        ]
                    },
                    {
                        "text": "Šta je poluprečnik?",
                        "is_multichoice": False,
                        "answers": [
                            {"text": "Pola prečnika kruga", "is_correct": True},
                            {"text": "Dužina kružnice", "is_correct": False},
                            {"text": "Površina kruga", "is_correct": False},
                        ]
                    },
                    {
                        "text": "Koji broj je prost?",
                        "is_multichoice": True,
                        "answers": [
                            {"text": "4", "is_correct": False},
                            {"text": "7", "is_correct": True},
                            {"text": "5", "is_correct": True},
                        ]
                    }
                ]
            },
            {
                "title": "Geografija - Svet",
                "questions": [
                    {
                        "text": "Koji je glavni grad Francuske?",
                        "is_multichoice": False,
                        "answers": [
                            {"text": "Pariz", "is_correct": True},
                            {"text": "Madrid", "is_correct": False},
                            {"text": "Rim", "is_correct": False},
                        ]
                    },
                    {
                        "text": "Koji kontinent je najveći po površini?",
                        "is_multichoice": False,
                        "answers": [
                            {"text": "Azija", "is_correct": True},
                            {"text": "Evropa", "is_correct": False},
                            {"text": "Afrika", "is_correct": False},
                        ]
                    },
                    {
                        "text": "Koji okean je najveći?",
                        "is_multichoice": False,
                        "answers": [
                            {"text": "Pacifik", "is_correct": True},
                            {"text": "Atlantski", "is_correct": False},
                            {"text": "Indijski", "is_correct": False},
                        ]
                    }
                ]
            },
            {
                "title": "Istorija - Stari vek",
                "questions": [
                    {
                        "text": "Ko je bio prvi rimski car?",
                        "is_multichoice": False,
                        "answers": [
                            {"text": "Avgust", "is_correct": True},
                            {"text": "Julije Cezar", "is_correct": False},
                            {"text": "Kaligula", "is_correct": False},
                        ]
                    },
                    {
                        "text": "U kom veku je počeo srednji vek?",
                        "is_multichoice": False,
                        "answers": [
                            {"text": "5. vek", "is_correct": True},
                            {"text": "4. vek", "is_correct": False},
                            {"text": "6. vek", "is_correct": False},
                        ]
                    },
                    {
                        "text": "Koji grčki filozof je učitelj Aleksandra Velikog?",
                        "is_multichoice": False,
                        "answers": [
                            {"text": "Aristotel", "is_correct": True},
                            {"text": "Platon", "is_correct": False},
                            {"text": "Sokrat", "is_correct": False},
                        ]
                    }
                ]
            }
        ]


        for test_data in tests:
            test = Test(title=test_data["title"], author=professor)
            db.session.add(test)
            db.session.flush()

            for question_data in test_data["questions"]:
                question = Question(
                    text=question_data["text"],
                    is_multichoice=question_data["is_multichoice"],
                    test_id=test.id
                )
                db.session.add(question)
                db.session.flush()

                for answer_data in question_data["answers"]:
                    answer = Answer(
                        text=answer_data["text"],
                        is_correct=answer_data["is_correct"],
                        question_id=question.id
                    )
                    db.session.add(answer)

        db.session.commit()
        print("Data inserted successfully!!!")