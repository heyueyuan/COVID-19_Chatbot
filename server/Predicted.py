import torch
import torch.nn as nn
from Voc import *
from model import *
import re

MAX_LENGTH = 100
model_name = 'cb_model'
attn_model = 'dot'
#attn_model = 'general'
#attn_model = 'concat'
hidden_size = 500
encoder_n_layers = 2
decoder_n_layers = 2
dropout = 0.1
batch_size = 64

cuda = torch.cuda.is_available()
device = torch.device("cuda" if cuda else "cpu")

corpus_name = 'covid-vocabulary'
voc = Voc(corpus_name)

modelName = '../savedWeight.tar'
model = torch.load(modelName)

encoder_saved = model['en']
decoder_saved = model['de']
encoder_optimizer_saved = model['en_opt']
decoder_optimizer_saved = model['de_opt']
embedding_saved = model['embedding']
voc.__dict__ = model['voc_dict']

embedding = nn.Embedding(voc.num_words, hidden_size)
embedding.load_state_dict(embedding_saved)

encoder = EncoderRNN(hidden_size, embedding, encoder_n_layers, dropout)
decoder = LuongAttnDecoderRNN(attn_model, embedding, hidden_size, voc.num_words, 
				decoder_n_layers, dropout)
encoder.load_state_dict(encoder_saved)
decoder.load_state_dict(decoder_saved)

searcher = GreedySearchDecoder(encoder, decoder)

encoder.eval()
decoder.eval()

def normalize(s):
#     s = unicodeToAscii(s.lower().strip())
    s = s.lower().strip()
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    s = re.sub(r"\s+", r" ", s).strip()
    return s

def indexesFromSentence(voc, sentence):
    return [voc.word2index[word] for word in sentence.split(' ')] + [EOS_token]

def evaluate(encoder, decoder, searcher, voc, sentence, max_length=MAX_LENGTH):
    sentence = normalize(sentence)
    words = []
    indexes_batch = [indexesFromSentence(voc, sentence)]
    lengths = torch.tensor([len(indexes) for indexes in indexes_batch])
    input_batch = torch.LongTensor(indexes_batch).transpose(0, 1)
    input_batch = input_batch.to(device)
    lengths = lengths.to(device)
    tokens, scores = searcher(input_batch, lengths, max_length)
    decoded_words = [voc.index2word[token.item()] for token in tokens]
    for word in decoded_words:
        if word == 'EOS':
            break
        elif word != 'PAD':
            words.append(word)
    words = ' '.join(words)

    return words

def predicted(input_sentence):
    output_words = evaluate(encoder, decoder, searcher, voc, input_sentence)
    return output_words   



