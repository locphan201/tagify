# Tagify

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

```bash
python main.py
```

Using version `v1` for more stable. Version `v1` is set as default.
Convert only using version `v1`

## Convert

```bash
python setup.py
```

The project will convert `data/metadata.txt` and return a list of process prompts in json. Assume the prompt is like this `Blurred abstract round lights in blue and red tones with black or dark background.` The prompt will be converted to a json like the example below

```json
{
    "v": "mixkit_v2_00003.mp4", 
    "s": [
        {
            "p": "Blurred abstract round lights in blue and red tones with black or dark background.", 
            "k": [
                "light", "tone", "background"
            ], 
            "n": {
                "light": {
                    "d": [
                        "Blurred", "abstract", "round"
                    ]
                }, 
                "tone": {
                    "d": [
                        "blue"
                    ]
                }, 
                "background": {
                    "d": [
                        "black"
                    ]
                }
            }, 
            "pn": [], 
            "act": []
        }
    ]
}
```

### Note:
 - `v`: Video filename
 - `s`: The full prompt.
 - `p`: Small prompt divided from the full prompt(in seperated sentences)
 - `k`: Keywords
 - `n`: Nouns
 - `d`: Details of the nouns
 - `pn`: Pronouns and special nouns
 - `act`: Activities, actions of the subject

## Compare

Need to run the `load_data()` then pass in the the list of videos with the user input `compare(videos, prompt)`.
Compare function will return the same list of videos but it has been sorted from the closest to farest meanings to the user prompt.

Based on what version you want to use, import module `compare` with its version.

```python
from compare.v1 import load_data, compare 
from compare.v2 import load_data, compare
```

## Version v1

This version will compare the user input to other videos in the list based on the number of matched keywords. And if there is no matched nouns, set the weight as 0 for excluding. All the keywords are treated the same (1 point).

## Version v2

This version is the same as the version v1. However, nouns are treated as 3 points than other types. 