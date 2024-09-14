import streamlit as st
import markdown2
import pdfkit
import io

def convert_markdown_to_html(markdown_text):
    try:
        # Convert Markdown to HTML with table support
        html_content = markdown2.markdown(markdown_text, extras=["tables", "break-on-newline", "fenced-code-blocks"])
        return html_content
    except Exception as e:
        st.error(f"Error converting Markdown to HTML: {e}")
        return None

def main():
    st.set_page_config(page_title="Markdown to PDF Converter", layout="wide")
    
    st.title("Markdown to PDF Converter")
    st.markdown("---")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Input Markdown")
        markdown_text = st.text_area("Enter your Markdown text here", height=400, key="markdown_input")

    if markdown_text:
        html_content = convert_markdown_to_html(markdown_text)

        if html_content:
            with col2:
                st.subheader("PDF Settings")
                with st.expander("Customize PDF", expanded=True):
                    font_size = st.slider('Font size', min_value=10, max_value=36, value=14)
                    font_family = st.selectbox('Font', options=['Arial', 'Helvetica', 'Times New Roman', 'Courier New', 'Verdana'])
                    line_height = st.slider('Line height', min_value=1.0, max_value=2.0, value=1.5, step=0.1)
                    page_size = st.selectbox('Page size', options=['A4', 'Letter', 'Legal'])

                # Move the download button here
                st.markdown("---")
                st.subheader("Generate PDF")
                if st.button("Generate and Download PDF", use_container_width=True):
                    # Generate PDF
                    css = f"""
                    <style>
                        body {{
                            font-family: '{font_family}', sans-serif;
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
                    </style>
                    """

                    html_preview = f"{css}<div style='background-color: white;'>{html_content}</div>"

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
                        'page-size': page_size,
                        'minimum-font-size': font_size,
                        'enable-local-file-access': None,
                    }

                    # Add this line to set the default font
                    pdf_options['--default-font'] = font_family

                    try:
                        pdf_bytes = pdfkit.from_string(html_preview, False, options=pdf_options)

                        if pdf_bytes:
                            pdf_preview_io = io.BytesIO(pdf_bytes)
                            pdf_preview_io.seek(0)

                            st.download_button(
                                label="Download PDF",
                                data=pdf_preview_io,
                                file_name="converted.pdf",
                                mime="application/pdf",
                                key="pdf_preview_download_button",
                            )
                        else:
                            st.error("Failed to generate PDF. The PDF output is empty.")
                    except IOError as e:
                        st.error(f"Error generating PDF: {str(e)}")
                        st.info("This error might be due to wkhtmltopdf not being installed or configured correctly. Please check your system configuration.")
                    except Exception as e:
                        st.error(f"An unexpected error occurred: {str(e)}")

                st.markdown("---")
                st.subheader("Preview")
                with st.expander("HTML Preview", expanded=False):
                    st.markdown(html_content, unsafe_allow_html=True)

    else:
        with col2:
            st.info("Enter some Markdown text to see the preview and generate a PDF.")

if __name__ == "__main__":
    main()
