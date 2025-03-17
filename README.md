# Setup Instructions

## Create a Virtual Environment
```python3 -m venv langchain-env```

## Activate the Environment
```source langchain-env/bin/activate```

## Install LangChain
```pip install langchain```

## Create a Requirements Text File
requirements.txt
```bash
langchain-Ollama
streamlit
langchain-experimental
```

## Install Requirements
```pip install -r requirements.txt```

## Pull the Model Locally
```ollama pull llama3.1```


> ```python3 -m venv langchain-env```
> 
> ```source langchain-env/bin/activate```
> 
> Create a `requirements.txt` file:
> ```
> langchain
> langchain-ollama
> streamlit
> ```
> 
> ```pip install -r requirements.txt```
> 
> ```ollama pull llama3.1```
> 
> ```streamlit run file.py```

