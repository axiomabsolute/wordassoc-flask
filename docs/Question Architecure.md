# Question System Architecture

This document describes the design, goals, and implementation of the question generation system for the application.

## Goals
The goal of the question system is to allow users to add questions to the bank with minimal amounts of repetition and maximum flexibility to match the player's background.

## Design
Questions will be defined in JSON with the following form, which will be explained below:

```json
{"questions": [
    [
        {
            "question_id" : "c26196df6934cc3aa08311aa35c61346",
            "question_text": "HEAD~2",
            "question_answer": "git",
            "question_type": "snippetToTech"
        }, ...
    ]
]}
```

The `question_id` field is a unique identifier for the question.  The question text is a string representing the actual text to display to the user.  It will be embedded in the application using the `<pre>` tag to preserve formatting.  The `question_answer` is the value of the correct answer.  The last field, `question_type`, determines what type of question it is, which in turn determines other behaviors in the application.

In order to dynamically adjust the game to meet with the player's background, only the bare minimum information is given for each question.  Notice in the above definition, only the correct answer is given.  When the application selects questions for the user, it will only select questions which are relevant to the user's background, that is, questions for which the correct answer is part of their listed background technologies or which we assume all players know.  Furthermore, the `question_type` will be used to generate the other answers for the question.  The various question types and answer generation schemes are detailed below.

### snippetToTech
This type of question presents a code snippet to the user and offers two or more answers for the user to select from, depending on the number of technologies the user is comfortable with.  If the user has 4 or technologies in their technology set, they will always have 4 answers to choose from.  If they have 2-3 technologies, they will have 2 or 3 answers respectively.  If they have only one technology listed then this type of question is invalid and will not be used.  Scores for correct answers (and negatives) will scale according to the number of answers (more points for correct anwsers, fewer negatives for wrong ones).

### snippedToOODConcept
This type of question presents a snippet of code to the user and asks them to identify which OOD concept is being demonstrated.  In addition to the data above, the following data will be included for use in this question:

```json
{...,
    "ood-concepts": [
        "overloading", // Dynamic dispatch, late binding
        "overriding", 
        "interface",
        "class",
        "inheritance",
        "object",
        "super",
        "encapsulation",
        "Single Responsibility Principle",
        "Open/closed principle",
        "Liskov Substitution Principle"
    ]
...}
```

There will always be exactly four answers to this type of question and all four answers will appear on this list.

### everydayDataStructs
This type of question presents the user with an everyday item or activity and asks them to match it with one of four data structures that most naturally represents it.  The answers will always be the same pool of four common structures

```json
{...
    "data-structures": ["tree", "list", "map", "set"],...
}
```

### algorithmToType
This type of question presents the user with an algorithm name and asks them to match it with the type, pulled from the following list:

```json
{...
    "algorithm-types": ["search", "sort", "numerical", "machine learning/ai"],...
}

### languageToSnippet
This type is the opposite of the `snippetToTech`, limited to only languages.  In this, the user is given a language and asked to pick which snippet of code could be that language.  Each of the code snippets will be be doing the same, or very similar, tasks.  The format of this type of question is slightly different than the one presented above:

```json
{"questions": [
    [
        ...,
        {
            "question_id" : "c26196df6934cc3aa08311aa35c61346",
            "question_text": "Print 'Hello' in: ",
            "question_answers": [
                {
                    "language","python",
                    "snippet","print('Hello')"
                },....
            ],
            "question_type": "snippetToTech"
        }, ...
    ]
]}
```

## Implementation
The questions will be stored in memory in the Flask application, and will be selected at random to populate the question generation response.  Each question type will have a corresponding function defined that will generate appropriate answers based on the question type, answer, and user's technology set.