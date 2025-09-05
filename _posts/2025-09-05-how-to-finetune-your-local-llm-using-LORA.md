---
layout: post
title: "How to finetune your local llm using LORA"
date: 2025-09-05
---

# Train in hours not days using LORA 
## LoRA = Tiny Add-On Brains 🧠

Instead of training all billion parameters, LoRA adds small trainable matrices.

Think of it as teaching just a few neurons, not rewiring the whole brain.

## Magic Settings ⚡

- Rank (r): How many "extra neurons" LoRA adds (small r = more compression).

- Alpha: How strong those neurons influence the model.

- Dropout: Prevents overfitting — like making the neurons forget some details.

## Result = Cheap + Fast Training 💸

- Train a model on your laptop in hours (not days).

- Save GPU memory while keeping accuracy.

- Perfect for fine-tuning chatbots, code assistants, or small domain models.

<details>
<summary>Click to expand and see dependancy for this project📌</summary>

``` 
name: lora
channels:
  - defaults
dependencies:
  - _libgcc_mutex=0.1=main
  - _openmp_mutex=5.1=1_gnu
  - bzip2=1.0.8=h5eee18b_6
  - ca-certificates=2025.7.15=h06a4308_0
  - expat=2.7.1=h6a678d5_0
  - ld_impl_linux-64=2.40=h12ee557_0
  - libffi=3.4.4=h6a678d5_1
  - libgcc-ng=11.2.0=h1234567_1
  - libgomp=11.2.0=h1234567_1
  - libstdcxx-ng=11.2.0=h1234567_1
  - libuuid=1.41.5=h5eee18b_0
  - libxcb=1.17.0=h9b100fa_0
  - ncurses=6.5=h7934f7d_0
  - openssl=3.0.17=h5eee18b_0
  - pip=25.2=pyhc872135_0
  - pthread-stubs=0.3=h0ce48e5_1
  - python=3.10.18=h1a3bd86_0
  - readline=8.3=hc2a1206_0
  - setuptools=78.1.1=py310h06a4308_0
  - sqlite=3.50.2=hb25bd0a_1
  - tk=8.6.15=h54e0aa7_0
  - wheel=0.45.1=py310h06a4308_0
  - xorg-libx11=1.8.12=h9b100fa_1
  - xorg-libxau=1.0.12=h9b100fa_0
  - xorg-libxdmcp=1.1.5=h9b100fa_0
  - xorg-xorgproto=2024.1=h5eee18b_1
  - xz=5.6.4=h5eee18b_1
  - zlib=1.2.13=h5eee18b_1
  - pip:
      - accelerate==0.31.0
      - aiohappyeyeballs==2.6.1
      - aiohttp==3.12.15
      - aiosignal==1.4.0
      - alembic==1.16.5
      - annotated-types==0.7.0
      - annoy==1.17.3
      - anyio==4.10.0
      - argon2-cffi==25.1.0
      - argon2-cffi-bindings==25.1.0
      - arrow==1.3.0
      - asttokens==3.0.0
      - async-lru==2.0.5
      - async-timeout==4.0.3
      - attrs==25.3.0
      - babel==2.17.0
      - banal==1.0.6
      - beautifulsoup4==4.13.5
      - bertopic==0.16.3
      - bitsandbytes==0.43.1
      - bleach==6.2.0
      - boto3==1.40.24
      - botocore==1.40.24
      - certifi==2025.8.3
      - cffi==1.17.1
      - charset-normalizer==3.4.3
      - click==8.2.1
      - cohere==5.5.8
      - colorcet==3.1.0
      - colorspacious==1.1.2
      - comm==0.2.3
      - contourpy==1.3.2
      - cycler==0.12.1
      - dataclasses-json==0.6.7
      - datamapplot==0.3.0
      - dataset==1.6.2
      - datasets==2.20.0
      - datashader==0.18.2
      - debugpy==1.8.16
      - decorator==5.2.1
      - defusedxml==0.7.1
      - dill==0.3.8
      - diskcache==5.6.3
      - distro==1.9.0
      - docstring-parser==0.17.0
      - duckduckgo-search==7.1.1
      - eval-type-backport==0.2.2
      - evaluate==0.4.2
      - exceptiongroup==1.3.0
      - executing==2.2.1
      - faiss-cpu==1.8.0
      - fastavro==1.12.0
      - fastjsonschema==2.21.2
      - filelock==3.19.1
      - fonttools==4.59.2
      - fqdn==1.5.1
      - frozenlist==1.7.0
      - fsspec==2024.5.0
      - gensim==4.3.2
      - greenlet==3.2.4
      - h11==0.16.0
      - hdbscan==0.8.40
      - hf-xet==1.1.9
      - httpcore==1.0.9
      - httpx==0.28.1
      - httpx-sse==0.4.1
      - huggingface-hub==0.34.4
      - idna==3.10
      - imageio==2.37.0
      - ipykernel==6.30.1
      - ipython==8.37.0
      - ipywidgets==8.1.3
      - isoduration==20.11.0
      - jedi==0.19.2
      - jinja2==3.1.6
      - jmespath==1.0.1
      - joblib==1.5.2
      - json5==0.12.1
      - jsonpatch==1.33
      - jsonpointer==3.0.0
      - jsonschema==4.25.1
      - jsonschema-specifications==2025.4.1
      - jupyter-client==8.6.3
      - jupyter-core==5.8.1
      - jupyter-events==0.12.0
      - jupyter-lsp==2.3.0
      - jupyter-server==2.17.0
      - jupyter-server-terminals==0.5.3
      - jupyterlab==4.2.2
      - jupyterlab-pygments==0.3.0
      - jupyterlab-server==2.27.3
      - jupyterlab-widgets==3.0.15
      - kiwisolver==1.4.9
      - langchain==0.2.5
      - langchain-community==0.2.5
      - langchain-core==0.2.43
      - langchain-openai==0.1.8
      - langchain-text-splitters==0.2.4
      - langsmith==0.1.147
      - lark==1.2.2
      - lazy-loader==0.4
      - llama-cpp-python==0.2.78
      - llvmlite==0.44.0
      - lxml==6.0.1
      - mako==1.3.10
      - markdown-it-py==4.0.0
      - markupsafe==3.0.2
      - marshmallow==3.26.1
      - matplotlib==3.9.0
      - matplotlib-inline==0.1.7
      - mdurl==0.1.2
      - mistune==3.1.4
      - mpmath==1.3.0
      - mteb==1.12.39
      - multidict==6.6.4
      - multipledispatch==1.0.0
      - multiprocess==0.70.16
      - mypy-extensions==1.1.0
      - narwhals==2.3.0
      - nbclient==0.10.2
      - nbconvert==7.16.6
      - nbformat==5.10.4
      - nest-asyncio==1.6.0
      - networkx==3.4.2
      - nltk==3.8.1
      - notebook-shim==0.2.4
      - numba==0.61.2
      - numexpr==2.10.0
      - numpy==1.26.4
      - nvidia-cublas-cu12==12.1.3.1
      - nvidia-cuda-cupti-cu12==12.1.105
      - nvidia-cuda-nvrtc-cu12==12.1.105
      - nvidia-cuda-runtime-cu12==12.1.105
      - nvidia-cudnn-cu12==8.9.2.26
      - nvidia-cufft-cu12==11.0.2.54
      - nvidia-cufile-cu12==1.13.1.3
      - nvidia-curand-cu12==10.3.2.106
      - nvidia-cusolver-cu12==11.4.5.107
      - nvidia-cusparse-cu12==12.1.0.106
      - nvidia-cusparselt-cu12==0.7.1
      - nvidia-nccl-cu12==2.20.5
      - nvidia-nvjitlink-cu12==12.8.93
      - nvidia-nvtx-cu12==12.1.105
      - openai==1.34.0
      - orjson==3.11.3
      - overrides==7.7.0
      - packaging==24.2
      - pandas==2.2.2
      - pandocfilters==1.5.1
      - param==2.2.1
      - parameterized==0.9.0
      - parso==0.8.5
      - peft==0.11.1
      - pexpect==4.9.0
      - pillow==11.3.0
      - platformdirs==4.4.0
      - plotly==6.3.0
      - polars==1.33.0
      - primp==0.15.0
      - prometheus-client==0.22.1
      - prompt-toolkit==3.0.52
      - propcache==0.3.2
      - psutil==7.0.0
      - ptyprocess==0.7.0
      - pure-eval==0.2.3
      - pyarrow==21.0.0
      - pyarrow-hotfix==0.7
      - pycparser==2.22
      - pyct==0.5.0
      - pydantic==2.11.7
      - pydantic-core==2.33.2
      - pygments==2.19.2
      - pylabeladjust==0.1.13
      - pynndescent==0.5.13
      - pyparsing==3.2.3
      - pyqtree==1.0.0
      - python-dateutil==2.9.0.post0
      - python-json-logger==3.3.0
      - pytrec-eval-terrier==0.5.8
      - pytz==2025.2
      - pyyaml==6.0.2
      - pyzmq==27.0.2
      - referencing==0.36.2
      - regex==2025.9.1
      - requests==2.32.5
      - requests-toolbelt==1.0.0
      - rfc3339-validator==0.1.4
      - rfc3986-validator==0.1.1
      - rfc3987-syntax==1.1.0
      - rich==14.1.0
      - rpds-py==0.27.1
      - s3transfer==0.13.1
      - safetensors==0.6.2
      - scikit-image==0.25.2
      - scikit-learn==1.5.0
      - scipy==1.15.3
      - send2trash==1.8.3
      - sentence-transformers==3.0.1
      - sentencepiece==0.2.0
      - seqeval==1.2.2
      - setfit==1.0.3
      - shtab==1.7.2
      - six==1.17.0
      - smart-open==7.3.0.post1
      - sniffio==1.3.1
      - soupsieve==2.8
      - sqlalchemy==1.4.54
      - stack-data==0.6.3
      - sympy==1.14.0
      - tenacity==8.5.0
      - terminado==0.18.1
      - threadpoolctl==3.6.0
      - tifffile==2025.5.10
      - tiktoken==0.11.0
      - tinycss2==1.4.0
      - tokenizers==0.19.1
      - tomli==2.2.1
      - toolz==1.0.0
      - torch==2.3.1
      - tornado==6.5.2
      - tqdm==4.67.1
      - traitlets==5.14.3
      - transformers==4.41.2
      - triton==2.3.1
      - trl==0.9.4
      - typeguard==4.4.4
      - types-python-dateutil==2.9.0.20250822
      - types-requests==2.32.4.20250809
      - typing-extensions==4.15.0
      - typing-inspect==0.9.0
      - typing-inspection==0.4.1
      - tyro==0.9.31
      - tzdata==2025.2
      - umap-learn==0.5.7
      - uri-template==1.3.0
      - urllib3==2.5.0
      - wcwidth==0.2.13
      - webcolors==24.11.1
      - webencodings==0.5.1
      - websocket-client==1.8.0
      - widgetsnbextension==4.0.14
      - wrapt==1.17.3
      - xarray==2025.6.1
      - xxhash==3.5.0
      - yarl==1.20.1
      - zstandard==0.24.0
prefix: /home/sv/anaconda3/envs/lora

```
</details>

<details>
<summary>Click to see code for quickly train using LORA</summary>

```python 

# -*- coding: utf-8 -*-
# Install the requirements in Google Colab
# !pip install transformers datasets trl huggingface_hub

# Authenticate to Hugging Face

# from huggingface_hub import login
#
# login()

# for convenience you can create an environment variable containing your hub token as HF_TOKEN

"""## 2. Load the dataset"""

# Load a sample dataset
from datasets import load_dataset

# TODO: define your dataset and config using the path and name parameters
dataset = load_dataset(path="HuggingFaceTB/smoltalk", name="everyday-conversations")

# 2. Show first row
print("data sample")
print(dataset['test'][0])

# Import necessary libraries
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
from trl import SFTConfig, SFTTrainer, setup_chat_format
import torch

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available() else "cpu"
)

# Load the model and tokenizer
model_name = "HuggingFaceTB/SmolLM2-135M"

model = AutoModelForCausalLM.from_pretrained(
    pretrained_model_name_or_path=model_name
).to(device)
tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=model_name)

# Set up the chat format
model, tokenizer = setup_chat_format(model=model, tokenizer=tokenizer)

# Set our name for the finetune to be saved &/ uploaded to
finetune_name = "SmolLM2-FT-MyDataset"
finetune_tags = ["smol-course", "module_1"]


from peft import LoraConfig

# TODO: Configure LoRA parameters
# r: rank dimension for LoRA update matrices (smaller = more compression)
rank_dimension = 6
# lora_alpha: scaling factor for LoRA layers (higher = stronger adaptation)
lora_alpha = 8
# lora_dropout: dropout probability for LoRA layers (helps prevent overfitting)
lora_dropout = 0.05

peft_config = LoraConfig(
    r=rank_dimension,  # Rank dimension - typically between 4-32
    lora_alpha=lora_alpha,  # LoRA scaling factor - typically 2x rank
    lora_dropout=lora_dropout,  # Dropout probability for LoRA layers
    bias="none",  # Bias type for LoRA. the corresponding biases will be updated during training.
    target_modules="all-linear",  # Which modules to apply LoRA to
    task_type="CAUSAL_LM",  # Task type for model architecture
)

"""Before we can start our training we need to define the hyperparameters (`TrainingArguments`) we want to use."""

# Training configuration
# Hyperparameters based on QLoRA paper recommendations
args = SFTConfig(
    # Output settings
    output_dir=finetune_name,  # Directory to save model checkpoints
    # Training duration
    num_train_epochs=1,  # Number of training epochs
    # Batch size settings
    per_device_train_batch_size=2,  # Batch size per GPU
    gradient_accumulation_steps=2,  # Accumulate gradients for larger effective batch
    # Memory optimization
    gradient_checkpointing=True,  # Trade compute for memory savings
    # Optimizer settings
    optim="adamw_torch_fused",  # Use fused AdamW for efficiency
    learning_rate=2e-4,  # Learning rate (QLoRA paper)
    max_grad_norm=0.3,  # Gradient clipping threshold
    # Learning rate schedule
    warmup_ratio=0.03,  # Portion of steps for warmup
    lr_scheduler_type="constant",  # Keep learning rate constant after warmup
    # Logging and saving
    logging_steps=10,  # Log metrics every N steps
    save_strategy="epoch",  # Save checkpoint every epoch
    # Precision settings
    bf16=True,  # Use bfloat16 precision
    # Integration settings
    push_to_hub=False,  # Don't push to HuggingFace Hub
    report_to="none",  # Disable external logging
)


max_seq_length = 1512  # max sequence length for model and packing of the dataset

# Create SFTTrainer with LoRA configuration
trainer = SFTTrainer(
    model=model,
    args=args,
    train_dataset=dataset["train"],
    peft_config=peft_config,  # LoRA configuration
    max_seq_length=max_seq_length,  # Maximum sequence length
    tokenizer=tokenizer,
    packing=True,  # Enable input packing for efficiency
    dataset_kwargs={
        "add_special_tokens": False,  # Special tokens handled by template
        "append_concat_token": False,  # No additional separator needed
    },
)

"""Start training our model by calling the `train()` method on our `Trainer` instance. This will start the training loop and train our model for 3 epochs. Since we are using a PEFT method, we will only save the adapted model weights and not the full model."""

# start training, the model will be automatically saved to the hub and the output directory
trainer.train()

# save model
trainer.save_model()


from peft import AutoPeftModelForCausalLM


# Load PEFT model on CPU
model = AutoPeftModelForCausalLM.from_pretrained(
    pretrained_model_name_or_path=args.output_dir,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True,
)

# Merge LoRA and base model and save
merged_model = model.merge_and_unload()
merged_model.save_pretrained(
    args.output_dir, safe_serialization=True, max_shard_size="2GB"
)

# free the memory again
del model
del trainer
torch.cuda.empty_cache()

```
</details>

<details>
<summary>How to use this trained model</summary>
```python 
from transformers import pipeline, AutoTokenizer
from peft import AutoPeftModelForCausalLM
import torch

finetune_name = "./SmolLM2-FT-MyDataset"

# 1. Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(finetune_name)

# 2. Load PEFT (LoRA) model
model = AutoPeftModelForCausalLM.from_pretrained(
    finetune_name,
    device_map="auto",
    torch_dtype=torch.float16
)

# Optional: merge LoRA weights into base
# model = model.merge_and_unload()

# 3. Create inference pipeline
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.float16,
    device_map="auto"
)

# ---- Test inference ----
prompt = ("What is the difference between a fruit and a "
          "vegetable? Give examples of each.")
outputs = pipe(prompt, max_new_tokens=100, do_sample=True, temperature=0.7)
print(outputs[0]["generated_text"])


```
</details>