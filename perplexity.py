import math

class ModelEvaluator:

    def __init__(self,model):
        self.model_probs = model

    def prob(self,sentence):
        s = zip(['*','*'] + sentence,range(0,len(sentence) + 2))
        items = [(word + '|' + s[i-2][0] + ',' + s[i-1][0] )for (word,i) in s if word != '*']
        return reduce(lambda acc,x:acc * self.model_probs.get(x,0),items,1)

    def perplexity(self,test):
        #word_count = len(set([word for sentence in test for word in sentence]))
        word_count = len([word for sentence in test for word in sentence])
        logpart = - 1.0 * sum([math.log(self.prob(s),2) for s in test]) / word_count
        return 2**(logpart)




if __name__ == "__main__":
    model = {'the|*,*':1, 'dog|*,the' :0.5, 'cat|*,the':0.5, 'walks|the,cat':1,
             'STOP|cat,walks': 1, 'runs|the,dog':1, 'STOP|dog,runs':1}
    evaluator = ModelEvaluator(model)

    test = [sentence.split() for sentence in ['the dog runs STOP', 'the cat walks STOP', 'the dog runs STOP']]

    print([(sentence, evaluator.prob(sentence)) for sentence in test ])
    print 'perplexity', evaluator.perplexity(test)


