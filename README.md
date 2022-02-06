<h1 align="center">Unsupervised movie summarization using script and summary alignment</h1>

## About The Project
This project aims to summarize movies with a set of scenes from the script using the alignment from [Alignarr](https://github.com/paramitamirza/AligNarr).
The dataset is the [Scriptbase corpus](https://github.com/EdinburghNLP/scriptbase).


## How to use

We have the dataset in the folder `test_movies/10_movies`, coming from Scriptbase.

### Requirements
This project requires Python 3.7

Download [GoogleNews-vectors-negative300.bin](https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz) and uncompress.

Install the requirements using
```sh
py -3.7 -m pip install -r env/requirements.txt
```
The summaries are generated with
```sh
py -3.7 alignarr.py
py read_output.py
```
The generated summaries are in the folder `selected_scenes`. The ground truth from [TRIPOD](https://github.com/ppapalampidi/TRIPOD) and random selected scenes are in the folder `Segmented_screenplays`.


The ROUGE score is displayed with
```sh
py rouge.py
```

