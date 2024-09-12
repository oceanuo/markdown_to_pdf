import streamlit as st
import markdown2
import pdfkit
import io
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def convert_markdown_to_html(markdown_text):
    try:
        # Convert Markdown to HTML with table support and code blocks
        html_content = markdown2.markdown(markdown_text, extras=["tables", "break-on-newline", "fenced-code-blocks"])
        
        # Add syntax highlighting to code blocks
        def highlight_code(match):
            lang = match.group(1) or 'text'
            code = match.group(2)
            try:
                lexer = get_lexer_by_name(lang, stripall=True)
            except ValueError:
                lexer = get_lexer_by_name('text', stripall=True)
            formatter = HtmlFormatter(style='default', noclasses=True)
            return highlight(code, lexer, formatter)
        
        import re
        # Handle triple backtick code blocks
        html_content = re.sub(r'<pre><code class="language-(\w+)">(.*?)</code></pre>', highlight_code, html_content, flags=re.DOTALL)
        
        # Handle single backtick inline code
        html_content = re.sub(r'<code>(.*?)</code>', lambda m: f'<code style="background-color: #f0f0f0; padding: 2px 4px; border-radius: 4px;">{m.group(1)}</code>', html_content)
        
        return html_content
    except Exception as e:
        st.error(f"Error converting Markdown to HTML: {e}")
        return None

def main():
    st.title("Markdown to PDF App")

    uploaded_file = st.sidebar.file_uploader("Upload a Markdown file", type=["md"])

    col1, col2 = st.columns(2)

    markdown_text = ""
    with col1:
        st.header("Input Markdown")
        if uploaded_file is not None:
            markdown_text = uploaded_file.read().decode("utf-8")
        else:
            markdown_text = st.text_area("Enter Markdown text here", height=400)

    if markdown_text:
        html_content = convert_markdown_to_html(markdown_text)

        if html_content:
            with col2:
                st.header("HTML Preview")
                with st.expander("Show HTML Preview", expanded=False):
                    st.markdown(html_content, unsafe_allow_html=True)

                font_size = st.slider('Select font size', min_value=10, max_value=36, value=20)
                font_family = st.selectbox('Select font family', options=['Arial', 'Helvetica', 'Times New Roman', 'Courier New', 'Verdana'])
                line_height = st.slider('Select line height', min_value=1.0, max_value=2.0, value=2.0, step=0.1)

                css = f"""
                <style>
                    body {{
                        font-family: {font_family}, sans-serif;
                        font-size: {font_size}px;
                        line-height: {line_height};
                    }}
                    /* ... (other CSS remains the same) ... */
                    pre {{
                        background-color: #f5f5f5;
                        border: 1px solid #ccc;
                        border-radius: 4px;
                        padding: 10px;
                        overflow-x: auto;
                    }}
                    code {{
                        font-family: 'Courier New', Courier, monospace;
                        font-size: 0.9em;
                    }}
                </style>
                """

                html_preview = f"""
                {css}
                <div style="background-color: white;">
                    {html_content}
                </div>
                """

                pdf_options = {
                    'quiet': '',
                    'no-outline': None,
                    'dpi': 300,
                    'margin-top': '20mm',
                    'margin-right': '20mm',
                    'margin-bottom': '20mm',
                    'margin-left': '20mm',
                    'encoding': "UTF-8",
                    'custom-header' : [
                        ('Accept-Encoding', 'gzip')
                    ],
                    'no-outline': None,
                    'zoom': 1,
                    'page-size': 'Letter',
                    'minimum-font-size': font_size,
                }

                pdf_bytes = pdfkit.from_string(html_preview, False, options=pdf_options)

                if pdf_bytes:
                    pdf_preview_io = io.BytesIO(pdf_bytes)
                    pdf_preview_io.seek(0)

                    st.text_area("PDF Preview", "PDF generated successfully. Click the button below to download.", height=100, disabled=True)
                    st.download_button(
                        label="Download PDF",
                        data=pdf_preview_io,
                        file_name="converted.pdf",
                        mime="application/pdf",
                        key="pdf_preview_download_button"
                    )
                else:
                    st.write("Failed to generate PDF.")

if __name__ == "__main__":
    main()
