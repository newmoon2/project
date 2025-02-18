!/bin/bash

cd /home/project/ThinkRAG_mod

pip3 install -r requirements.txt
echo "dependency install completed.."
streamlit run app.py