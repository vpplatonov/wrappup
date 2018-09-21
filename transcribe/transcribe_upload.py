"""
    you should never have a need to put credentials in a source (.py) file.
    Instead, store credentials in a configuration file.
    The SDK will automatically retrieve them.
    The easiest way to create the file is with the AWS Command-Line Interface (CLI)

    Buckets List
    $ aws s3api list-buckets --query "Buckets[].Name"

    Object List
    $ aws s3api list-objects --bucket wrappup --query 'Contents[].{Key: Key, Size: Size}'

    arn:aws:s3:::wrappup-west
"""

import boto3
import logging

Bucket = "wrappup-west"
File = './files/C4W2L01.mp4'


def s3_upload(file):
    """
     import boto3

     bucket_name = 'my-bucket'
     content = open('local-file.txt', 'rb')

     s3 = boto3.client('s3')
     s3.put_object( Bucket=bucket_name, Key='directory-in-bucket/remote-file.txt', Body=content )

    :param file:
    :return:
    """
    name = file.split('/').pop()
    client = boto3.client('s3')
    client.upload_file(file, Bucket, f'test-transcribe/{name}')


def s3_download(s3_file_path = 'test-transcribe/C4W2L01.mp4'):
    save_as = 'local_file_name.txt'
    s3 = boto3.client('s3')
    s3.download_file(Bucket, s3_file_path, save_as)  # Prints out contents of file with open(save_as) as f: print(f.read())


def s3_bucket_list():
    s3 = boto3.client('s3')
    s3_list = s3.list_buckets()
    return s3_list


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)

    ''' Upload file on S3 for transcribe job '''
    s3_upload(File)
    # check bucket
    print(str(s3_bucket_list()))
