import torch, re, glob
from torch import nn
from torchtext.data.utils import ngrams_iterator
from torchtext.data.utils import get_tokenizer

vocab = torch.load("dictionary.pt")

class TextSentiment(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_class):
        super().__init__()
        self.embedding = nn.EmbeddingBag(vocab_size, embed_dim, sparse=True)
        self.fc = nn.Linear(embed_dim, num_class)
        self.init_weights()

    def init_weights(self):
        initrange = 0.5
        self.embedding.weight.data.uniform_(-initrange, initrange)
        self.fc.weight.data.uniform_(-initrange, initrange)
        self.fc.bias.data.zero_()

    def forward(self, text, offsets):
        embedded = self.embedding(text, offsets)
        return self.fc(embedded)

ag_news_label = {1 : "World",
                 2 : "Sports",
                 3 : "Business",
                 4 : "Sci/Tec"}

model = torch.load("model.pt")


def predict(text, model, vocab, ngrams):
    tokenizer = get_tokenizer("basic_english")
    with torch.no_grad():
        text = torch.tensor([vocab[token]
                            for token in ngrams_iterator(tokenizer(text), ngrams)])
        output = model(text, torch.tensor([0]))
        return output.argmax(1).item() + 1

model = model.to("cpu")

with open('input.txt', 'r') as file:
    input = file.read().replace('\n', '')



output_str = "This is %s news" %ag_news_label[predict(input, model, vocab, 2)]

text_file = open("output.txt", "w")
text_file.write(output_str)
text_file.close()