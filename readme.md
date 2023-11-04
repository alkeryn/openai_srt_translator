the point of this project is to easily translate srt files when i need to because my gf doesn't understand english.  
subtitles are translated in batches of 50 by default, use the `-b` flag to change it.  
the default model is `gpt-3.5-turbo` but you can always use `-m gpt-4`.  
make sure to export the **`OPENAI_API_KEY`** variable.

better result could certainly be achieved by using a sliding context and discarding the begining each time or more advanced techniques;  
however, another objective is to have it being simple enough to fit in a single file of code and this will be good enough in 99% of cases anyway.  

this could probably be used along some text to speech software such as whisper for some pretty cool results.

# Usage

```bash
usage: main.py [-h] [-l LANGUAGE] [-b BATCH_SIZE] [-m MODEL] files [files ...]

Translate srt files

positional arguments:
  files                 File pattern to match

options:
  -h, --help            show this help message and exit
  -l LANGUAGE, --language LANGUAGE
                        Specify the language
  -b BATCH_SIZE, --batch_size BATCH_SIZE
                        Specify the batch size
  -m MODEL, --model MODEL
                        openai's model to use
```
