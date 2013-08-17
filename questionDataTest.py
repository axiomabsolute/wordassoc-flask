from questions import question_bank as qb

validQuestionTypes = set(["snippetToTech", "everydayDataStructs", "algorithmToType", "snippetToOODConcept", "generalProgrammingPrinciples"])

def testValidQuestionTypes():
    print("Looking for invalid question types")
    for q in qb["questions"]:
        if q["question_type"] not in validQuestionTypes:
            print(q)

def testSnippetToTechAnswerTypes():
    print("Looking for invalid snippetToTech answers")
    iterateOverAnswerTypeAndConfirm("snippetToTech", "technologies")

def testEverydayDataStructsAnswerTypes():
    print("Looking for invalid dataStruct answers")
    iterateOverAnswerTypeAndConfirm("everydayDataStructs", "data-structures")

def testAlgorithmToTypeAnswerTypes():
    print("Looking for invalid algorithmToType answers")
    iterateOverAnswerTypeAndConfirm("algorithmToType", "algorithm-types")

def testSnippetToOODConceptAnswerTypes():
    print("Looking for invalid snippetToOODConcept answers")
    iterateOverAnswerTypeAndConfirm("snippetToOODConcept", "ood-concepts")

def testGeneralProgrammingPrinciplesAnswerTypes():
    print("Looking for invalid generalProgrammingPrinciples answers")
    iterateOverAnswerTypeAndConfirm("generalProgrammingPrinciples", "general-programming-principles")

# Helper methods
def iterateOverAnswerTypeAndConfirm(questionType, answerSet):
    for q in qb["questions"]:
        if q["question_type"] == questionType and q["question_answer"] not in qb[answerSet]:
            print(q)

if __name__ == "__main__":
    testSnippetToTechAnswerTypes()
    testEverydayDataStructsAnswerTypes()
    testAlgorithmToTypeAnswerTypes()
    testSnippetToOODConceptAnswerTypes()
    testGeneralProgrammingPrinciplesAnswerTypes()
