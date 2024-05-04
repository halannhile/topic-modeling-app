# topic-modeling-app
COSI-217B Final Project

## Running the app
1. Setup virutal environment
```
conda create -n topic-modeling-app python=3.12
conda activate topic-modeling-app
python -m pip install -r requirements.txt
```
2. Run the streamlit app
```
python -m streamlit run 1_Your_Documents.py
```
3. Build and run Docker
```
docker build -t your-app-name .
```
```
 docker run -p 8501:8501 your-app-name
```
Navigate to http://localhost:8501 to access app.

4. Run unit tests
```
python -m unittest discover -s unit_tests
```