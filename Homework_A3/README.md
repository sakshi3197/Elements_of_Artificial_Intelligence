# Part 1: Part-of-speech tagging

Here the goal is to mark every word in a sentence with its corresponding parts of speech.
We have used 3 different models to implement parts of speech tagging using Bayes Network.

1. Simple: Naive Bayes:
This is a probabilistic machine learning model that is used for classification task. 
This classifier is based on Bayes Theorem, p(A/B) = (p(B/A)p(A)) / p(B) 
Here We need to find the probability of parts of speech given words and returning the class with maximum 
probability p(class/x1,x2,x3...xn) = (p(x1,x2,x3.....xn/class)p(class))/p(x1,x2,x3...xn)

2. HMM: Viterbi:
The Viterbi algorithm is a dynamic programming algorithm for obtaining the maximum a posteriori probability estimate of 
the most likely sequence of hidden states—called the Viterbi path.
Here parts of speech depends on the previous parts of speech
V(k,v) = max(V(k-1,u)) * transition_probability(v/u) * emission_probability(x,v)

3. Complex: MCMC with Gibbs Sampling:
Gibbs sampling is a Markov chain Monte Carlo (MCMC) algorithm for obtaining a sequence of observations which
are approximated from a specified multivariate probability distribution
Here parts of speech depends on previous two parts of speech.

Train the data:
- We have processed the entire train data to find total word counts, total parts of speech counts,
emission counts, transition counts and before level transition counts
- Emission counts: Counts the no of times a word is assigned to a particular parts of speech
- Transition Counts: Count the no of times a parts of speech comes before a parts of speech
- Before level transition counts: Count the no of times 3 parts of speeches comes one after the other
  (Two previous parts of speech transitions)


ALGORITHM:

Simple: Naive Bayes
- For each word in the sentence we will be calculating the posterior probability using Bayes Theorem.
- Apply laplace smoothing while calculating the log probability to handle 0 probability.
- Compare the total log probabilities of all the parts of speech and add the parts of speech with maximum probability 
for the word.
- After iterating through all test data, we return the final list

HMM: Viterbi
- No of states in the viterbi algorithm is no of words in the test sentence
- For the first word we will be calculating the probability with emission and initial probabilities
- From second, we will be using the transition probability using previous parts of speech and the values at
each step is stored in viterbi table which will be used for next words. 
- Parts of speech of each word which got the highest probability will be stored in the current path.
- For the last word we will check the parts of speech of highest probability and return the path to it

Complex: MCMC with Gibbs Sampling
- Initially we start taking the first sample by using naive bayes. Later we use this sample to generate more
samples
- In create_sample(), probability of parts of speech for a word is calculated and this is used to find the
probabilities of other words. P(Si | (S - {si}), W1,W2,...,Wn)
- For the first, emission and initial probability is used and for the second emission and transition probability
is used and for third emission, transition and before level transition probabilities are used.
- 30 Iterations are used where we used first 10 iterations as burn_in and later used the remaining 20 samples
- Using these samples we take the parts of speech with more count as the tag for the given word


DESIGN DECISIONS:

Logarithms: 
Initially we have calculated without the product of probabilities and later found that small probabilities 
underflow numerical precision, so added log which makes it into sum of logs

Laplace Smoothing: 
Directly used bayes theorem, and while testing with custom inputs found the probability resulted to 
0, so used laplace smoothing to handle zero probability

Probabilities:
If we find new words in test data we used 0.000000001 in HMM Viterbi and MCMC with Gibbs Sampling for
probabilities

First sample in MCMC:
We have taken the first sample from naive bayes, so it can converge quickly with fewer iterations

Iterations in MCMC:
Randomly chose 30 iterations where the first 10 iterations are used for burn-in.

RESULTS:
                  Simple     HMM Complex it's  late  and   you   said  they'd be    here  by    dawn  ''    .    
0. Ground truth   -39.46  -34.37  -42.79 prt   adv   conj  pron  verb  prt    verb  adv   adp   noun  .     .    
1. Simple         -38.88  -33.89  -42.65 prt   adj   conj  pron  verb  prt    verb  adv   adp   noun  .     .    
2. HMM            -38.88  -33.89  -42.65 prt   adj   conj  pron  verb  prt    verb  adv   adp   noun  .     .    
3. Complex        -39.46  -34.37  -42.79 prt   adv   conj  pron  verb  prt    verb  adv   adp   noun  .     .    

==> So far scored 2000 sentences with 29442 words.
                   Words correct:     Sentences correct: 
   0. Ground truth:      100.00%              100.00%
   1. Simple:            93.41%               44.65%
   2. HMM:               95.27%               56.30%
   3. Complex:           94.14%               50.25%

From the above we can see that HMM has better accuracy compare to the MCMC model though it is dependant of
two level previous parts of speech. This could be because of overfitting on the train data.
This issue can be resolved with more iterations with gibbs sampling which may lead to larger amount of time

# Part 2: Reading text

Understanding the problem:
The goal of part 2 is to get the text from a noisy scanned image. We train a model based on the training data and then provide the test data and predict the the text present in the images.

Assumption:
All the text in the test images have fixed height and width of the font. The letters must fit in a 16px * 25px box. Another assumption is that, there are 26 upper case and lower case characters of English.

Here we are using two methods for character recognition:
1) Simple
2) HMM

There are three types of probabilities that are calculated for Hidden Markov Models:
-> Initial Probabilities:
These are the probabilities that a character will be at the starting of the sentence. We use the training data to calculate initial probabilities. For calculating these probabilities we first passed through the training file and got the total of the starting letters of the sentences and then normalized them.

-> Transition probabilities:
The meaning of Transition probabilities is that the probabilities which are associated with transition in state. So this probability stores the probability of one character changing into other.

-> Emission probabilities:
Here, these are the probabilities that store the chances of an alphabet being a particular letter. We have used naive bayes classifier to compute the emission probability of the letters. The array stored as (' ' and '*') of the test characters will be compared against the array of the training characters. The probability that a pixel is noisy, is basically the total numbers of pixels that are not same by total number of pixels.  So the emission probability is finally calculated by taking a product of all the probabilities of individual probabilities.

1)Simplified model:
We used the emission and individual character probabilities to compute this. The alphabet set to the noisy letter was computed from the emission probability and the instances of character.

2)HMM model:
The HMM algorithm uses all the above three computed probabilities. This algorithm uses the probability of the previous character and the probability of changing from previous character to present character. The algorithm holds the previously computed value multiplied by the emission probability of the present character. After calculating the above for the whole set,  the algorithm would go back to the state which is always going to its previous state at the position of the present character.

