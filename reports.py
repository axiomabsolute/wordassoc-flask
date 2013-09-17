from collections import defaultdict
from Models import Answer
# Report methods
def calculateAccuracyByTech(answers):
    techAnswers = [answer for answer in answers if answer.question.questionType == "snippetToTech"]
    answersByTech = defaultdict(list)
    for answer in techAnswers:
        answersByTech[answer.question.correctAnswer].append(answer)
    result =  {tech: len([x for x in answersByTech[tech] if x.correct])*1.0/len(answersByTech[tech])*1.0 for tech in answersByTech}
    return result

def calculateCorrectByCategory(answers):
    answersByCategory = defaultdict(list)
    for answer in answers:
        answersByCategory[answer.question.questionType].append(answer)
    result = {questionType: len([x for x in answersByCategory[questionType] if x.correct])*1.0/len(answersByCategory[questionType])*1.0 for questionType in answersByCategory}
    return result

def calculateCorrect(answers, nameMap):
    answersByLabel = defaultdict(list)
    for answer in answers:
       if answer.question.questionType == "snippetToTech":
            answersByLabel[nameMap[answer.question.correctAnswer]].append(answer)
       else:
            answersByLabel[nameMap[answer.question.questionType]].append(answer)
    result = {questionType: len([x for x in answersByLabel[questionType] if x.correct])*1.0/len(answersByLabel[questionType])*1.0 for questionType in answersByLabel}
    return result

def getLeaderboard(games):
    result = defaultdict(lambda : -100)
    weightedresult = defaultdict(lambda : -100)
    correctCount = defaultdict(lambda: 0)
    totalCount = defaultdict(lambda: 0)
    answers = Answer.query.all()
    for answer in answers:
        totalCount[answer.question.text] = totalCount[answer.question.text] + 1
        if answer.correct:
            correctCount[answer.question.text] = correctCount[answer.question.text] + 1
    weights = {q:1.5-(correctCount[q]*1.0/(totalCount[q]*1.0)) for q in totalCount.keys()}
    weightedScores = {game.id: sum(map(lambda x: weights[x.question.text] if x.correct else (0.0-0.25), game.answers)) for game in games }
    print(weightedScores)
    for game in games:
        result[game.player] = max(result[game.player], game.score)
        weightedresult[game.player] = max(result[game.player], weightedScores[game.id])
    result = [{"user": p, "score":result[p], "weightedScore":weightedresult[p]} for p in result]
    return [x for x in reversed(sorted(result,key=lambda x: x["score"]))]

def countQuestionsByType(answers, nameMap):
    countsByType = defaultdict(lambda : 0)
    for answer in answers:
        if answer.question.questionType == "snippetToTech":
            countsByType[nameMap[answer.question.correctAnswer]] += 1
        else:
            countsByType[nameMap[answer.question.questionType]] += 1
    return countsByType
