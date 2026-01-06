---
title: Notes
---
# What is NLP?
NLP is a field of linguistics and machine learning focused on understanding everything related to human language. The aim of NLP tasks is not only to understand single words individually, but to be able to understand the context of those words. [🔗](https://huggingface.co/learn/llm-course/chapter1/2)

**Common NLP Tasks:**
- Classifying whole sentences
- Classifying each word in a sentence
- Generating text content
- Extracting an answer from a text
- Generating a new sentence from an input text

**Characteristics of LLMs:**
- **Scale**: They contain millions, billions, or even hundreds of billions of parameters
- **General capabilities**: They can perform multiple tasks without task-specific training
- **In-context learning**: They can learn from examples provided in the prompt
- **Emergent abilities**: They can demonstrate capabilities that weren’t explicitly programmed or anticipated

**Limitations of LLMs:**
- **Hallucinations**: They can generate incorrect information confidently
- **Lack of true understanding**: They lack true understanding of the world and operate purely on statistical patterns
- **Bias**: They may reproduce biases present in their training data or inputs.
- **Context windows**: They have limited context windows (though this is improving)
- **Computational resources**: They require significant computational resources

# HuggingFace Pipelines/Tasks
**Text pipelines**
- `text-generation`: Generate text from a prompt
- `text-classification`: Classify text into predefined categories
- `summarization`: Create a shorter version of a text while preserving key information
- `translation`: Translate text from one language to another
- `zero-shot-classification`: Classify text without prior training on specific labels
- `feature-extraction`: Extract vector representations of text

**Image pipelines**
- `image-to-text`: Generate text descriptions of images
- `image-classification`: Identify objects in an image
- `object-detection`: Locate and identify objects in images

**Audio pipelines**
- `automatic-speech-recognition`: Convert speech to text
- `audio-classification`: Classify audio into categories
- `text-to-speech`: Convert text to spoken audio

**Multimodal pipelines**
- `image-text-to-text`: Respond to an image based on a text prompt

