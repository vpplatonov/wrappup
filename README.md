# Description

### Take any podcast from youtube, run it through a publicly available speech to text engine.

put your .WAV or .MP4 file on S3 bucket

### Set up an elastic search client and store the transcript on the elastic search index.

You may choose to set it up on your local machine for testing purposes
on MAC OS X
```
brew cask install homebrew/cask-versions/java8
brew install elasticsearch
brew services start elasticsearch
```

check in browser http://http://localhost:9200/

see [Getting started with Elasticsearch in Python](https://towardsdatascience.com/getting-started-with-elasticsearch-in-python-c3598e718380)

```
(.nlpenv) $ pip3 install elasticsearch
```

### Based on the keywords, identify the top 20 relevant keywords that categorizes that transcript.
It should account for factors such as uniqueness of word, frequency and relevance in the transcript

#### Tokenizing & Stop word & Stemming

#### Extracting the frequency of terms using a Bag of Words model
```
Vocabulary:
 ['building' 'computervision' 'end' 'even' 'find' 'ideas' 'interesting'
 'll' 'think' 'work']

Document term matrix:

         Word     Chunk-1     Chunk-2

    building           2           1
computervision           1           1
         end           1           1
        even           1           1
        find           3           1
       ideas           6           1
 interesting           2           1
          ll           2           1
       think           3           1
        work           2           1
```

#### Topic modeling using Latent Dirichlet Allocation

```
Top 10 contributing words to each topic:

Topic 0
"idea" ==> 2.7%
"els" ==> 1.6%
"find" ==> 1.6%
"mani" ==> 1.6%
"resid" ==> 1.6%
"incept" ==> 1.6%
"way" ==> 1.6%
"make" ==> 1.6%
"appl" ==> 1.6%
"across" ==> 1.6%

Topic 1
"network" ==> 3.4%
"see" ==> 2.2%
"effect" ==> 1.9%
"well" ==> 1.9%
"might" ==> 1.6%
"comput" ==> 1.6%
"vision" ==> 1.6%
"work" ==> 1.6%
"idea" ==> 1.6%
"paper" ==> 1.3%
```

### Use these keywords and relevance of other words in the vicinity to create
clusters of moments from the transcript that can be called the important highlights of the discussion
with their corresponding timestamps (start & stop time)


### The audio should also have the ability to be searched from the data stored in the elastic search index.
If you can make the search understand intent of the query, for eg “Tell me something about marketing in this conversation”,
in essence looking for moments in the audio where marketing was said, it helps you get a higher score for the hack challenge.
