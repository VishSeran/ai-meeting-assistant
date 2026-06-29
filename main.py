import gradio as gr
from app import speech_to_text

def gradio_interface():
    
    audio_input = gr.Audio(label="Upload your audio file", sources="upload", type="filepath")
    output_text = gr.Textbox(label="Meeting Minutes and Tasks")
    download_file = gr.File(label="Download the Generated Meeting Minutes and Tasks")
    
    interface = gr.Interface(
        fn=speech_to_text,
        inputs=audio_input,
        outputs=[output_text, download_file],
        title="AI Meeting Assistant",
        description="Upload an audio file of a meeting. This tool will transcribe the audio, fix product-related terminology, and generate meeting minutes along with a list of tasks."
    )
    
    interface.launch()
    
if __name__ == "__main__":
    gradio_interface()