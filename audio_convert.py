import library_location
library_location.set_path_if_library_not_available('ffmpeg','lib','ffmpeg is required for this library, but was not found')

import json
import boto3
import email
from email.mime.multipart import MIMEMultipart
from subprocess import Popen, PIPE
import re

DOMAIN = 'jamiestarke.com'

def lambda_handler (event, context):
    print("Received event: " + json.dumps(event, indent=2))
    message = json.loads(event['Records'][0]['Sns']['Message'])

    email_message = email.message_from_string(message['content'])
    
    new_email = MIMEMultipart()
    new_email['From'] = email_message['To']
    new_email['Reply-To'] = email_message['From']
    new_email['Subject'] = email_message['Subject']
    
    to_address = re.sub(r'([a-z0-9._-]*)@(.+\.)(%s)' % DOMAIN, r'\1@\3',email_message['To'])
    new_email['To'] = to_address
    
    convert_message(email_message)
    
    new_email.attach(email_message)
    
    print("New Message: " + new_email.as_string())
    
    ses_client = boto3.client('ses')
    ses_client.send_raw_email(
        RawMessage={"Data":new_email.as_string()}
    )

def convert_message(message):
    for part in message.walk():
        if part.get_content_type() == "audio/x-wav":
            content = base64_audio_to_base64_mp3(part.get_payload())
            part.set_payload(content)
            filename = part.get_filename().lower().replace('.wav','.mp3')
            
            del part['Content-Disposition']
            del part['Content-Type']
            
            part.add_header('Content-Disposition','attachment', filename=filename)
            part.add_header('Content-Type','audio/mpeg3', name=filename)
    
def base64_audio_to_base64_mp3(audio_base64):
    return audio_bytes_to_mp3_bytes(audio_base64.decode('base64')).encode('base64')
    
def audio_bytes_to_mp3_bytes(audio_bytes):
    process = Popen('ffmpeg -i pipe:0 -f mp3 pipe:1'.split(), stdout=PIPE, stdin=PIPE)
    stdout, stderr = process.communicate(input = audio_bytes)
    
    return stdout
