# Project 7: Teaching Students to Leverage LLMs for Regulatory Genomics on HPC

This project introduces students to **genomic language models, DNA tokenization, Transformer models, and GPU computing on NERSC Perlmutter**.

Students work with **CTCF ChIP-seq DNA sequences** and follow one of two beginner-friendly learning paths.

## Project pathways

### Group A — Pretrained DNABERT

Students learn how a pretrained genomic language model works and then fine-tune DNABERT on multiple GPUs.

```text
Notebook 1
Understand and fine-tune DNABERT
        ↓
Notebook 3A
Scale DNABERT training on Perlmutter
```

### Group B — Build a Transformer

Students explore DNA tokenization strategies, build a custom Transformer with PyTorch, and then scale their model on multiple GPUs.

```text
Notebook 2
Build and understand a DNA Transformer
        ↓
Notebook 3B
Choose a tokenizer and scale training on Perlmutter
```

Both groups finish with:

```text
Notebook 4
Use the trained model on new CTCF DNA
from a different human cell type
```

## Getting started

Clone the Project 7 repository into your Perlmutter scratch space:

```bash
cd $SCRATCH

git clone https://github.com/joserico00/Intro-to-HPC-Bootcamp-Teaching-Students-to-Leverage-LLMs-for-Regulatory-Genomics-on-HPC.git

cd Intro-to-HPC-Bootcamp-Teaching-Students-to-Leverage-LLMs-for-Regulatory-Genomics-on-HPC
```

The required K562 CTCF training dataset and DNABERT model are already available on Perlmutter, so students do not need to download them.

For full setup instructions, notebook descriptions, datasets, and exercises, see the [Project 7 repository](https://github.com/joserico00/Intro-to-HPC-Bootcamp-Teaching-Students-to-Leverage-LLMs-for-Regulatory-Genomics-on-HPC).
