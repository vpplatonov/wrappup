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


### Use these keywords and relevance of other words in the vicinity to create
clusters of moments from the transcript that can be called the important highlights of the discussion
with their corresponding timestamps (start & stop time)


### The audio should also have the ability to be searched from the data stored in the elastic search index.
If you can make the search understand intent of the query, for eg “Tell me something about marketing in this conversation”,
in essence looking for moments in the audio where marketing was said, it helps you get a higher score for the hack challenge.
