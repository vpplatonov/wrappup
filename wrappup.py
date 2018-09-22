"""
    1. Take any podcast from youtube,
    run it through a publicly available speech to text engine (Amazon Transcribe / Google Speech-to-Text / Sphinx).
    and store the transcript on the elastic search index.

    2. Identify the top 20 relevant keywords that categorizes that transcript.
    (uniqueness of word, frequency and relevance)

    (c) Platonov Valerii 09.2018 v0.1
"""

from __future__ import print_function
import logging
import json
from .elasticsearch.es_index import (
    connect_elasticsearch,
    create_index_aws,
    store_record
)
from .transcribe.transcribe_job import (
    transcribe_start_job,
    job_name,
    job_uri,
    aws_get_answer
)
from .transcribe.transcribe_upload import (
    s3_upload
)

File = './files/C4W2L01.mp4'


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)

    ''' Upload file on S3 for transcribe job '''
    s3_upload(File)

    ''' Part 1 Speech To Text '''
    es_obj = connect_elasticsearch()
    create_index_aws(es_obj)

    TranscriptionJob = transcribe_start_job(job_name, job_uri)
    try:
        # TranscriptObj = json.loads(TranscriptionJob, object_hook=aws_object_hook)
        TranscriptFileUri = TranscriptionJob['TranscriptionJob']['Transcript']['TranscriptFileUri']
    except json.JSONDecodeError as ex:
        TranscriptFileUri = ex.msg

    transcribeJSON = aws_get_answer(TranscriptFileUri)
    # Convert or not to object
    # transcribeJSON = aws_parse_json(transcribeJSON)

    # Save your job to ES index
    store_record(es_obj, transcribeJSON)

    ''' Part 2 Vocabulary (uniqueness of word, frequency and relevance) '''
    # text = read_record(es_obj, 0)



