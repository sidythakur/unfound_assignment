import wikipedia
import re
import nltk
nltk.download('punkt')
nltk.data.path.append('./nltk_data/nltk.txt') 
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pandas as pd
def unfound(phrase,n):
    
    links = wikipedia.search(phrase)
    corpus = set()
    res=[]
    if(len(links)==0):
        res.append("Null")
    else:
          
        for i in range(len(links)):
            try:
                link=links[i]
                print(link)
                res.append(link)
                
                link = wikipedia.page(link).content
                head , sep , tail = link.partition('== See also ==')
                corpus.add(re.sub("\n|\r" , '', head))
            except:
                i=i+1
        res.append("Your result is here")
        all_documents_data=[]

        for data in corpus:
            all_documents_data.append(sent_tokenize(data))

        df = pd.DataFrame(columns = ['sentences','year','sum','keyword'])
        temporal = ["today","tomorrow","yesterday"]

        count = 0

        for data in all_documents_data:

            for i in data:
                if(re.search("[0-9]{4}",i)): 
                    year = (word_tokenize(re.sub('[^0-9 ]', ' ', i)))
                    ans = 0
                    for day in year:
                        if len(day) == 4:
                            ans = day
                            break                 
                    df.loc[count, ['sentences','year']] = [i,int(ans)]
                    count += 1
                for t in temporal:
                    if (t in i and i not in df['sentences'][:]):
                        df.loc[count, ['sentences','year']] = [i,int(2018)]
                        count += 1

        final_sentence_freq = dict()
        ps = PorterStemmer()
        for document in all_documents_data:
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
            df["sum"][i] = 0.0

        for i in range(len(df["sentences"])):
            for words in df["keyword"][i]:       
                if words in final_sentence_freq:
                    df["sum"].values[i] = final_sentence_freq.get(words) + df["sum"][i]
            df["sum"][i] = df["sum"][i]/len(df["keyword"][i])

        similarity_matrix = [[0 for x in range(len(df["sentences"]))] for y in range(len(df["sentences"]))]

        for i in range(len(df["sentences"])):
            for j in range(len(df["sentences"])):
                if j != i and df['year'][j] == df['year'][i] :
                    for word in df['keyword'][i] :
                        if word in df['keyword'][j]:
                            similarity_matrix[i][j] =  similarity_matrix[i][j] + 1

        for i in range(len(df["sentences"])):
            for j in range(len(df["sentences"])):
                similarity_matrix[i][j] =  (similarity_matrix[i][j] / len(df['keyword'][i]))*100 

        sent_removal_list = [] 

        for i in range(len(df["sentences"])):
            for j in range(len(df["sentences"])):
                if similarity_matrix[i][j] > 50:
                    sent_removal_list.append(i)
                    similarity_matrix[j][i] = 0
                    break

        df = df.drop(sent_removal_list)
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
    
