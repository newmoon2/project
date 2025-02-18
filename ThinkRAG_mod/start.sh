!/bin/bash

cd /home/
git clone https://github.com/newmoon2/project.git
echo "git clone completed.."
cd /home/project/ThinkRAG_mod
pip3 install -r requirements.txt
echo "dependency install completed.."
streamlit run app.py
