# Knowledge Graph and Test Management System

## Project Overview

This application is a knowledge management system designed to model and analyze student knowledge using **Knowledge Space Theory (KST)**. It utilizes knowledge graphs, tests, and semantic web technologies to create a dynamic platform for educators and students.

### Core Objective
- Implement **Knowledge Space Theory (KST)** to model and analyze a student’s knowledge using graphs and questions.

---

## Key Features

### 1. Graph Creation
![Image](https://github.com/ThreeAmigosCoding/KnowledgeTesting/blob/dev/Project%20Images/graph-create.png)
- Purpose: Allows teachers to create graphs representing knowledge structures (assumed graphs) for tests.
- Features:
  - Add nodes representing specific topics or concepts.
  - Connect nodes with directed edges to define relationships between topics.
  - Editable fields include the graph title, node titles, and edge connections.
  - Provides a visual preview of the graph as it’s being created.

---

### 2. Test Creation
![Image](https://github.com/ThreeAmigosCoding/KnowledgeTesting/blob/dev/Project%20Images/test-create.png)
- Purpose: Allows teachers to create tests by associating questions with specific topics in the knowledge graph.
- Features:
  - Fields for test title, question input, and answers.
  - Mark answers as correct or incorrect.
  - Associate each question with a specific node in the knowledge graph.

---

### 3. Tests Overview
![Image](https://github.com/ThreeAmigosCoding/KnowledgeTesting/blob/dev/Project%20Images/tests-overview.png)
- Purpose: Offers a dashboard where teachers can see all the tests they have created.
- Features:
  - Lists test titles, authors, and the number of questions in each test.
  - Includes a “Create Test” button for adding new tests.

---

### 4. Test Overview
![Image](https://github.com/ThreeAmigosCoding/KnowledgeTesting/blob/dev/Project%20Images/test-overview.png)
- Purpose: Displays a summary of a single test, including its questions and their answers.
- Features:
  - Highlights correct answers for easy review.
  - Provides options for exporting tests in standardized formats (e.g., IMS QTI).

---

### 5. Student Result Overview
![Image](https://github.com/ThreeAmigosCoding/KnowledgeTesting/blob/dev/Project%20Images/student-result-overview.png)
- Purpose: Displays detailed test results for individual students.
- Features:
  - Shows each question, its options, and the student’s selected answers.
  - Correct and incorrect answers are visually distinguished with colors (green for correct, red for incorrect).
  - Includes icons (checkmarks and crosses) to emphasize correctness.

---

### 6. Teacher Results Overview
![Image](https://github.com/ThreeAmigosCoding/KnowledgeTesting/blob/dev/Project%20Images/teacher-results-overview-1.png)
![Image](https://github.com/ThreeAmigosCoding/KnowledgeTesting/blob/dev/Project%20Images/teacher-results-overview-2.png)
- Purpose: Provides a summary of results for all students who have taken a specific test.
- Features:
  - Lists students’ names along with their test completion times.
  - Offers filters for specifying time ranges to generate performance-based knowledge graphs.

---

### 7. Teacher Result Overview
![Image](https://github.com/ThreeAmigosCoding/KnowledgeTesting/blob/dev/Project%20Images/teacher-result-overview.png)
- Purpose: Enables teachers to view the overall test results and analyze individual student performance.
- Features:
  - Displays test questions and highlights student performance for each.
  - Allows teachers to compare student answers with the correct ones.
  - Includes the knowledge graph representation with colors indicating performance for each topic.

---

### 8. Graphs Comparison
![Image](https://github.com/ThreeAmigosCoding/KnowledgeTesting/blob/dev/Project%20Images/graphs-comparison.png)
- Purpose: Enables the comparison of assumed graphs (teacher-defined) with generated graphs (student performance-based).
- Features:
  - Visualizes both the assumed and generated graphs side by side.
  - Highlights the differences between the two graphs to analyze discrepancies in knowledge structures.

---

## Core Data Models

1. **Test**: Contains questions and is associated with a knowledge graph.
2. **Question**: Each question belongs to a test and a graph node. It has multiple possible answers.
3. **Answer**: Represents possible answers for a question and whether they’re correct or not.
4. **Result**: Stores a student’s test results and their selected answers.
5. **Node and Edge**: Represent topics (nodes) and dependencies between topics (edges) in the graph.

---

## Ontology Integration

- The project integrates **LOM (Learning Object Metadata)** and uses **OWL ontology** to describe resources like tests, questions, and answers.
- **Graph nodes** are mapped to educational objectives, and relationships like `hasQuestion` and `hasAnswer` connect these entities.

---

## IMS QTI Export

- Ability to export tests in the **IMS QTI** format for compatibility with external educational systems.

---

## Graph Visualization

- Dynamic graph visualization component showing nodes and edges:
  - Nodes are dynamically updated based on associated questions (e.g., display question text on hover).
  - Nodes are colored based on the correctness of student answers.
  - This visualization dynamically syncs with the state (e.g., when adding/removing questions).

---

## Tech Stack

<img align="left" alt="Python" width="26px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" style="padding-right:10px;" />
<img align="left" alt="React" width="26px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg" style="padding-right:10px;" />
<img align="left" alt="React" width="26px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" style="padding-right:10px;" />

<br/>
<br/>

**Backend**: Python (Flask), PostgreSQL database. <br/>
**Frontend**: React (TypeScript) for managing tests, graphs, and visualizations. <br/>

## Authors
- [Luka Đorđević](https://github.com/lukaDjordjevic01)
- [Marko Janošević](https://github.com/janosevicsm)

## Academic Context
This project was developed for the purposes of the course [Modern Educational Technologies and Standards](https://stari.ftn.uns.ac.rs/1303412144/savremene-obrazovne-tehnologije-i-standardi).
### Course Professor
- [Goran Savić](https://github.com/savic071)
- [Milan Segedinac](https://github.com/milansegedinac)
