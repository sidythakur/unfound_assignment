# Wikipedia-Crawler

Lisiting 'n' important sentences related to the search phrase in chronlogical order


This is one of the codes I was told to write in an early competition with following instructions
1. Given some input word or phrase, figure out all relevant Wikipedia articles. If there’s
nothing relevant, return null.
2. Create a timeline from these articles. To do that, extract all sentences with dates (&
temporal words like yesterday, tomorrow, etc). Return only best n (NOT necessarily first
n) sentences in timeline in chronological order. [we leave it up to how you infer best]
3. Create a microservice (BONUS: host it on Heroku or similar) which takes some
word/phrase and a number n as input, & returns these
a. All relevant Wikipedia page name (return null if irrelevant)
b. Best n timeline sentences
