import gradio as gr

def gradio_interface():
    
    audio_input = gr.Audio(label="Upload your audio file", sources="upload", type="filepath")
    output_text = gr.Textbox(label="Meeting Minutes and Tasks")
    download_file = gr.File(label="Download the Generated Meeting Minutes and Tasks")
    
    interface = gr.Interface(
        fn=
    )