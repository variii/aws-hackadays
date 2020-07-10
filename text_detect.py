import csv
import boto3
import spacy
from spacy import displacy

nlp = spacy.load("en_ner_bc5cdr_md")

def unique_list(s):
	l = s.split()
	k = []
	for i in l:
		if (s.count(i)>1 and (i not in k)or s.count(i)==1): 
			k.append(i)
	return (' '.join(k))

with open('ly_cred.csv','r') as input:
	next(input)
	reader = csv.reader(input)
	for col in reader:
		access_id = col[2]
		secret_key = col[3]
		
photo = 'test2.jpg'

client = boto3.client('rekognition', aws_access_key_id = access_id, aws_secret_access_key = secret_key)

with open(photo, 'rb') as source_image:
	source_bytes = source_image.read()
	
response = client.detect_text(Image={'Bytes': source_bytes})

# print (response["TextDetections"])

detect = response["TextDetections"]

alltext = ""

for line in detect:
	# print(line["DetectedText"])
	alltext = alltext + " " + line["DetectedText"]

	
alltext = unique_list(alltext)
# print(alltext)

'''
doc = nlp(alltext.lower())

for ent in doc.ents:
	print(ent, ent.label_)
'''	

client2 = boto3.client(service_name='comprehendmedical', region_name='us-east-1')
result2 = client2.detect_entities(Text= alltext)
entities = result2['Entities'];
for entity in entities:
	if entity['Type'] == 'GENERIC_NAME' and entity['Score'] > 0.7:
		med = entity['Text']
		print(med)
	
	
