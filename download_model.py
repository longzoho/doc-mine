from ctransformers import AutoModelForCausalLM

# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
if __name__ == '__main__':
    llm = AutoModelForCausalLM.from_pretrained("TheBloke/Llama-2-7b-Chat-GGML",
                                               model_file="llama-2-7b-chat.q4_K_M.gguf",
                                               model_type="llama", gpu_layers=50)

    print(llm("AI is going to"))
