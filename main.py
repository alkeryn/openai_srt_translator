#!/usr/bin/env python

import srt
import argparse
import openai
import json
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

BATCHSIZE = 50 # later i may use a token conter instead but this is simpler for now
LANG = "french"
MODEL = "gpt-3.5-turbo"

prompt = f"""You are a professional translator.
Translate the text below line by line into {LANG}, do not add any content on your own, and aside from translating, do not produce any other text, you will make the most accurate and authentic to the source translation possible.

you will reply with a json array that only contain the translation excluding the separation format and numbers."""

def makebatch(chunk):
    return [x.content for x in chunk]

def translate_batch(batch):
    blen = len(batch)
    tbatch = []
    batch = json.dumps(batch, ensure_ascii=False)

    lendiff = 1
    while lendiff: # TODO add try catch retry
        completion = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": batch}
            ]
        )
        tbatch = json.loads(completion.choices[0].message.content)
        lendiff = len(tbatch) - blen
    return tbatch

def translate_file(subs):
    total_batch = (len(subs) + BATCHSIZE - 1) // BATCHSIZE
    for i in range(0, len(subs), BATCHSIZE):
        print(f"batch {i//BATCHSIZE + 1} / {total_batch}")

        chunk = subs[i:i+BATCHSIZE]
        batch = makebatch(chunk)
        batch = translate_batch(batch)

        for j, n in enumerate(batch):
            chunk[j].content = n

def get_translated_filename(filepath):
    root, ext = os.path.splitext(filepath)
    return f"{root}_{LANG}{ext}"

def main():
    parser = argparse.ArgumentParser(description="Translate srt files")
    parser.add_argument("files", help="File pattern to match",nargs="+")
    parser.add_argument("-l", "--language", help="Specify the language", default="french", type=str)
    parser.add_argument("-b", "--batch_size", help="Specify the batch size", default=50, type=int)
    parser.add_argument("-m", "--model", help="openai's model to use", default="gpt-3.5-turbo", type=str)

    args = parser.parse_args()

    files = args.files

    global LANG, BATCHSIZE, MODEL
    LANG = args.language
    BATCHSIZE = args.batch_size
    MODEL = args.model

    if not files:
        print("No files found matching the pattern.")
        return

    for filename in files:
        print(filename)
        sub = open(filename).read()
        subs = list(srt.parse(sub))

        # batch = makebatch(subs[10:15])
        # print(batch)
        # tbatch = translate_batch(batch)
        # print(tbatch)

        translate_file(subs)
        output = srt.compose(subs)

        handle = open(get_translated_filename(filename),"w")
        handle.write(output)
        handle.close()

if __name__ == "__main__":
    main()
