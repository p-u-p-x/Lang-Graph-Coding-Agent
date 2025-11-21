import streamlit as st
import os
import subprocess
import threading
import time
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools import PROJECT_ROOT, create_web_server, open_web_browser, check_html_files, init_project_root

def list_generated_files():
    """List all files in the generated project"""
    try:
        files = []
        for root, dirs, filenames in os.walk(PROJECT_ROOT):
            for filename in filenames:
                relative_path = os.path.relpath(os.path.join(root, filename), PROJECT_ROOT)
                files.append(relative_path)
        return files
    except Exception as e:
        return [f"Error listing files: {e}"]

def read_file_content(filepath):
    """Read content of a file"""
    try:
        full_path = PROJECT_ROOT / filepath
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def main():
    st.set_page_config(page_title="🔄 LangGraph Project Generator", layout="wide")

    st.title("🔄 LangGraph Project Generator")
    st.markdown("---")

    # Initialize project directory
    init_project_root()

    # Project generation section
    col1, col2 = st.columns([2, 1])

    with col1:
        user_prompt = st.text_area(
            "Enter your project prompt:",
            placeholder="e.g., Create a colorful modern todo app with dark mode using HTML, CSS, and JavaScript",
            height=100
        )

        if st.button("🚀 Generate Project", type="primary"):
            if user_prompt.strip():
                with st.spinner("Generating project... This may take a minute."):
                    try:
                        # Import and run the agent
                        from graph import agent
                        result = agent.invoke(
                            {"user_prompt": user_prompt},
                            {"recursion_limit": 100}
                        )
                        st.success("✅ Project generation completed!")
                    except Exception as e:
                        st.error(f"❌ Error during generation: {e}")
            else:
                st.warning("⚠️ Please enter a project prompt")

    with col2:
        st.markdown("### Quick Actions")
        if st.button("📁 List Generated Files"):
            files = list_generated_files()
            if files:
                st.write("**Generated Files:**")
                for file in files:
                    st.write(f"- `{file}`")
            else:
                st.info("No files generated yet")

        if st.button("🌐 Start Web Server"):
            try:
                create_web_server(8000)
                st.success("Web server started on http://localhost:8000")
            except Exception as e:
                st.error(f"Error starting server: {e}")

        if st.button("🔍 Check HTML Files"):
            result = check_html_files()
            st.info(result)

    st.markdown("---")

    # File browser section
    st.subheader("📁 Project Files")

    files = list_generated_files()
    if files:
        selected_file = st.selectbox("Select a file to view:", files)

        if selected_file:
            content = read_file_content(selected_file)
            st.text_area(f"Content of `{selected_file}`:", content, height=400)
    else:
        st.info("No project files generated yet. Enter a prompt above to get started!")

    # Quick preview section
    st.markdown("---")
    st.subheader("🎯 Quick Preview")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🖥️ Open in Browser", type="secondary"):
            try:
                open_web_browser(8000)
                st.success("Opening browser...")
            except Exception as e:
                st.error(f"Error opening browser: {e}")

    with col2:
        if st.button("🔄 Restart Server", type="secondary"):
            try:
                create_web_server(8000)
                st.success("Server restarted!")
            except Exception as e:
                st.error(f"Error restarting server: {e}")

if __name__ == "__main__":
    main()