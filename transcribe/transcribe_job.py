"""
    Have a speech file in .WAV or .MP4 format that is stored in an S3 bucket that has the proper permissions.
    The location must be in the same region as the endpoint that you are calling.
    This example assumes that the file is in an Amazon S3 bucket named

        test-transcribe

    and that the file name is

        C4W2L01.mp4
"""

from __future__ import print_function
import time
import boto3
import requests
import re
import json
from types import SimpleNamespace as Namespace

accountId = ''
auth = ''

# must satisfy regular expression pattern: ^[0-9a-zA-Z._-]+
job_name = "Andrew-Ng-Lecture-Transcribe"
s3_endpoint = "wrappup-west.s3.amazonaws.com"
s3_endpoint_region = "wrappup-west.s3-us-west-2.amazonaws.com"
job_uri = f'https://{s3_endpoint_region}/test-transcribe/C4W2L01.mp4'


def transcribe_start_job(jobname=job_name, joburi=job_uri, mformat='mp4'):
    transcribe = boto3.client('transcribe')
    transcribe.start_transcription_job(
        TranscriptionJobName=jobname,
        Media={'MediaFileUri': joburi},
        MediaFormat=mformat,
        LanguageCode='en-US'
    )
    while True:
        jobstatus = transcribe.get_transcription_job(TranscriptionJobName=jobname)
        if jobstatus['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)

    """
    {
    'TranscriptionJob': 
        {'TranscriptionJobName': 'Andrew-Ng-Lecture', 
        'TranscriptionJobStatus': 'COMPLETED', 
        'LanguageCode': 'en-US', 
        'MediaSampleRateHertz': 44100, 
        'MediaFormat': 'mp4', 
        'Media': {'MediaFileUri': 'https://wrappup-west.s3-us-west-2.amazonaws.com/test-transcribe/C4W2L01.mp4'}, 
        'Transcript': {
            'TranscriptFileUri': 'https://s3.us-west-2.amazonaws.com/aws-transcribe-us-west-2-prod/888736911809/Andrew-Ng-Lecture/asrOutput.json?X-Amz-Security-Token=FQoGZXIvYXdzEOz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDPrqfaCs1Z%2BsOM%2BeRSK3A0O3GqmLXbOtKNWZ75j1%2BVRHofT%2BXQCqE%2BwULaCjSvCs3bR%2FJhA5uKTqwFvnmZw1gMj3N0%2B5somO6nHJfm5qo33%2F%2FdgGl2sipWyVfTKsIlRjrtBCuUVTTby6i5WMj%2FaL1NVtRQ1GZ7JOBNKSVhRbJ%2BXvHwyybzDkGLD8Yk6EHPNAgqNNXzZ7czeaLkyA0VhL%2F17b%2BU6mIRHVIu%2Fr29GjlxHW%2BsOCJ0%2BCEaniw5KFwTAJ8KBmjXWLi1e%2BR2lIkRlzIOz02h9rv8mgklOV%2FE%2BwgpdnKkY6c2R1zDLuo6wom9G1QR%2F0MFuUHQAj7lEMWjmFvgWT8%2FLUs8F2Sd%2FaIo5hM781Z3J7JhZ5Rdsy3niK%2BEdy2btPJX5IO64GPeP7ELgQMshhXOJWYbY5AvvAd518prYI2F4r00wcrKHxN6C00muwwqna36f6kLGRkiYGwvSIRzbwuK1KioBxfcY7852POpCFOXmaTDcn9VQlE9%2BjbRZ9xt940W9XkpU18lZlmOu4IromzNkO80RlnrFnzmE%2Bel6ZhE8TbIifapYjm5qde0bfjnzTBTqI8rXWmjfkj186zvfH%2Bk%2BISE0o2%2BWU3QU%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20180921T184535Z&X-Amz-SignedHeaders=host&X-Amz-Expires=899&X-Amz-Credential=ASIARFLZMHCPMO6A7QNR%2F20180921%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Signature=2ccc618167e2f91af26597ff3fb838760a7ce76483ea94be97c6edd1c134d65b'
        }, 
        'CreationTime': datetime.datetime(2018, 9, 21, 21, 41, 31, 223000, tzinfo=tzlocal()), 
        'CompletionTime': datetime.datetime(2018, 9, 21, 21, 45, 32, 665000, tzinfo=tzlocal()), 
        'Settings': {'ChannelIdentification': False}
        }, 
    'ResponseMetadata': {
        'RequestId': '86e9c5c1-bdce-11e8-8ee6-27c134cf441b', 
        'HTTPStatusCode': 200, 
        'HTTPHeaders': {
            'content-type': 'application/x-amz-json-1.1', 
            'date': 'Fri, 21 Sep 2018 18:45:35 GMT', 
            'x-amzn-requestid': '86e9c5c1-bdce-11e8-8ee6-27c134cf441b', 
            'content-length': '1544', 
            'connection': 'keep-alive'}, 
        'RetryAttempts': 0}
    }
    """
    return jobstatus


def aws_get_answer(uri):
    """
    result links to an Amazon S3 presigned URL that contains the transcription in JSON format
    """
    # r = REQUEST.get(uri, auth=(accountId, auth))
    r = requests.get(uri)
    if r.status_code == 200:
        return r.status_code, r.json()

    # 403, <Expires>2018-09-21T19:00:34Z</Expires>
    return r.status_code, r.text


def aws_object_hook(d):
    if 'TranscriptFileUri' in d:
        raise json.JSONDecodeError(d['TranscriptFileUri'], d['TranscriptFileUri'], 0)

    return Namespace(**d)


if __name__ == '__main__':
    """
    For debug purpose only
    """
    status = transcribe_start_job(job_name, job_uri)
    print(status)

    """
    status = '''{
    "TranscriptionJob": {
        "TranscriptionJobName": "Andrew-Ng-Lecture", 
        "TranscriptionJobStatus": "COMPLETED", 
        "LanguageCode": "en-US", 
        "MediaSampleRateHertz": 44100, 
        "MediaFormat": "mp4", 
        "Media": {"MediaFileUri": "https://wrappup-west.s3-us-west-2.amazonaws.com/test-transcribe/C4W2L01.mp4"}, 
        "Transcript": {
            "TranscriptFileUri": "https://s3.us-west-2.amazonaws.com/aws-transcribe-us-west-2-prod/888736911809/Andrew-Ng-Lecture/asrOutput.json?X-Amz-Security-Token=FQoGZXIvYXdzEOz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDPrqfaCs1Z%2BsOM%2BeRSK3A0O3GqmLXbOtKNWZ75j1%2BVRHofT%2BXQCqE%2BwULaCjSvCs3bR%2FJhA5uKTqwFvnmZw1gMj3N0%2B5somO6nHJfm5qo33%2F%2FdgGl2sipWyVfTKsIlRjrtBCuUVTTby6i5WMj%2FaL1NVtRQ1GZ7JOBNKSVhRbJ%2BXvHwyybzDkGLD8Yk6EHPNAgqNNXzZ7czeaLkyA0VhL%2F17b%2BU6mIRHVIu%2Fr29GjlxHW%2BsOCJ0%2BCEaniw5KFwTAJ8KBmjXWLi1e%2BR2lIkRlzIOz02h9rv8mgklOV%2FE%2BwgpdnKkY6c2R1zDLuo6wom9G1QR%2F0MFuUHQAj7lEMWjmFvgWT8%2FLUs8F2Sd%2FaIo5hM781Z3J7JhZ5Rdsy3niK%2BEdy2btPJX5IO64GPeP7ELgQMshhXOJWYbY5AvvAd518prYI2F4r00wcrKHxN6C00muwwqna36f6kLGRkiYGwvSIRzbwuK1KioBxfcY7852POpCFOXmaTDcn9VQlE9%2BjbRZ9xt940W9XkpU18lZlmOu4IromzNkO80RlnrFnzmE%2Bel6ZhE8TbIifapYjm5qde0bfjnzTBTqI8rXWmjfkj186zvfH%2Bk%2BISE0o2%2BWU3QU%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20180921T184535Z&X-Amz-SignedHeaders=host&X-Amz-Expires=899&X-Amz-Credential=ASIARFLZMHCPMO6A7QNR%2F20180921%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Signature=2ccc618167e2f91af26597ff3fb838760a7ce76483ea94be97c6edd1c134d65b"
        }, 
        "CreationTime": datetime.datetime(2018, 9, 21, 21, 41, 31, 223000, tzinfo=tzlocal()), 
        "CompletionTime": datetime.datetime(2018, 9, 21, 21, 45, 32, 665000, tzinfo=tzlocal()), 
        "Settings": {"ChannelIdentification": False}
        }, 
    "ResponseMetadata": {
        "RequestId": "86e9c5c1-bdce-11e8-8ee6-27c134cf441b", 
        "HTTPStatusCode": 200, 
        "HTTPHeaders": {
            "content-type": "application/x-amz-json-1.1", 
            "date": "Fri, 21 Sep 2018 18:45:35 GMT", 
            "x-amzn-requestid": "86e9c5c1-bdce-11e8-8ee6-27c134cf441b", 
            "content-length": "1544",
            "connection": "keep-alive"},
        "RetryAttempts": 0}
    }'''
    """

    try:
        # TranscriptObj = json.loads(status, object_hook=aws_object_hook)
        TranscriptFileUri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    except json.JSONDecodeError as ex:
        TranscriptFileUri = ex.msg

    print(TranscriptFileUri)
    transcribeJSON = aws_get_answer(TranscriptFileUri)

    print(transcribeJSON)
