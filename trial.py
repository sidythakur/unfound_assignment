import wikipedia
import re
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pandas as pd
def unfound(phrase,n):
    
    links = wikipedia.search(phrase)
    corpus = []
    res=[]
    if(len(links)==0):
        res.append("None")
    else:
        res.append(links)
        for i in range(len(links)):
            try:
                link=links[i]
                print(link)
                
                link = wikipedia.page(link).content
                head , sep , tail = link.partition('== See also ==')
                corpus.append(re.sub("\n|\r" , '', head))
            except:
                i=i+1
        corpus = set(corpus)

        documents=[]

        for data in corpus:
            documents.append(sent_tokenize(data))

        df = pd.DataFrame(columns=['sentences','year','sum','keyword'])

        temporal=["today","tomorrow","yesterday"]

        count = 0

        for data in documents:
                
            for i in data:
                if(re.search("[0-9]{4}",i)): 
                    year = (word_tokenize(re.sub('[^0-9 ]', ' ', i)))
                    ans = 0
                    for day in year:
                        if len(day) == 4:
                            ans = day
                            break                 
                    df.loc[count, ['sentences','year']] = [i,ans]
                    count += 1
                for t in temporal:
                    if (t in i and i not in df['sentences'][:]):
                        df.loc[count, ['sentences','year']] = [i,t]
                        count += 1

        final_sentence_freq = dict()
        ps = PorterStemmer()
        for document in documents:
            for data in document:
                data = re.sub('[^A-Za-z0-9$&% ]', ' ', data)
                data = word_tokenize(data.lower())
                data = [ps.stem(word) for word in data if not word in set(stopwords.words('english'))]
                wordfreq = []
                for words in data:
                    if words in final_sentence_freq:                
                        wordfreq.append(data.count(words)+final_sentence_freq.get(words))
                    else:
                        wordfreq.append(data.count(words)) 
                final_sentence_freq.update(dict(zip(data, wordfreq)))

        for i in range(len(df["sentences"])):
            wordfreq = word_tokenize(df['sentences'][i].lower())
            df["keyword"][i] =  [ps.stem(word) for word in wordfreq if not word in set(stopwords.words('english'))]

        for i in range(len(df["sentences"])):
            df["sum"][i] = 0
            
        #for data in df['sentences']:
        #    for words in data:
        #        for i in range(len(df["sentences"])):
        #            if words in df["keyword"][i]:
        #                if words in final_sentence_freq:
        #                    df["sum"].values[i] = final_sentence_freq.get(words) + df["sum"][i]
            
        for i in range(len(df["sentences"])):
            for words in df["keyword"][i]:       
                if words in final_sentence_freq:
                    df["sum"].values[i] = final_sentence_freq.get(words) + df["sum"][i]
            df["sum"][i] = df["sum"][i]/len(df["keyword"][i])
            
        df = df.sort_values(by=['sum'], ascending=False)
        n1=int(n)
        df1 = df.head(n1)
        df1 = df1.sort_values(by=['year'])
        for data in df1['sentences']:
            print(data+"\n##############################")
        
        for data in df1['sentences']:
            d=re.sub("\n","",data)
            res.append(d)
    return res
    