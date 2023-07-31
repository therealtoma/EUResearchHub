# EUResearchHub
![DB](https://img.shields.io/badge/DB-PostgreSQL-green?style=flat)
![python](https://img.shields.io/badge/python-3.10-green?style=flat)
[![docs](https://img.shields.io/badge/docs-link-blue?style=flat)](https://github.com/andreramolivaz/EUResearchHub/tree/main/docs)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/4989423ce1e84a7fb6e80de66447e2f9)](https://app.codacy.com/gh/andreramolivaz/EUResearchHub/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![CodeFactor](https://www.codefactor.io/repository/github/andreramolivaz/euresearchhub/badge)](https://www.codefactor.io/repository/github/andreramolivaz/euresearchhub)

## Description

This project aims to design and implement a web application for the internal evaluation of research projects to be submitted for funding to the European Union. The web application provides a platform for researchers to create new projects for evaluation, each consisting of a textual description and one or more PDF documents for assessment, potentially of different types such as data management plans, ethics deliverables, etc. 

Each project has a specific state, including:
- `Approved`: Evaluators have expressed a favorable opinion, and no further modifications are possible.
- `Submitted` for Evaluation: Submitted for the next evaluation window but not yet assessed.
- `Requires Modifications`: Evaluators have requested changes for further evaluation.
- `Not Approved`: Evaluators have expressed a negative opinion, and no further modifications are possible.

Evaluators can access the projects assigned to them for evaluation in the upcoming window, download the assessment documents, and create evaluation reports for each project. They can also update the project's state, for example, marking it as `Approved`. Researchers have access to the evaluation reports and can review their projects based on the feedback until they are approved or rejected.

Each project maintains a version history to track the different iterations of the evaluation process. Researchers and evaluators should be able to access all previously submitted versions of each document within a project, along with the corresponding evaluation reports. The versions may include auxiliary information detailing the changes compared to previous versions.

The project also includes a messaging component through which researchers and evaluators can interact. For example, researchers can request further clarification on an evaluation received, and evaluators can respond anonymously. Evaluators can insert specific comments directly within the submitted PDFs for evaluation, such as notes. This way, evaluation reports can refer to these specific comments (e.g., "see note on page 4").

> ⚠️ The application relies on an `.env` file to set environment variables. This file is not included in the repository for security reasons. If you want to run the application locally, you will need to create this file and set the needed variables. In addition to this, for the complete experience, you will also need to run the command (you can find them in the DB_design doc) for the creation of the roles, triggers, check and materialized view for data integrity. 

## Features
- Researchers can create new research projects for evaluation.
- Each project consists of a textual description and one or more PDF documents.
- Projects have different states: Approved, Submitted for Evaluation, Requires Modifications, Not Approved.
- Evaluators can access projects for evaluation, download assessment documents, and create evaluation reports.
- Evaluators can update the state of a project.
- Researchers have access to evaluation reports and can revise their projects based on the feedback.
- Projects maintain a version history for documents, including auxiliary information about changes.
- Researchers and evaluators can interact through a messaging system.
- Evaluators can insert comments within the PDFs for evaluation.
- Evaluation reports can reference specific comments within the documents.

## Demo Video

 <div align="center">

 | Webapp presentation |
 |:------------------:|
 | ![Demo Video](https://github.com/andreramolivaz/EUResearchHub/assets/92636448/fed21aa8-1f6e-481f-8e8d-315af82cc304) |

 </div>

 ### Contributors
 - [Alberto Tomasin](https://github.com/therealtoma) 
 - [Simone Dinato](https://github.com/simonedinato) 


## Database Design

For detailed information about the database design, please refer to the [Database Design Documentation](https://github.com/andreramolivaz/EUResearchHub/blob/main/docs/DB_design/summary.md).

## Documentation

For comprehensive documentation of the web application please refer to the [Documentation](https://github.com/andreramolivaz/EUResearchHub/blob/main/docs/report.pdf).


 
