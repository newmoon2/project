from flask import Flask, request, jsonify
import threading
import streamlit as st


import config as config
from server.models import ollama
from server.models.llm_api import create_openai_llm, check_openai_llm
from server.models.ollama import create_ollama_llm
from server.models.embedding import create_embedding_model
from server.index import IndexManager
from server.stores.config_store import CONFIG_STORE
from frontend.state import init_state
from server.engine import create_query_engine


app = Flask(__name__)

# API Endpoint
@app.route('/api', methods=['GET', 'POST'])
def api():
    #data = request.get_json()
    #content = data.get('content', '')
    prompt = 'nltk란?'

    query_response = st.session_state.query_engine.query(prompt)
    print(query_response)
    # 여기에 요청 처리 로직을 추가 (예: 문서 처리)
    return []
    #return jsonify({"response": f"Received: {content}"})


def init() :
    a = 1

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
    app.run(host='0.0.0.0', port=5000)
else    :
    init_state()
    init()
    app.run(host='0.0.0.0', port=5000)

# 별도로 Flask 서버를 실행하는 함수
#def start_flask_thread():
#    flask_thread = threading.Thread(target=run_flask)
#    flask_thread.daemon = True
#    flask_thread.start()
