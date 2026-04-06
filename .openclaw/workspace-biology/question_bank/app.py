"""
app.py - Streamlit 试题库主应用
"""

import streamlit as st
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import database
import vector_store
import importer
import exporter

st.set_page_config(
    page_title="高中生物试题库",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: bold; color: #2E7D32; text-align: center; padding: 1rem; }
    .question-card { background-color: #f8f9fa; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; border-left: 4px solid #2E7D32; }
    .stats-card { background-color: #E8F5E9; border-radius: 10px; padding: 1.5rem; text-align: center; }
    .stButton>button { width: 100%; }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    if "selected_questions" not in st.session_state:
        st.session_state.selected_questions = []
    if "search_done" not in st.session_state:
        st.session_state.search_done = False


init_session_state()


def get_difficulty_stars(difficulty: int) -> str:
    stars = "★" * difficulty + "☆" * (5 - difficulty)
    color = {1: "green", 2: "lightgreen", 3: "yellow", 4: "orange", 5: "red"}.get(difficulty, "gray")
    return stars


def display_question_row(question: dict):
    difficulty = question.get("difficulty", 3)
    stars = get_difficulty_stars(difficulty)
    
    with st.container():
        cols = st.columns([0.05, 0.05, 0.4, 0.1, 0.1, 0.1, 0.2])
        
        # 选择框
        with cols[0]:
            is_selected = question["id"] in st.session_state.selected_questions
            selected = st.checkbox("", key=f"q_{question['id']}", value=is_selected)
            if selected:
                if question["id"] not in st.session_state.selected_questions:
                    st.session_state.selected_questions.append(question["id"])
            else:
                if question["id"] in st.session_state.selected_questions:
                    st.session_state.selected_questions.remove(question["id"])
        
        # 序号
        with cols[1]:
            st.markdown(f"**{question['id']}**")
        
        # 题干
        with cols[2]:
            title = question.get("title", "")[:100] + ("..." if len(question.get("title", "")) > 100 else "")
            st.markdown(f"📝 {title}")
        
        # 难度
        with cols[3]:
            st.markdown(f"⭐{stars}")
        
        # 题型
        with cols[4]:
            st.caption(question.get("question_type", "选择题"))
        
        # 知识点
        with cols[5]:
            kp = question.get("knowledge_point", "")
            if kp:
                st.caption(kp[:8] + "..." if len(kp) > 8 else kp)
        
        # 来源
        with cols[6]:
            src = question.get("source", "")
            if src:
                st.caption(src[:10] + "..." if len(src) > 10 else src)


def main():
    st.markdown('<h1 class="main-header">📚 高中生物试题库</h1>', unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.title("功能菜单")
        
        menu = st.radio(
            "选择功能",
            ["📖 题库浏览", "🔍 题目搜索", "📥 导入题目", "📤 导出试卷", "📊 数据统计"],
            index=0
        )
        
        st.divider()
        
        # 统计信息
        stats = database.get_statistics()
        st.markdown("### 📈 题库统计")
        st.markdown(f"""
        <div class="stats-card">
            <h2>{stats['total']}</h2>
            <p>总题目数</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        - 📚 知识点数：{stats['knowledge_point_count']}
        - 📑 来源数：{stats['source_count']}
        """)
        
        if st.session_state.selected_questions:
            st.divider()
            st.markdown(f"**已选题目：{len(st.session_state.selected_questions)} 道**")
            if st.button("🗑️ 清空已选"):
                st.session_state.selected_questions = []
                st.rerun()
    
    # ===== 题库浏览 =====
    if menu == "📖 题库浏览":
        st.header("📖 题库浏览")
        
        # 筛选条件
        with st.expander("🔍 筛选条件", expanded=True):
            cols = st.columns(4)
            with cols[0]:
                difficulty_filter = st.selectbox("难度", ["全部", "1", "2", "3", "4", "5"])
            with cols[1]:
                kp_options = ["全部"] + database.get_all_knowledge_points()
                kp_filter = st.selectbox("知识点", kp_options)
            with cols[2]:
                source_options = ["全部"] + database.get_all_sources()
                source_filter = st.selectbox("来源", source_options)
            with cols[3]:
                type_options = ["全部"] + database.get_all_question_types()
                type_filter = st.selectbox("题型", type_options)
        
        # 构建筛选参数
        filters = {}
        if difficulty_filter != "全部":
            filters["difficulty"] = int(difficulty_filter)
        if kp_filter != "全部":
            filters["knowledge_point"] = kp_filter
        if source_filter != "全部":
            filters["source"] = source_filter
        if type_filter != "全部":
            filters["question_type"] = type_filter
        
        # 获取题目
        questions = database.search_questions(**filters)
        
        st.markdown(f"**共找到 {len(questions)} 道题目**")
        
        # 分页
        page_size = 20
        total_pages = max(1, (len(questions) + page_size - 1) // page_size)
        page = st.number_input("页码", min_value=1, max_value=total_pages, value=1)
        
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_questions = questions[start_idx:end_idx]
        
        for q in page_questions:
            display_question_row(q)
        
        if not questions:
            st.info("题库为空，请先导入题目！")
    
    # ===== 题目搜索 =====
    elif menu == "🔍 题目搜索":
        st.header("🔍 题目搜索")
        
        # 搜索方式选择
        search_mode = st.radio("搜索方式", ["语义搜索（AI）", "关键词搜索"], horizontal=True)
        
        if search_mode == "语义搜索（AI）":
            st.info("💡 使用AI理解语义，找到与查询内容相关的题目")
            query = st.text_input("输入搜索内容（可以用自然语言描述题目特征）", placeholder="例如：关于细胞呼吸的综合题")
            
            if query:
                with st.spinner("正在搜索..."):
                    results = vector_store.search_similar(query, top_k=10)
                
                if results:
                    st.success(f"找到 {len(results)} 道相关题目")
                    
                    # 筛选条件
                    with st.expander("附加筛选"):
                        s_cols = st.columns(3)
                        with s_cols[0]:
                            s_diff = st.selectbox("难度", ["全部", "1", "2", "3", "4", "5"], key="s_diff")
                        with s_cols[1]:
                            s_type = st.selectbox("题型", ["全部"] + database.get_all_question_types(), key="s_type")
                        with s_cols[2]:
                            s_kp = st.selectbox("知识点", ["全部"] + database.get_all_knowledge_points(), key="s_kp")
                    
                    for r in results:
                        q = database.get_question_by_id(r["question_id"])
                        if q:
                            # 应用附加筛选
                            if s_diff != "全部" and q.get("difficulty") != int(s_diff):
                                continue
                            if s_type != "全部" and q.get("question_type") != s_type:
                                continue
                            if s_kp != "全部" and s_kp not in (q.get("knowledge_point") or ""):
                                continue
                            
                            display_question_row(q)
                else:
                    st.warning("未找到相关题目，试试其他关键词？")
        else:
            # 关键词搜索
            kw_col1, kw_col2 = st.columns(2)
            with kw_col1:
                keyword = st.text_input("关键词", placeholder="搜索题目、知识点、关键词...")
            with kw_col2:
                kw_difficulty = st.selectbox("难度", ["全部", "1", "2", "3", "4", "5"], key="kw_diff")
            
            if keyword or kw_difficulty != "全部":
                filters = {"keyword": keyword} if keyword else {}
                if kw_difficulty != "全部":
                    filters["difficulty"] = int(kw_difficulty)
                
                results = database.search_questions(**filters)
                st.success(f"找到 {len(results)} 道题目")
                
                for q in results:
                    display_question_row(q)
    
    # ===== 导入题目 =====
    elif menu == "📥 导入题目":
        st.header("📥 导入题目")
        
        st.markdown("""
        ### 支持的文件格式
        - **Excel文件** (.xlsx, .xls)：需包含表头行
        - **Word文档** (.docx)：自动识别题目格式
        - **JSON文件** (.json)：标准JSON数组格式
        """)
        
        st.markdown("### 📋 Excel格式要求")
        st.markdown("""
        | 列 | 内容 | 说明 |
        |---|---|---|
        | A | 题干 | 必填 |
        | B | 答案 | 选填 |
        | C | 难度 | 1-5数字，选填，默认3 |
        | D | 来源 | 选填，如：学科网 |
        | E | 知识点 | 选填，如：光合作用 |
        | F | 关键词 | 选填，逗号分隔 |
        | G | 题型 | 选填，如：选择题 |
        """)
        
        uploaded_file = st.file_uploader("选择文件", type=["xlsx", "xls", "docx", "json"])
        
        if uploaded_file:
            # 保存上传的文件
            upload_dir = os.path.join(os.path.dirname(__file__), "data", "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            
            file_path = os.path.join(upload_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.info(f"文件已上传：{uploaded_file.name}")
            
            if st.button("🚀 开始导入"):
                with st.spinner("正在导入..."):
                    try:
                        questions = importer.import_questions_auto(file_path)
                        
                        if not questions:
                            st.warning("未能从文件中提取题目，请检查文件格式！")
                        else:
                            # 插入数据库
                            count = database.insert_questions_batch(questions)
                            
                            # 添加到向量库
                            for i, q in enumerate(questions):
                                q["text"] = q.get("title", "") + " " + q.get("knowledge_point", "") + " " + q.get("keywords", "")
                                q["id"] = database.insert_question(
                                    title=q.get("title", ""),
                                    answer=q.get("answer", ""),
                                    difficulty=q.get("difficulty", 3),
                                    source=q.get("source", ""),
                                    knowledge_point=q.get("knowledge_point", ""),
                                    keywords=q.get("keywords", ""),
                                    question_type=q.get("question_type", "选择题")
                                )
                                vector_store.add_question(
                                    question_id=q["id"],
                                    text=q["text"],
                                    metadata=q
                                )
                            
                            st.success(f"✅ 成功导入 {len(questions)} 道题目！")
                            st.rerun()
                    
                    except Exception as e:
                        st.error(f"导入失败：{str(e)}")
        
        # 批量导入示例
        st.divider()
        st.markdown("### 📁 批量导入")
        st.markdown("如需批量导入多个文件，请将文件放入 `data/uploads/` 目录后运行：")
        st.code("python -c \"import importer; importer.import_from_excel('your_file.xlsx')\"")
    
    # ===== 导出试卷 =====
    elif menu == "📤 导出试卷":
        st.header("📤 导出试卷")
        
        if not st.session_state.selected_questions:
            st.warning("请先在「题库浏览」或「题目搜索」中选择题目！")
        else:
            st.success(f"已选择 {len(st.session_state.selected_questions)} 道题目")
            
            # 预览已选题目
            with st.expander("👀 预览已选题目", expanded=True):
                selected_qs = [database.get_question_by_id(qid) for qid in st.session_state.selected_questions]
                for q in selected_qs:
                    if q:
                        st.markdown(f"**{q['id']}.** {q.get('title', '')[:60]}...")
            
            # 导出设置
            st.markdown("### 导出设置")
            
            export_col1, export_col2 = st.columns(2)
            with export_col1:
                exam_title = st.text_input("试卷标题", value="高中生物练习题")
            with export_col2:
                export_format = st.selectbox("导出格式", ["Word文档（含答案）", "Word文档（题目+答案分开）", "Excel表格"])
            
            if export_format == "Word文档（含答案）":
                output_name = st.text_input("文件名", value="生物试卷.docx")
                
                if st.button("📥 导出 Word"):
                    output_path = os.path.join(os.path.dirname(__file__), "data", "exports", output_name)
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    
                    with st.spinner("正在生成试卷..."):
                        selected_qs = [database.get_question_by_id(qid) for qid in st.session_state.selected_questions]
                        exporter.export_to_word(selected_qs, output_path, exam_title)
                    
                    st.success(f"✅ 试卷已生成：{output_path}")
                    with open(output_path, "rb") as f:
                        st.download_button("⬇️ 下载试卷", f, file_name=output_name)
            
            elif export_format == "Word文档（题目+答案分开）":
                output_name = st.text_input("文件名", value="生物试卷_含答案.docx")
                
                if st.button("📥 导出 Word（题目+答案）"):
                    output_path = os.path.join(os.path.dirname(__file__), "data", "exports", output_name)
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    
                    with st.spinner("正在生成试卷..."):
                        selected_qs = [database.get_question_by_id(qid) for qid in st.session_state.selected_questions]
                        exporter.export_to_word_with_answer_sheet(selected_qs, output_path, exam_title)
                    
                    st.success(f"✅ 试卷已生成：{output_path}")
                    with open(output_path, "rb") as f:
                        st.download_button("⬇️ 下载试卷", f, file_name=output_name)
            
            else:
                output_name = st.text_input("文件名", value="生物题目.xlsx")
                
                if st.button("📥 导出 Excel"):
                    output_path = os.path.join(os.path.dirname(__file__), "data", "exports", output_name)
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    
                    with st.spinner("正在生成表格..."):
                        selected_qs = [database.get_question_by_id(qid) for qid in st.session_state.selected_questions]
                        exporter.export_to_excel(selected_qs, output_path)
                    
                    st.success(f"✅ 表格已生成：{output_path}")
                    with open(output_path, "rb") as f:
                        st.download_button("⬇️ 下载表格", f, file_name=output_name)
    
    # ===== 数据统计 =====
    elif menu == "📊 数据统计":
        st.header("📊 数据统计")
        
        stats = database.get_statistics()
        
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.metric("总题目数", stats["total"])
        with stat_col2:
            st.metric("知识点数", stats["knowledge_point_count"])
        with stat_col3:
            st.metric("来源数", stats["source_count"])
        with stat_col4:
            types = list(stats["type_distribution"].keys())
            st.metric("题型种类", len(types))
        
        # 题型分布
        st.markdown("### 题型分布")
        if stats["type_distribution"]:
            for qtype, count in stats["type_distribution"].items():
                percentage = (count / stats["total"] * 100) if stats["total"] > 0 else 0
                st.progress(percentage / 100, text=f"{qtype}: {count} ({percentage:.1f}%)")
        
        # 知识点分布
        st.markdown("### 知识点分布")
        knowledge_points = database.get_all_knowledge_points()
        if knowledge_points:
            for kp in knowledge_points[:20]:
                count = len(database.search_questions(knowledge_point=kp))
                st.markdown(f"- **{kp}**: {count} 题")
        else:
            st.info("暂无知识点数据")


if __name__ == "__main__":
    main()
