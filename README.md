# Description

### Take any podcast from youtube, run it through a publicly available speech to text engine.

video [C4W2L01 Why look at case studies?](https://www.youtube.com/watch?v=-bvTzZCEOdM&list=PLkDaE6sCZn6Gl29AoE31iwdVwSG-KnDzF&index=12)

put your .WAV or .MP4 file on S3 bucket
```
$ python3 ./transcribe/transcribe_upload
```

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

result
```
{
    "_index": "podcast",
    "_type": "records",
    "_id": "B-cA_mUBn9pTplpGA7is",
    "_score": 1,
    "_source": {
        "jobName": "Andrew-Ng-Lecture-Transcribe",
        "accountId": "888736911809",
        "results": {
            "transcripts": [
                {
                    "transcript": "Hello and welcome back this week the first thing we'll do is show you a number of case studies of effective convolution all your networks so why look a case studies last week to learn about the basic building plots such as accomplished all layers proving this and fully connected layers of confidence it turns out along the past few years of computer vision research has been on hard to put together these basic building blocks to form effective convolution your networks and one of the best ways for use again intuition yourself is to see some of these examples i think just as many of you might have learned to write code by reading other people's code, i think that the good way to get intuition hard bill confidence is the weed or to see other examples of effective confidence and it turns out that a net new network architecture there works well on one computer vision toss often worlds well on other tacis well stations, maybe on your toss. So if someone else's train in your network has always figured out and you're in the calm protector there's very good at recognizing cats and dogs and people but you have a different computer vision task that maybe your trumpet also driving home you might well be able to take someone. Else's knew that to aguatecture and apply that to your problem. And finally, after the next few videos, you be able to read some of the research papers from the future of computer vision and i hope that you might find it satisfying as well you don't have to do this is klaus we hoped you might find it satisfying to read you know some of these seminal computervision research paper and see yourself able to understand so that let's get started as an outline for what we do in the next few videos we'll first show you a few classic networks so the net five network which came from because in nineteen eighties alice net which is often cited in the v gina at work and these are examples of pretty effective new networks and some of the ideas later foundation for modern come on division and you see ideas in these papers they're probably useful for your own and you see ideas from these papers that will probably be useful for your own work as well then want want to show you the resident or called residual network and you might have heard that new and that's where is getting deeper and deeper the rest net new and that's where train's a very very deep one hundred fifty two layer and your network then has some very interesting tricks interesting ideas how to do that effect of the on dh then finally also see a case study of thie inception your network after seeing these your networks i think you have much better intuition about how to build effective convolution you're in that world and even if you end up not working, computer vision yourself, i can. You find a lot of the ideas from some music's apples, such as residents, inception, that's, where many of these ideas across fertilizing are making their way in tow. Other disciplines, even if you don't end up building computervision africans yourself, i think you'll find some of these ideas very interesting and helpful for your work."
                }
            ],
            "items": [
                {
                    "start_time": "0.225",
                    "end_time": "0.705",
                    "alternatives": [
                        {
                            "confidence": "0.7869",
                            "content": "Hello"
                        }
                    ],
                    "type": "pronunciation"
                },
```

### Based on the keywords, identify the top 20 relevant keywords that categorizes that transcript.
It should account for factors such as uniqueness of word, frequency and relevance in the transcript

#### Download dataset for training
```
$ python3 dataset.py
```

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

### Use these keywords and relevance of other words
in the vicinity to create clusters of moments from the transcript that can be called
the important highlights of the discussion with their corresponding timestamps (start & stop time)


### The audio should also have the ability to be searched from the data stored in the elastic search index.
If you can make the search understand intent of the query, for eg “Tell me something about marketing in this conversation”,
in essence looking for moments in the audio where marketing was said, it helps you get a higher score for the hack challenge.
