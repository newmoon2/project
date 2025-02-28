from flask import Flask, request, jsonify
import streamlit as st

import config as config
from server.models.ollama import create_ollama_llm
from server.models.embedding import create_embedding_model
from server.index import IndexManager
from server.stores.config_store import CONFIG_STORE
from frontend.state import init_state
from server.engine import create_query_engine

app = Flask(__name__)

@app.route('/api', methods=['GET', 'POST'])
def api():
    try:
        data = request.get_json()
        prompt = data.get('content', 'nltk란?')  # 기본 질문 설정

        if 'query_engine' not in st.session_state:
            return jsonify({"error": "Query engine not initialized"}), 500

        query_response = st.session_state.query_engine.query(prompt)
        return jsonify({"response": query_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def init():
    try:
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
                reranker=current_llm_settings["reranker_model"]
            )
            print("Index loaded and query engine created")
    except Exception as e:
        print(f"Initialization failed: {str(e)}")


if __name__ == '__main__':
    init_state()
    init()
    print('server 실행 ->')
    app.run(host='192.168.1.111', port=5000)
