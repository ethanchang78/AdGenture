import torch.nn as nn
import pandas as pd
from transformers import GPT2LMHeadModel, BertTokenizer, GPT2Tokenizer
import torch

# Tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
tokenizer.pad_token = tokenizer.eos_token

class Novelizer(nn.Module):
  def __init__(self, generator, device):
    super(Novelizer, self).__init__()
    self.tokenizer = tokenizer
    self.generator = generator
    self.device = device

  def forward(self, input_ids, labels):
    input_ids = input_ids.to(self.device)

    outputs = self.generator(input_ids=input_ids, labels=input_ids)
    return outputs

  def generate_story_intro(self, story_type, num_return_sequences=1, device='cpu'): #Change num of sequences to get different answers
    # Tokenize the story type prompt
    input_ids = self.tokenizer.encode(story_type, return_tensors="pt").to(device)
    num_beams = max(num_return_sequences, 1)
    # Use the forward method to generate text
    self.generator.to(device)
    generated_sequences = self.generator.generate(
            input_ids,
            max_length=128, # max length
            num_return_sequences=num_return_sequences,
            num_beams=num_beams,
            no_repeat_ngram_size=2,
            top_k=50,
            top_p=0.95,
            temperature=0.4
        )

    return [
            self.tokenizer.decode(generated_sequence, skip_special_tokens=True)
            for generated_sequence in generated_sequences
        ]
