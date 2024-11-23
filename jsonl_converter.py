import gradio as gr
import pandas as pd
from pathlib import Path


def load_data(input_file):
    if not input_file:
        return None
    filepath = Path(input_file)
    if filepath.suffix == ".jsonl":
        return pd.read_json(filepath, lines=True)
    elif filepath.suffix == ".json":
        return pd.read_json(filepath, orient="records")
    elif filepath.suffix == ".xlsx":
        return pd.read_excel(filepath)
    elif filepath.suffix == ".csv":
        return pd.read_csv(filepath)

def write_data(data, export_to, input_file):
    input_file = Path(input_file)
    export_files = []
    for format in export_to:
        if format == ".jsonl":
            output_file = input_file.with_suffix(".jsonl")
            data.to_json(output_file, lines=True, orient="records", force_ascii=False)
            export_files.append(str(output_file))
        elif format == ".json":
            output_file = input_file.with_suffix(".json")
            data.to_json(output_file, orient="records", force_ascii=False, indent=4)
            export_files.append(str(output_file))
        elif format == ".xlsx":
            output_file = input_file.with_suffix(".xlsx")
            data.to_excel(output_file, index=False)
            export_files.append(str(output_file))
        elif format == ".csv":
            output_file = input_file.with_suffix(".csv")
            data.to_csv(output_file, index=False)
            export_files.append(str(output_file))
    return export_files

with gr.Blocks() as demo:
    gr.Markdown("# JSONL Converter")
    gr.Markdown("JSONL, JSON, XLSX, CSV ファイルを相互に変換します。")
    with gr.Row():
        format_list = [".jsonl", ".json", ".xlsx", ".csv"]
        with gr.Column():
            gr.Markdown("### Input File")
            input_file = gr.File(show_label=False, file_types=format_list)
        with gr.Column():
            gr.Markdown("### Convert to")
            gr.Markdown("選択したフォーマットにデータを変換します。")
            export_format = gr.CheckboxGroup(format_list, show_label=False)
            convert = gr.Button(value="Convert")
        with gr.Column():
            gr.Markdown("### Output File")
            output_file = gr.Files(show_label=False, label="Output File")
    gr.Markdown("### Preview")
    data_frame = gr.Dataframe()
    
    input_file.change(load_data, inputs=[input_file], outputs=[data_frame])
    convert.click(write_data, inputs=[data_frame, export_format, input_file], outputs=[output_file])

if __name__ == "__main__":
    demo.queue().launch()