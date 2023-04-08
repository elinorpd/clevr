import json
import argparse

parser = argparse.ArgumentParser()

# Input options
parser.add_argument('--original', 
                    dest='original', 
                    default=False, 
                    action='store_true',
                    help="whether to preview original or the training,\
                        original being stored in output/CLEVR_questions.json")
parser.add_argument('--questions_file',
                    default='/home/nlp/users/bkroje/clevr/train/captions/recognition_shape.json',
                    help="filepath to one questions json, for example '/home/nlp/users/bkroje/clevr/train/captions/recognition_shape.json'")
parser.add_argument('--verbose', 
                    dest='verbose', 
                    default=False, 
                    action='store_true',
                    help="whether to print the questions or not")

args = parser.parse_args()

if args.original:
    q = json.load(open('/home/nlp/users/bkroje/clevr/output/CLEVR_questions.json'))
    if args.verbose:
        for i in q['questions']:
            print(f"{i['image_filename']}")
            print(f"Q: {i['question']}\nA: {i['answer']}\n")
    print(len(q['questions']))
else: 
    q = json.load(open(args.questions_file))
    if args.verbose:
        for k, v in q.items():
            print(k,v[0])
    print(len(q))