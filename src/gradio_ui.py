import gradio as gr
from functools import partial

# Import handlers
from src.gradio_handlers import (
    add_text,
    add_file,
    reset_user_input,
    reset_state,
    predict,
    regenerate
)


def create_demo(args):
    """
    Builds the Gradio UI and wires up the event handlers.
    """
    # Use functools.partial to pass the 'args' object to the handlers
    predict_with_args = partial(predict, args=args)
    regenerate_with_args = partial(regenerate, args=args)
    
    with gr.Blocks() as demo:
        gr.Markdown("""<center><font size=3> Local Multi-Modal LLM Demo (via OLLAMA) </center>""")

        chatbot = gr.Chatbot(label='OLLAMA Chat', elem_classes="control-height", height=500)
        query = gr.Textbox(lines=2, label='Input')
        task_history = gr.State([])

        with gr.Row():
            addfile_btn = gr.UploadButton("📁 Upload Image (上传图片)", file_types=["image"])
            submit_btn = gr.Button("🚀 Submit (发送)")
            regen_btn = gr.Button("🤔️ Regenerate (重试)")
            empty_bin = gr.Button("🧹 Clear History (清除历史)")

        # Wire up the event handlers
        submit_btn.click(
            add_text, 
            [chatbot, task_history, query], 
            [chatbot, task_history, query]
        ).then(
            predict_with_args, [chatbot, task_history], [chatbot]
        )

        empty_bin.click(
            reset_state, 
            [task_history], 
            [chatbot], 
            show_progress=True
        )

        regen_btn.click(
            regenerate_with_args, 
            [chatbot, task_history], 
            [chatbot], 
            show_progress=True
        )

        addfile_btn.upload(
            add_file, 
            [chatbot, task_history, addfile_btn], 
            [chatbot, task_history], 
            show_progress=True
        )
        
    return demo 