import os

@staticmethod
def GetEnvVariables():
    return {
        "producerApiURL":os.environ.get('ProducerApiURL'),
        "classCodeApiURL":os.environ.get('ClassCodeApiURL')
    }
    