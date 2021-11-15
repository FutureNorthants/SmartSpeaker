# A simple smart speaker 
The aim of this project is to showcase innovation by building a smart speaker that can connect to Norbert's Microsft QnA service to answer questions.

## Prerequisites
- Python 3.* installed
- Python virtual environments able to be created
- flac install (on mac with brew run ```brew install flac``` in ubuntu run ```sudo apt install flac```)

Add a credentials.py file with the following format:

```python
class credentials():
    def __init__(self):
        self.QnA_DOMAIN=""
        self.QnA_AUTH=""
        self.QnA_COOKIE=""
        self.QnA_ENDPOINT=""
        self.QnA_CONFIDENCE=60
```
## Setup

Navigate to the folder
connect to the virtual environment (on a mac run ```source virtenv/bin/activate```, in vscode select python next to the git branch and select the recommended option)
install the dependancies by running ```pip3 install -r requirements.txt```


## Run
ensure you are in the virtual environment
run ```python3 app.py```