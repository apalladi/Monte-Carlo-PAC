# Monte-Carlo PAC, Capital Accumulation Plan

## Introduction
This repository provides a tool to simulate investments of varying durations across different types of assets using **Monte Carlo simulations**. The assets can include **stocks, ETFs, bond ETFs**, or **market indices** such as the **S&P 500**. The simulation specifically refers to a **monthly investment of a fixed amount of money** rather than a one-time investment. It strictly analyzes past data to produce a distribution of returns based on historical performance, without any predictive power regarding future outcomes.

The goal is to obtain the return distribution for different investment durations, allowing users to assess the likelihood of achieving positive returns, both in nominal terms and in real terms (adjusted for inflation). This method can help investors gain insights into how various assets have performed historically over time, but it should not be interpreted as a tool for forecasting future performance.

## 1. Cloning the repository
To get started, clone the repository from GitHub:
```
git clone git@github.com:apalladi/Monte-Carlo-PAC.git
```

Then, navigate into the project directory:
```
cd Monte-Carlo-PAC
```

## 2. Installing and Activating the Environment
To set up the Conda environment with all required dependencies, follow these steps:

1. Make sure you have Conda installed on your system.

2. Create the environment using the provided `environment.yml` file:
```
conda env create -f environment.yml
```

3. Once the environment is created, activate it with:
```
conda activate pac-monte-carlo
```

Now you are ready to start working with the project and run simulations!
