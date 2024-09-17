import streamlit as st
import markdown2
import pdfkit
import io

def convert_markdown_to_html(markdown_text):
    try:
        html_content = markdown2.markdown(markdown_text, extras=["tables", "break-on-newline", "fenced-code-blocks", "codehilite"])
        return html_content
    except Exception as e:
        st.error(f"Error converting Markdown to HTML: {e}")
        return None

def main():
    st.set_page_config(page_title="Markdown to PDF Converter", layout="wide")
    
    st.title("Markdown to PDF Converter")
    st.markdown("---")

    # Initialize session state for the list
    if 'custom_list' not in st.session_state:
        st.session_state.custom_list = []

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Input Markdown")
        markdown_text = st.text_area("Enter your Markdown text here", height=300, key="markdown_input")

        # Add custom list functionality
        st.subheader("Custom List")
        new_item = st.text_input("Add new item")
        if st.button("Add"):
            st.session_state.custom_list.append(new_item)
            st.experimental_rerun()

        # Display and allow deletion of list items
        for i, item in enumerate(st.session_state.custom_list):
            col1, col2 = st.columns([4, 1])
            col1.text(item)
            if col2.button("Delete", key=f"delete_{i}"):
                st.session_state.custom_list.pop(i)
                st.experimental_rerun()

    if markdown_text or st.session_state.custom_list:
        html_content = convert_markdown_to_html(markdown_text)

        # Add custom list to HTML content
        if st.session_state.custom_list:
            html_content += "<h3>Custom List</h3><ul>"
            for item in st.session_state.custom_list:
                html_content += f"<li>{item}</li>"
            html_content += "</ul>"

        if html_content:
            with col2:
                st.subheader("PDF Settings")
                with st.expander("Customize PDF", expanded=True):
                    font_size = st.text_input('Font size', value='20')
                    line_height = st.text_input('Line height', value='2.0')
                    
                    file_name_col, pdf_suffix_col = st.columns([4, 1])
                    with file_name_col:
                        file_name = st.text_input('File name', value='converted')
                    with pdf_suffix_col:
                        st.text_input('', value='.pdf', disabled=True)

                st.markdown("---")
                st.subheader("Generate PDF")
                if st.button("Generate and Download PDF", use_container_width=True):
                    try:
                        font_size = int(font_size)
                        line_height = float(line_height)
                    except ValueError:
                        st.error("Invalid input for font size or line height. Please enter numeric values.")
                        return

                    css = f"""
                    <style>
                        body {{
                            font-size: {font_size}px;
                            line-height: {line_height};
                        }}
                        p {{ margin-bottom: 1em; }}
                        ol, ul {{ padding-left: 20px; }}
                        li {{ margin-bottom: 0.5em; }}
                        table {{
                            border-collapse: collapse;
                            width: 100%;
                            margin-bottom: 1em;
                        }}
                        th, td {{
                            border: 1px solid #ddd;
                            padding: 8px;
                            text-align: left;
                        }}
                        th {{ background-color: #f2f2f2; }}
                        pre, code {{
                            background-color: #f5f5f5;
                            border: 1px solid #ccc;
                            border-radius: 4px;
                            padding: 10px;
                            font-family: monospace;
                            white-space: pre-wrap;
                            word-wrap: break-word;
                        }}
                        pre code {{
                            border: none;
                            padding: 0;
                        }}
                    </style>
                    """

                    html_preview = f"{css}<div>{html_content}</div>"

                    pdf_options = {
                        'quiet': '',
                        'no-outline': None,
                        'dpi': 300,
                        'margin-top': '20mm',
                        'margin-right': '20mm',
                        'margin-bottom': '20mm',
                        'margin-left': '20mm',
                        'encoding': "UTF-8",
                        'custom-header': [('Accept-Encoding', 'gzip')],
                        'zoom': 1,
                        'minimum-font-size': font_size,
                    }

                    pdf_bytes = pdfkit.from_string(html_preview, False, options=pdf_options)

                    if pdf_bytes:
                        st.download_button(
                            label="Download PDF",
                            data=pdf_bytes,
                            file_name=f"{file_name}.pdf",
                            mime="application/pdf",
                            key="pdf_download_button",
                            use_container_width=True  
                        )
                        st.success("PDF generated successfully. Click the download button above to save it.")
                    else:
                        st.error("Failed to generate PDF. Please check your input and try again.")

                st.markdown("---")
                st.subheader("Preview")
                with st.expander("HTML Preview", expanded=False):
                    st.markdown(html_content, unsafe_allow_html=True)

    else:
        with col2:
            st.info("Enter some Markdown text to see the preview and generate a PDF.")

if __name__ == "__main__":
    main()
