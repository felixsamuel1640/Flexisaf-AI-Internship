# Understanding How Large Language Models (LLMs) Work

Large Language Models (LLMs) process text by first breaking user input into smaller 
units called tokens through a process known as tokenization. These tokens are 
converted into numerical representations called embeddings, allowing the model to 
work with language as numbers rather than words.

The embeddings are then passed through multiple transformer layers, which form the 
core of modern LLMs. Within these layers, the attention mechanism enables the model 
to consider all tokens at once and focus on the most relevant ones, helping it 
understand context and relationships across the entire input. As the data moves 
through successive layers, the model builds a deeper contextual understanding and 
ultimately predicts the most likely next tokens to generate a coherent output.

## Diagram

The diagram below illustrates the step-by-step flow of how an LLM processes text, 
from user input to final output.
