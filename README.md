
# Evaluating Machine Learning Models for Modelling Piezo Dynamics
**Authors** David Kleindiek

**Date** 20.08.2024

GitHub repository for the research project during the summer term 2024 at the Eberhard-Karls Universität Tübingen.

The project report is available [here](doc/Evaluating_Machine_Learning_Models_for_Modelling_Piezo_Dynamics.pdf). The project presentation can be accessed [here](doc/Preseantation.pdf)

## Overview
This repository contains the research work conducted to develop and evaluate machine learning models to predict the behaviour of piezo actuators. The aim of this project is to evaluate how machine learning models can bne used to predict piezo creep and hysteresis.

## Objectives
 - Record piezo input voltage and displacement to create a comprehensive dataset.
 - Generate features off of the recorded data to better capture the effects that creep and hysteresis depend on.
 - Train machine learning models on the prepared data and evaluate their performance.

## Repository Structure

The repository is organized into several directories:

 - [`src/`](src): Contains Python notebooks for controling the devices, data recording and quantification of system dynamics.
 - [`exp/`](exp): Contains Python notebooks for feature generation, model training, model evaluation and the trained model files.
 - [`dat/`](dat): Contains raw and processed data used in the project, including recordings of piezo displacement behaviour, sensor noise quantification and model predictions.
 - [`doc/`](doc): Documentation, including the project report, presentation and any additional figures.

### Running the code
1. Clone the repository:
```bash
git clone https://github.com/stedavkle/uni-tuebingen-piezo-ml.git
cd uni-tuebingen-piezo-ml
```
2. Set Up a Virtual Environment (Optional but Recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install Required Packages:
```bash
pip install -r requirements.txt
```
4. Run The Notebooks:
```bash
jupyter notebook
```
