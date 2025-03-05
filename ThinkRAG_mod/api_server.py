import datetime
from flask import Flask, request, jsonify, session, Response
import streamlit as st
import time
import pandas as pd
import config as config
from server.index import IndexManager
from server.stores.config_store import CONFIG_STORE
from frontend.state import init_state
from server.engine import create_query_engine
from flask_cors import CORS  # 추가
import json

app = Flask(__name__)
CORS(app)

def yield_message(data):
    prompt = data.get("prompt")
    start_time = time.time()
    response = st.session_state.query_engine.query(prompt)
    for chunk in response.response_gen :
        print(chunk)

        row = {
            "dateTime": datetime.now().isoformat(),
            "role": "assistant",
            "content": chunk,
            "segment": "text",
            "docsInfo": []
        }

        stream = json.dumps(row)
        yield  stream + "\n"

    row = {
        "dateTime": datetime.now().isoformat(),
        "role": "assistant",
        "content": '',
        "segment": "stop",
        "docsInfo": []
    }
    stream = json.dumps(row)
    yield stream + "\n"

# API Endpoint
@app.route('/api/chat/completion', methods=[  'POST', 'GET'])
def api():
    data = request.get_json()
    resp = Response(yield_message(data), content_type="text/event-stream")
    return resp

def init() :

    current_llm_info = CONFIG_STORE.get(key="current_llm_info")
    current_llm_settings = CONFIG_STORE.get(key="current_llm_settings")

    st.session_state.index_manager = IndexManager(config.DEFAULT_INDEX_NAME)

    if st.session_state.index_manager.check_index_exists():
        st.session_state.index_manager.load_index()
        st.session_state.query_engine = create_query_engine(
            index=st.session_state.index_manager.index,
            use_reranker=current_llm_settings["use_reranker"],
            response_mode=current_llm_settings["response_mode"],
            top_k=current_llm_settings["top_k"],
            top_n=current_llm_settings["top_n"],
            reranker=current_llm_settings["reranker_model"])
        print("Index loaded and query engine created")

if __name__ == '__main__':
    init_state()
    init()
    app.run(host='0.0.0.0', port=5000, debug=True)
