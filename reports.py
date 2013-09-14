from collections import defaultdict
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

def getLeaderboard(games):
    result = defaultdict(lambda : -100)
    for game in games:
        result[game.player] = max(result[game.player], game.score)
    result = [{"user": p, "score":result[p]} for p in result]
    return [x for x in reversed(sorted(result,key=lambda x: x["score"]))]

def countQuestionsByType(answers):
    countsByType = defaultdict(lambda : 0)
    for answer in answers:
        if answer.question.questionType == "snippetToTech":
            countsByType[answer.question.correctAnswer] += 1
        else:
            countsByType[answer.question.questionType] += 1
    return countsByType
