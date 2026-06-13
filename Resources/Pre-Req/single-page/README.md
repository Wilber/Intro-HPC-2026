# Bootcamp Prep Pack

Hello!

This Prep Pack is designed to help you get comfortable with some of the tools and concepts you’ll encounter during the Intro to HPC Bootcamp. Participants come from many different backgrounds and experience levels, so don’t worry if some of these topics are completely new to you.

The goal is **not** to become an expert before the bootcamp.

The goal is simply to become familiar enough with the tools that when someone says “open a Jupyter notebook,” “clone a GitHub repository,” or “run this command in the terminal,” you’ll think: “Hey! I’ve seen that before.”

Think of this prep work as a guided tour of the HPC landscape before we start the journey together. Explore as much or as little as you need. If you’re already comfortable with a topic, feel free to skim it. If something is brand new, take your time and don’t be afraid to use hints, solutions, or additional resources.

Most importantly: **you belong here, even if you’re a complete beginner.**

<br>

> If you run into any issues, broken links, or have questions while working through these materials, feel free to contact Rene at <rmontelongo@anl.gov>.

---

## Contents

#### Start Here

- [00. Pre-Assessment](#00-pre-assessment-start-here)

#### Lessons

- [01. Python](#01-python)
- [02. Jupyter Notebooks](#02-jupyter-notebooks)
- [03. CLI / Shell](#03-cli--shell)
- [04. Git & GitHub](#04-git--github)

#### Reference Material

- [05. Cheat Sheets](#05-cheat-sheets)

---

## Quick Start Guide

Short on time? Here are the key resources in one place. For additional context and explanations, check out the lessons above.

1. [Complete the Python Self-Assessment](https://elearning.unidata.ucar.edu/metpy/PythonReadiness/selfassessment/)

2. [Work through FutureCoder from "Introducing the Shell" through the "For Loops" section](https://futurecoder.io/course/#toc)

3. [Open and interact with a Jupyter Notebook](https://jupyter.org/try-jupyter/notebooks/?path=notebooks/Intro.ipynb)

4. [Complete the Terminal Tutor lessons](https://www.terminaltutor.com)

5. [Complete GitHub Skills: Introduction to GitHub](https://github.com/skills/introduction-to-github)

---

<br>

## 00. Pre-Assessment [Start Here]

**Estimated Time:** 30 minutes

[Python Skills Self-Assessment](https://elearning.unidata.ucar.edu/metpy/PythonReadiness/selfassessment/)

This short assessment consists of 26 questions covering Python fundamentals, Jupyter notebooks, and common programming concepts.

The purpose is **not** to earn a high score.

Instead, think of it as a map. It can help identify areas where you already feel comfortable and areas where you may want a little extra practice before the bootcamp begins.

If you don’t know an answer, that’s perfectly okay. That’s what the bootcamp is for.

---

<br>

## 01. Python

**Estimated Time:** 1 hour

[futurecoder Interactive Python Tutorial](https://futurecoder.io/course/#toc)

Python is one of the most widely used programming languages in science, engineering, data analysis, machine learning, and high-performance computing. Many of the bootcamp projects use Python in some form, so becoming comfortable with the basics will make everything else feel much easier.

The FutureCoder lessons are interactive, browser-based, and beginner-friendly. They allow you to experiment with code directly in your web browser without installing anything.

If you get stuck, don’t worry. The built-in **Hints and Solutions** are there to help and are encouraged.

Start with: [Introducing The Shell](https://futurecoder.io/course/#IntroducingTheShell) 

From there, work through the lessons until you reach the end of the **For Loops** section.

You’re welcome to continue beyond that if you’re having fun, but completing through For Loops will provide a strong foundation for the bootcamp.

---

### Libraries and Packages

One of Python’s biggest strengths is its ecosystem of libraries and packages.

A **library** (sometimes called a package) is a collection of code written by other people that you can reuse in your own programs. Instead of solving every problem from scratch, you can import a library that already provides the functionality you need.

Different bootcamp projects use different libraries. You do **not** need to become an expert in any of them before arriving. We simply want you to recognize their names and have a general idea of what they do.

#### NumPy

**What is it?** NumPy is the foundation of scientific computing in Python. It provides fast numerical operations and efficient storage for large arrays and matrices of data.

If you’re working with scientific data, simulations, machine learning, or numerical calculations, chances are NumPy is somewhere under the hood.

**Think of it as:** Python’s high-performance calculator for large amounts of data.

**Optional Tutorials**

- https://numpy.org/doc/stable/user/absolute_beginners.html

#### Matplotlib

**What is it?** Matplotlib is one of the most popular plotting and visualization libraries in Python. It allows you to create graphs, charts, histograms, scatter plots, and many other visualizations.

**Think of it as:** Python’s graphing and chart-making toolkit.

**Optional Tutorials**

- https://matplotlib.org/stable/users/explain/quick_start.html

#### Pandas

**What is it?** Pandas is a library designed for working with structured data such as spreadsheets, CSV files, and tables.

It makes it easy to filter, organize, summarize, and analyze datasets.

**Think of it as:** Excel or Google Sheets, but programmable.

**Optional Tutorials**

- https://pandas.pydata.org/docs/user_guide/10min.html
- https://www.kaggle.com/learn/pandas

#### PyTorch

**What is it?** PyTorch is an open-source machine learning framework used for building and training neural networks.

Many modern artificial intelligence and deep learning applications use PyTorch, including some scientific computing and research workflows.

**Think of it as:** A toolkit for building and training AI models.

**Optional Tutorials**

- https://docs.pytorch.org/tutorials/beginner/basics/intro.html

#### TensorFlow

**What is it?** TensorFlow is another popular machine learning framework developed by Google. Like PyTorch, it is used for building and training neural networks and large-scale machine learning systems.

Different projects may use either TensorFlow or PyTorch depending on their needs.

**Think of it as:** Another toolbox for creating AI and machine learning applications.

**Optional Tutorials**

- https://www.tensorflow.org/tutorials/quickstart/beginner

#### Conda

**What is it?** Conda is a package and environment manager commonly used in scientific computing.

It helps you install software, manage dependencies, and keep different projects from interfering with one another.

For example, one project might need Python 3.10 while another needs Python 3.12. Conda helps both projects coexist peacefully on the same computer.

**Think of it as:** A tool that keeps your Python projects organized and prevents software conflicts.

**Optional Tutorials**

- https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html

#### Machine Learning (Optional)

Python is widely used in machine learning, artificial intelligence, and data science.

If you’re curious about how some of these libraries come together in practice, Kaggle provides an excellent beginner-friendly introduction.

**Optional Tutorial**

- https://www.kaggle.com/learn/intro-to-machine-learning

---

<br>

## 02. Jupyter Notebooks

**Estimated Time:** 30 minutes

Many bootcamp projects use **Jupyter Notebooks** as their primary interface.

A Jupyter Notebook combines:

- Code
- Text
- Images
- Charts
- Documentation

all in a single interactive document.

Think of it as a laboratory notebook for computing. Instead of writing notes on paper, you write notes, code, and results together in one place.

**What is the difference between Python and Jupyter?**

Python is a programming language.

Jupyter Notebook is a tool for writing and running Python code interactively.

Think of it like:

- Python = the language
- Jupyter = the notebook you write it in

The good news is that you do **not** need to know how to create a notebook from scratch. Most project leads will provide notebooks for you. Your goal is simply to become comfortable opening a notebook, running code, and making small changes.

---

### Open a Notebook

Visit:

https://jupyter.org/try-jupyter/notebooks/?path=notebooks/Intro.ipynb

This launches a Jupyter Notebook directly in your browser. No installation required.

### Five Things to Try

**1. Click on a Cell**

Notice that each block of text or code is contained inside a **cell**.

A cell is the basic building block of a notebook.

**2. Run a Cell**

Click inside a code cell and press:

`Shift + Enter`

This executes the code and moves to the next cell.

You will use this shortcut constantly during bootcamp.

**3. Change Something**

Find a code cell.

Modify a number or some text and run it again.

Notice how the output changes.

Congratulations—you just edited and executed code.

**4. Run Cells in Order**

Notebooks remember information from previous cells.

Try running a cell near the bottom of the notebook before running the cells above it.

Sometimes you'll get an error.

This happens because notebooks execute sequentially and later cells often depend on earlier cells.

When in doubt: **Run cells from top to bottom.**

**5. Restart the Kernel**

A **kernel** is the program that actually runs your code.

Think of it as the notebook's engine.

If something seems broken or out of sync, restarting the kernel often fixes the issue.

You don't need to fully understand kernels yet. Just know that every notebook has one.

---

### Important Jupyter Shortcuts

| Shortcut      | Action                   |
| ------------- | ------------------------ |
| Shift + Enter | Run current cell         |
| Enter         | Edit a cell              |
| Esc           | Exit editing mode        |
| A             | Create cell above        |
| B             | Create cell below        |
| M             | Convert cell to Markdown |
| Y             | Convert cell to Code     |

Don't worry about memorizing these. You'll pick them up naturally during bootcamp.

---

### Common Beginner Mistakes

**"Nothing happened."**

Make sure you actually ran the cell using `Shift + Enter`.

**"This worked earlier but now it doesn't."**

Try running the notebook from top to bottom again.

**"I got a NameError."**

A previous cell probably hasn't been run yet.

**"Everything is broken."**

Restart the kernel and run all cells again.

This fixes more problems than you'd think.

---

### Explore Further (Optional)

Google Colab is a browser-based notebook environment built on many of the same ideas as Jupyter.

If you'd like more examples, check out:

- Google Collab [Python Skills](https://colab.research.google.com/github/cs231n/cs231n.github.io/blob/master/python-colab.ipynb#scrollTo=7DmKVUFaL9gQ)
- Google Collab: [Numpy](https://colab.research.google.com/github/amanchadha/aman-ai/blob/master/numpy.ipynb#scrollTo=y1LvV56hB0PS)
- Google Collab: [Matplotlib](https://colab.research.google.com/github/amanchadha/aman-ai/blob/master/matplotlib.ipynb)
- Google Collab: [Pandas ](https://colab.research.google.com/drive/1a4sbKG7jOJGn4oeonQPA8XjJm7OYgcdX)
- Google Collab: [Tensorflow](https://colab.research.google.com/github/amanchadha/aman-ai/blob/master/tensorflow.ipynb)
- Google Collab: [Pytorch](https://colab.research.google.com/github/amanchadha/aman-ai/blob/master/pytorch.ipynb)

---

<br>

## 03. CLI / Shell

**Estimated Time:** 1 hour

[Terminal Tutor](https://www.terminaltutor.com)

The **Command Line Interface (CLI)**, often called the **shell** or **terminal**, is a text-based way of interacting with a computer.

Instead of clicking buttons and folders with a mouse, you type commands to navigate files, launch programs, move data, and connect to remote systems.

While that might sound old-fashioned, the command line remains one of the most powerful tools in computing and is the primary way many researchers interact with HPC systems.

If you’ve never used a terminal before, don’t worry. Nearly everyone arrives at the bootcamp with different levels of experience, and many participants are seeing the shell for the very first time.

Terminal Tutor is a fantastic interactive resource that runs entirely in your browser and teaches the fundamentals through hands-on practice.

Work through the lessons until you feel comfortable with:

- Viewing files and folders
- Navigating directories
- Creating folders
- Moving files
- Running simple commands

You do **not** need to memorize every command.

The goal is simply to become comfortable seeing a terminal window and typing commands into it.

---

### Common Commands You’ll See

You may encounter some of these commands during the bootcamp:

| **Command** | **What It Does**                  |
| ----------- | --------------------------------- |
| `pwd`       | Shows your current location       |
| `ls`        | Lists files and folders           |
| `cd`        | Changes directories               |
| `mkdir`     | Creates a new folder              |
| `cp`        | Copies files                      |
| `mv`        | Moves or renames files            |
| `rm`        | Deletes files                     |
| `cat`       | Displays a file’s contents        |
| `ssh`       | Connects to a remote system       |
| `history`   | Shows previously entered commands |

Don’t worry if these look unfamiliar right now. You’ll see them again throughout the bootcamp.

---

### A Quick Note About HPC

One of the first things you’ll do during the bootcamp is connect to a remote computing system.

Unlike a personal laptop, HPC systems are often accessed through a terminal session using a command called:

```bash
ssh
```

This may feel strange at first, but by the end of the week you’ll likely be navigating remote systems like you’ve been doing it for years.

---

### Common Beginner Mistakes

**“I typed a command and got an error.”**

This happens to everyone. Computers are very literal and even a small typo can change the meaning of a command.

**“I don’t know where I am.”**

Try:

```bash
pwd
```

This displays your current location.

**“I can’t find my files.”**

Try:

```bash
ls
```

This lists the files and folders in your current directory.

**“The terminal seems frozen.”**

Try pressing:

```text
Ctrl + C
```

This stops the currently running command and is one of the most useful keyboard shortcuts you’ll learn.

---

### Why Do People Love the Terminal?

At first, the command line can feel intimidating.

Then something interesting happens.

You realize you can accomplish complex tasks with just a few commands, automate repetitive work, connect to powerful remote systems, and move through files faster than you ever could with a mouse.

---

### Explore Further (Optional)

If you find yourself enjoying the shell, here are some excellent resources that go beyond the basics.

#### **OverTheWire: Bandit**

A capture-the-flag style game that teaches Linux and shell skills through progressively harder challenges.

https://overthewire.org/wargames/bandit/

#### **Software Carpentry: The Unix Shell**

A more traditional lesson that covers shell fundamentals used in scientific computing.

https://swcarpentry.github.io/shell-novice/

#### **MIT Missing Semester: The Shell**

A fantastic lecture series covering practical computing skills often missing from traditional coursework.

https://missing.csail.mit.edu/2020/course-shell/

---

<br>

## 04. Git & GitHub

**Estimated Time:** 30 minutes

[GitHub Skills: Introduction to GitHub](https://github.com/skills/introduction-to-github)

Most bootcamp projects will use **GitHub** to share code, notebooks, datasets, documentation, and project resources.

Before the bootcamp begins, we’d like you to become familiar with the basics of navigating GitHub and understanding how collaborative software projects are organized.

You’ll need to create a free GitHub account (or log into an existing one) before starting the lesson.

The GitHub Skills lessons are interactive, beginner-friendly, and feature a helpful sidekick that guides you through the exercises.

The lesson introduces several concepts you’ll encounter during the bootcamp:

- Repositories
- Branches
- Commits
- Pull Requests

Don’t worry if these terms feel unfamiliar at first. By the end of the tutorial, you’ll have seen each of them in action.

---

### Git vs. GitHub

These two terms are often used together, but they’re *not* the same thing.

**Git** is a version control system.

It keeps track of changes to files over time and allows multiple people to collaborate on the same project without constantly emailing files back and forth.

Fun fact, if you’ve ever named a file:

```text
Final.docx
Final_v2.docx
Final_v2_final.docx
Final_v2_REALLY_FINAL.docx
```

you’ve already experienced the problem Git was invented to solve.

**GitHub** is a website built around Git.

It provides a place to store repositories online, collaborate with teammates, track issues, review code, and manage projects. We're in a repo, right now!

You **don’t** need to understand every detail of Git before the bootcamp. We simply want you to recognize the tools and basic workflow.

---

### Explore Further (Optional)

If you’d like to learn more before the bootcamp, GitHub offers several additional interactive lessons.

- Introduction to Git: https://github.com/skills/introduction-to-git
- Review Pull Requests: https://github.com/skills/review-pull-requests
- Resolve Merge Conflicts: https://github.com/skills/resolve-merge-conflicts

---

<br>

## 05. Cheat Sheets

That's it! We hope this was as helpful and informative as it was to write. And remember: the goal was never to memorize everything.

Professional programmers, researchers, engineers, and scientists look things up constantly. One of the most valuable skills in computing is knowing where to find answers when you need them.

The resources below are handy references that you can bookmark and return to throughout the bootcamp whenever you need a quick refresher.

---

- [Python Cheat Sheet](https://realpython.com/cheatsheets/python/)

- [Advanced Python Cheat Sheet](https://ehmatthes.github.io/pcc_3e/cheat_sheets/)
- [Jupyter Cheat Sheet](https://www.dataquest.io/blog/jupyter-notebook-tips-tricks-shortcuts/)
- [Shell/Bash Cheat Sheet](https://docs.nesi.org.nz/Getting_Started/Cheat_Sheets/Bash-Reference_Sheet/)
- [Github Git Cheat Sheet](https://training.github.com/downloads/github-git-cheat-sheet.pdf)

---

<br>

**One Final Thought**

Nobody arrives at the Intro to HPC Bootcamp knowing everything.

The purpose of this Prep Pack was simply to introduce some of the tools and vocabulary you’ll encounter so that your week can focus on learning, collaborating, and exploring interesting problems rather than figuring out what a terminal window is.

Be curious.

Ask questions.

Experiment.

*Make mistakes.*

That’s how we all learn!
