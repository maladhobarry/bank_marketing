# Build an ML-Powered Bank Marketing Solution

This project represents a bank marketing solution that streamlines prospect management and enhances the effectiveness of marketing campaigns. The marketing team have developed a frontend web application that serves as a dynamic interface to display the profiles of the prospects to call daily by each consultant as part of the current marketing campaign mission. The primary goal is to allow the consultants analyzing the profiles first, thus, they can efficiently identify and engage with potential clients who are most likely to be interested in our current marketing campaign.

**Challenges and Objectives:**

- **Consultant Overload**: Our consultants deal with a high volume of prospect profiles daily, making it challenging to analyze each one thoroughly.

- **Smarter Decision-Making**: We aim to provide our consultants with a ML-powered web application that enables smarter decision-making by predicting the likelihood of a client's interest in the current campaign.

- **Automation Modes**: The solution consists of two modes:
  - **Partial Automation**: Consultants will use model predictions alongside prospect profiles to make informed decisions.
  - **Full Automation**: Consultants will rely entirely on the ML model's predictions to select prospects for outreach.

**Key Benefits:**

- **Efficiency**: By automating the prospect selection process, we optimize the use of consultants' time and resources.

- **Enhanced Decision-Making**: Our ML model's predictions enable more targeted and personalized marketing outreach, leading to higher conversion rates.

**Future Enhancements:**

Throughout the MLOps upskilling program, we are committed to continuous improvement and plan to enhance the solution by maturing its MLOps level by building an end-to-end automated pipeline that operates on a regular cadence to retrain the model using new data, ensuring that it remains accurate and up-to-date. Afterward, we will setup a CI/CD environment to streamline all the quality assurance and deployment processes follow-up any data engineering or machine leaning code changes in the future.

## Starter Kit & Set Up

### Fork the project
Go to the Project Repository: [ml-powered-bank-marketing-solution](https://github.com/iva-mlops-program/ml-powered-bank-marketing-solution.git) and click on Fork in the upper right corner. This will create a fork in your Github account, i.e., a copy of the repository that is under your control. Now clone the repository locally so you can start working on it:
```
git clone https://github.com/[your github username]/ml-powered-bank-marketing-solution.git
```
### Create environment
We recommend [anaconda platform](https://www.anaconda.com/download), otherwise you can use Python virtualenv. If you have conda installed and ready, you can follow the below instructions to create a new environment and start working. 
```bash
> conda env create --name ml_bank_dev
> conda activate ml_bank_dev
```
When you are done working on the project, you can deactivate the environment:
```bash
> conda deactivate
```
### Install Dependencies
```bash
> cd ml-powered-bank-marketing-solution
> pip install -e .[all]
```
The `-e` option allows you to dynamically load the latest code changes without the need for reinstallation.

## Components

### Front-End Web Application
Our Front-End web application, which consumes the Flask Rest API server, provides a user-friendly interface for managing prospects selected for the current marketing campaign. The interactions with clients are simulated using ground-truth data. 

Indeed, Users initiate by selecting a past date as virtual today, then, choosing from three AI assistance modes: *without*, *partial*, or *full*. 
In the *without* mode, selected customer profiles are displayed, requiring employees, assumed to be experienced with sales objectives, to make manual decisions. In *partial* mode, AI insights accompany profiles to aid employee decision-making. *Full* mode exclusively showcases prospects validated by AI as high-potential successful calls. 

Once the employee selects a prospect and presses on CALL, the web application simulates the call and displays the call duration and the outcome.

**_NOTE_**: All code necessary for this functionality is fully provided in the starter kit, requiring no further development at this stage.

### REST API Server

Within our system, we've implemented a Flask-based REST API Server. This server serves as the gateway for accessing a trained machine learning model via the HTTP protocol. It offers extensive functionality, accommodating prediction requests for individual prospects as well as bulk prospect datasets. 

**_NOTE_**: All code necessary for this functionality is fully provided in the starter kit, requiring only the update of the [environment variables](server_app/.env) pointing to the feature engineering pipeline and the trained model, once they are built and saved, properly.

### Bank Marketing Library and ML Engineering Notebooks

The goal is to apply software engineering principles on the bank marketing model engineering code built in the previous lab to put them in production. We have already provided you the `EDA_tm.ipynb` file containing the solution to perform basic EDA on Bank datasets and build some baseline models for campaign outcome prediction, but without implementing the engineering and software best practices.

#### Code Refactoring

You need to refactor the given `EDA_tm.ipynb` file following the best coding practices to complete these files:

1. `notebooks/EDA.ipynb` 
2. `notebooks/Modeling.ipynb`

These three (incomplete) files are already created for you. They contain all the instructions for the missing development in the (incomplete) Bank Marketing Library, `src\bank_marketing`, that you should implement as you progress in the lab. In addition, for a better understanding of the requirements, you will find explicit instructions as comments or the function to implement calls.

In `src\bank_marketing`, you will notice all functions have been provided with document strings. These functions have been set up to guide you to a solution. In `notebooks/Modeling.ipynb`, Iteration 3 stands as an exception. In this iteration, it's expected that you consolidate all the concepts and knowledge acquired thus far. Your task will be to create new classes and functions from scratch, demonstrating your ability to refactor another portion of the code provided in the workshop notebook: `EDA_tm.ipynb`. This marks a pivotal stage where you apply your accumulated skills to optimize and enhance the existing codebase.

#### Code Quality Considerations: Testing and Logging

Unit tests play a crucial role in ensuring the reliability and robustness of our codebase. Ideally, each function should have its associated unit tests to validate its functionality comprehensively. However, for the sake of simplicity and time efficiency during this lab, we are introducing a focused approach. We kindly request that you prioritize completing the unit test suite for the `prepare_binary_classfication_tabular_data` function from the module `bank_marketing.data.prep_datasets`. This specific function holds a critical role in our modeling process, as any failures or issues within it may lead to silent failures and severe implications on the overall modeling process and final model performance. 

The pytest module `tests/test_data/test_prep_datasets.py` should:  
 - Contain unit tests for the `prepare_binary_classfication_tabular_data` functions. You have to write test for *each* requirement. Follow the provided example and the short description below each unit test, and use basic assert statements. 
 
 - Log any ERROR and INFO messages. You should log the info messages and errors in a .log file, so it can be viewed post the run of the script. The log messages should easily be understood and traceable.

 Also, ensure that testing and logging can be completed on the command line, meaning, running the below command in the terminal should test each of the functions and provide any errors to a file stored in the *./logs* folder.
```bash
> pytest . -vv --db /path/to/bank.db --sed /path/to/socio_economic_indices_data.csv
```

#### Code Styling Considerations

- **Style Guide** - Format your refactored code using [PEP 8 – Style Guide](https://peps.python.org/pep-0008/). 

- **Style Checking and Error Spotting** - Use [Pylint](https://pypi.org/project/pylint/) for the code analysis looking for programming errors, and scope for further refactoring. 