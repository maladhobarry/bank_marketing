---
title: 1.2 - ML Workflow Use Cases
---
# Traditional ML applied to Bank Marketing Use Case

!!! abstract
    This project represents an initial solution of a bank marketing problem that you were assigned to.

    It is vital to understand that the modelling process here is not the crucial part. We will focus on _how_ the model is built and how we deal with all the engineering specifications.

    In other words, we take some executive decisions on how to do the modelling to go fast.



## Project Context

Your boss says to you:

!!! quote "Your boss assigning you a new project"
    Hey, good news! We've just signed a new contract with a bank's marketing team. They need us to optimize how their direct marketing people call people.
    They need us to generate a list of customers that are willing to respond favorably to their marketing campaign.
    **They have a SQL database containing the records of their customers, that you can access.**
    Obviously I recommended you to lead this project.

    You will be paired with Junior ML Engineer, who will also be able to assist you.
    He might ask some weird questions, but make sure you teach him what you know!

    Here's the list of things that I've been able to acquire, they mainly have to **predict who will respond positively to the marketing campaign**.

    I'll send you a more information on the data and everything.
    Once you have it, you should focus on building a good machine learning model


_After having received the data and accesses, you've been able to browse and look at the data dictionary. You've also taken the precaution of asking the client's representative how their data is logged so you can validate your data dictionary._

### Project summary
The project aims to improve effectiveness of marketing campaigns by **predicting the likelihood of customers to do a term deposit.** 
The marketing department has their own system (that feeds off ERP) displaying customers that have not been marketed to
that they use day-to-day to identify opportunities by manually looking at customer profiles.
By looking at the profiles, the marketing argents evaluate if the client would be a good candidate.
However, they would like to increase efficiency by predicting customers that are likely to respond positively to the marketing campaign.

### Available data and data dictionary
You've also looked quite intensely at the data and find out that with the current data you have.

**The data you've received from the client seems to be dataset that contains one row per client that was a target of a marketing campaign.**

From your discussion with the client, you know that data comes from multiple other **data sources that seem to have been joined together already**.

You can identify the following data domains:

1. Customer information: Identifiable information about customers
    - age
    - job
    - marital
    - education
    - default
    - housing
    - loan
1. Marketing: details of previous marketing campaign results per user
    - contact / comm_type
    - month / comm_month
    - day_of_week / comm_day
    - duration / comm_duration
    - campaign / curr_n_contact
    - pdays / days_since_last_campaign
    - previous / last_n_contact
    - poutcome / last_outcome
1. Socio economical data
    - emp.var.rate
    - cons.price.idx
    - cons.conf.idx
    - euribor3m

We'll see those data more in detail in the notebook.
We will now see how we can solve the bank marketing use case by using our trusty ML tools.

!!! quote "You come back from vacation"
    Your colleague says he has completed the project!
    Indeed, he published a notebook that he wants you to look.

    _Note: This is a pretext so we don't have to actually implement the whole data science process in this lab by ourselves._


!!! example "How to read this guide and notebooks (ex: `02_EDA_tm.ipynb`)"

    You will need to follow this document _and_ the jupyter notebook in parallel.

    **In this guide, we will tell you what cells to execute in each section. In the notebook, we will tell you to go back in this document.**

    In this document, we will provide some retrospective while in the jupyter notebook we are focused on making the application work.

    _For simplicity of this lab, this notebook executes somewhat sequentially, **however this is not the case in most notebooks, so we are dealing with a not so bad notebook.**_


## Technologies used and your environment


### Creating your environment
==**Task: Create the project environment.**==

You can use whichever environment manager you want to start, either anaconda's `conda` or Python's `venv`.
In any case, we recommend your Python version to be `3.10`.

```bash
# You can pass `--prompt` to have a good name
$ python -m venv .venv --prompt ivamlops-11

# Activate your venv
$ source .venv/bin/activate
# Or on Windows:
# $ . .venv/Scripts/Activate.ps1
```
_Note: after this lab, we'll scratch the environment, so the name does not really matter._

Now install and run Jupyter Lab:

```bash
pip install jupyterlab
jupyter lab
```
## Download the assets

==**Task: Download the starting database checkpoint and put it in your directory.**==

**You will need to:**

- Download the [`start.db`](https://drive.google.com/file/d/13YJbLWhvVPErqIZ-03jlGsQUjETCkKHj/view?usp=sharing) and place it in `./data/bank/start.db`


## Run the Data Extraction

==**Task: Get the CSV files for EDA by running the Data Extraction nobteook.**==

**You will need to:**

- Navigate to the URL returned by Jupyter
- Open `01_DataExtraction.ipynb` notebook.
- Run all cells of the notebook

This will give you the necessary files to run the lab.

Now open `02_EDA_tm.ipynb`, the notebook where the magic will happen.

## Exploring the "EDA" implementation
!!! note "ML process in `02_EDA_tm.ipynb`"

    Although some data scientist might not be familiar with all the technologies here, this is a fairly standard notebook with "correctly" implemented pipelines.

    _Disclaimer: I am not a data scientist anymore, but what I will present in this notebook is somewhat representative of what most data science notebooks are._


### Dependencies
==**Run cells section: `START: Dependencies`.**==

What is the first problem you encounter?

Notice that there was no `requirements.txt` generated with this repository... So who knows what requirements you have now...

!!! question "What do you think could go wrong with this approach"


### Exploratory Data Analysis - reading and graphing
Objectives:

- ==**Run cells section: `START: EDA`. This is a lengthy section.**==
- ==**Fix the code so that it works for you.**==

!!! question "What issue did we encounter? Any way of fixing it so it doesn't happen when our boss tries to run the notebook?"

!!! success "Data leakage: Good catch"
    Your colleague has spotted a wild Data Leakage with the variable `duration`.


### Encountering the modelling in EDA notebook
Objectives:

- ==**Run cells section: `START: First Model, in EDA 🤔?`.**==
- ==**Fix the code so that it works for you.**==

??? question "What about this commented code? Is it useful?"
    Should I be concerned ?

??? question "How do you like them variables? (names)"
    You start questionning your choices of reading this code...


### Going with it: iterations 2 to 5
Objectives:

- ==**Run cells section: `START: Iterative improvements™️`.**==
- ==**Fix the code so that it works for you.**==

!!! question "There's so many iterations... How do I know I'm not using a variable from previous iterations?"

??? question "Did we use the same methodology for all our iterations?"
    What if we had to change something in the middle of our iterations?
    Would we know what iterations are impacted and which to re run?

!!! question "So what was the winning model in the end?"


!!! warning "We are in a happy path"
    Note that in a lot of cases, we would have **lost** the code and models for iterations 2 through 4 ; people usually overwrite their previous non working model with the more updated versions.

    This leads to reproducibility problems and most of all tracking problems...


## Exploring the real modelling notebook

Even though there is some modelling work done in the EDA, there seems to be a dedicated notebook `03_BestModelTrainEval.ipynb` that contains the training procedure for the model. Once again, you have to step through the notebook to understand and verify the work.


### Starting with our model from iteration 5
Objectives:

- ==**Run cells section: `START:  Training a Boosting Classifier with clustering (iteration 5)`.**==
- ==**Fix the code so that it works for you.**==

Start running the code and you'll encounter something that you are not happy about:

!!! bug "NameError: name 'transformerNumerical' is not defined"

In order to fix this bug, you'll need to change the `Pipeline` to use the correct value so the code works.

The correct name of the variable should have been `transformerNumerical5` instead. You'll probably have to update `transformerCategorical` too if you don't want another error...

!!! question "What does this mean for our previous 'best' model? "


??? failure "Did you spot the wrong dataset?"
    Note that the dataframe path we read from is different than what was originally provided. In _our_ case it doesn't change much since we have probably fixed the dataset to the same value.

    However, for your colleague, this means he might have trained using a _different_ file that existed (after all there were no jupyter errors in the cell outputs...)

    What does this mean for our EDA modelling?

### Continuing our iteration 5 after the bug is fixed
Objectives:

- ==**Run cells section: `START: Continuing our iteration 5 after the bug is fixed`.**==
- ==**Fix the code so that it works for you.**==

Do we have the same performance as we had in iteration 5? What could be the cause of this, you wonder...



### Cross validation and a new package
Objectives:

- ==**Run cells section: `START: Attempting Cross Validation and something else?`.**==
- ==**Fix the code so that it works for you.**==

_Note: The `RandomizedSearchCV` might take some time, but it's around 1 minute on a reasonable laptop CPU._

You see there is a new library being installed, that boasts to improve `scikit-learn`'s performance by a lot. Although it's installed mid notebook, you find the finding good.

Maybe next time the dependency management could be a bit better... You do wonder however:

??? question "Does the new library have side effects?"
    A fair question to ask when you add a new package in your codebase. Unfortunately, you don't have much to protect yourself against those.



### _XGBoost has entered the chat_
Objectives:

- ==**Run cells section: `START: XGBoost has entered the chat`.**==
- ==**Fix the code so that it works for you.**==

You might be missing some code. This is because you colleague has run their notebook out of order.
You needed to change a few things anyway

```python
transformer5 = ColumnTransformer([
    ('cluster_customer', kmeans_pipeline, person_info_cols_cat + person_info_cols_num),
    ('num', transformerNumerical5, num_cols_wo_customer),
    ('cat',  transformerCategorical5, cat_cols_wo_customer),
])
transformer5.fit(train_x)
```


Even with this change, you might still get some other (cryptic) errors. Why did it work for your colleague and not you? He probably did ++ctrl+z++ (Undo) without knowing having realized after...

In any case, you can proceed to correct the error by adding the correct training parameter

```python
param['tree_method'] = 'gpu_hist'
param['sampling_method'] = 'gradient_based'
# Or if you can't train with GPU:
param['tree_method'] = 'hist'
param['sampling_method'] = 'uniform'
```

Don't worry if the `accuracy_score` doesn't work too well, it's not an adequate metric for us anyway.

Then you can proceed to continue on with the feature importance graphs.

??? question "How well does xgboost performance wise?"

You also start to wonder if `pickle` is the best way to save an xgboost model: from what you remember reading there was a more robust way.

**In any case, now you have a few models saved in your local directory. Surely, you can put them to good use in a prediction task, let's switch to `04_DoPredictionForBoss.ipynb`.**

You've decided that although there are questionnable decisions in the codebase, the model is reasonably OK. You tell your boss you're satisfied with the work.

Satisfied, he says he will have some updates for you soon.

## Exploring the inference process
Objectives:

- ==**Run cells section: `START: Inference`.**==
- ==**Implement the missing scoring routine.**==

A month has passed and your boss gives you a new dataset and wants you to **score your predictions on this new dataset** so that the customer get a better sense of their options.

**You will need to:**

- Use the `y` value of the file `data/bank_marketing_2010-08-01_to_2010-09-30.csv` to get the AUC using `RocCurveDisplay`


After having seen the flow, you think to yourself.
> This isn't that bad, but I wonder how we will evolve from this...
> How to deal with all the possible improvement paths?

Notably you start asking yourself the impact on your workflow that all these additional (non-exhaustive) possibilities:

1. You might want to add additional economic metrics
2. Change the feature selection logic
3. You might want to train using a different split
4. You might want to set the values for the `OneHotEncoder` so it's prepopulated

## Feedback

After having done the scoring of your model with the newly provided data, your boss is pleased with your model. After verifying with the clients, he tells your colleague and you:

!!! quote "Future steps of the project"
    Good job out there, our clients were very pleased with your results.

    I have additional news for you: we've been selected to do a part 2 of this project! We'll have to integrate with their system more tightly. We will be feeding marketing agents _directly_ ; I've also identified a new way we could improve our solution.

    He proceeds to tell you all about the project...

After hearing the requirements, you know fully well that accomplishing the second phase will prove more difficult.

**In the light of these new requirements and your tuned MLOps reflexes, you tell your boss that you will need to make some adjustements to your project so that it can unlock the full expected value of AI, good engineering while delivering good business value.**

### Next steps

Keep in mind that for the next labs:

- The column names will change to be more representative

In the meantime you need to do a task you had promised your boss:

### Give feedback to your colleague about the work flow
Objectives:

- ==**Enumerate the pain points of this approach.**==
- ==**Explain the sources of potential error.**==
- ==**Address the reproducibility aspect.**==

Don't forget that at the beginning of the project, you were tasked to help your fellow colleague improve on the ML Ops engineering part of the work.

You first decide to employ the Socratic method:

Think of questions you would like to ask your colleague, in order to develop a better model and make sure you can maintain it.


!!! note "Colleague interactions"
    Some of our colleague comment's were a bit absurd some times. Generally, colleagues will not be like this: but everyone (even us) _can end up like this if we are not careful_. We need to stay alert and take educated decisions, even in the face of uncertainty.

    Clean code principles will allow us to better our practices so we can avoid such destructive patterns.

