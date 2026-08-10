
# Intro to HPC Bootcamp 2026  
Repository for training materials, project resources, and preparatory content for the **Intro to HPC Bootcamp**, held in person at **Argonne National Laboratory (ANL)** in **August 2026**. The Bootcamp is hosted by the **Argonne Leadership Computing Facility (ALCF)**.

---

<br>

## Overview  

This repository contains all materials supporting the *Intro to HPC Bootcamp 2026*, including:

- Project-based exercises  
- Preparatory and reference materials
- Presentations
- Hands-on tutorials
- Links to external documentation and HPC resources  

Use this repository as a working area to experiment with HPC concepts, examples, and hands‑on coding exercises.

---

<br>

## Repository Structure  

```
Intro-HPC-2026/
├── Presentations/
├── Projects/
│   ├── Project01/
│   ├── Project02/
│   ├── ...
│   └── Project10/
├── Resources/
└── Tutorials/
```

<br>

**[Presentations](./Presentations)**  
Presentation materials from Bootcamp keynotes, lectures, and other sessions.

**[Projects](./Projects)**  
Project materials organized by Bootcamp project (`Project01–Project10`). Individual project directories contain resources, example code, exercises, and guidance provided by the project teams.

**[Resources](./Resources)**  
Reference and preparatory materials supporting the Bootcamp, including the Prep Pack and other resources covering foundational HPC concepts, command-line tools, Git/GitHub, Jupyter, and related topics.

**[Tutorials](./Tutorials)**  
Hands-on tutorials, Jupyter notebooks, and supporting educational materials used throughout the Bootcamp.

---

<br>

## Getting Started

**New to the Bootcamp?** Check out the [Prep Pack](./Resources/Prep-Pack) to review Python, Jupyter, command-line tools, Git/GitHub, and foundational HPC concepts.

---

<br>

## Goals of the Bootcamp  

- Introduce high‑performance computing concepts  
- Teach participants how to run and optimize jobs on large-scale computing systems
- Explore parallel programming models (MPI, OpenMP, GPU computing, etc.)  
- Provide hands-on experience using ALCF resources  
- Develop practical workflows used in scientific computing  

---

<br>

## Cloning the Repository  

Clone the repository to your local machine:

```bash
git clone https://github.com/Wilber/Intro-HPC-2026.git
cd Intro-HPC-2026
```

---

<br>

## Contributing  

This repository is collaborative. Contributors with write access should create a branch for their changes rather than working directly on `main`.

### 1. Creating a Branch  
```bash
git checkout -b <branch-name>
```

Example:  
```bash
git checkout -b add-project3-examples
```

<br>

### 2. Make and Commit Your Changes 

Stage your changes:

```bash
git add .
```

Commit them with a descriptive message:

```bash
git commit -m "Describe your change clearly"
```

<br>

### 3. Push Your Branch  

```bash
git push -u origin <branch-name>
```

<br>

### 4. Open a Pull Request  

After pushing your branch, go to the [Intro-HPC-2026 Pull Requests page](https://github.com/Wilber/Intro-HPC-2026/pulls).

- Select “New Pull Request”  
- Choose your branch  
- Add a clear title and description of your changes  
- Submit the pull request for review  

