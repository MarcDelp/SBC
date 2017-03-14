rom theano_lstm import Embedding, LSTM, RNN, StackedCells, Layer, create_optimization_updates, masked_loss
celltype=LSTM
self.model = StackedCells(input_size, celltype=celltype, layers =[hidden_size] * stack_size)
# add an embedding
self.model.layers.insert(0, Embedding(chemin_size, input_size))
# add a classifier:
self.model.layers.append(Layer(hidden_size, chemin_size, activation = softmax))

def create_prediction(self, greedy=False):
        def step(idx, *states):
            # new hiddens are the states we need to pass to LSTMs
            # from past. Because the StackedCells also include
            # the embeddings, and those have no state, we pass
            # a "None" instead:
            new_hiddens = [None] + list(states)
            
            new_states = self.model.forward(idx, prev_hiddens = new_hiddens)
            if greedy:
                new_idxes = new_states[-1]
                new_idx   = new_idxes.argmax()
                # provide a stopping condition for greedy search:
                return ([new_idx.astype(self.priming_word.dtype)] + new_states[1:-1]), theano.scan_module.until(T.eq(new_idx,self._stop_word))
            else:
                return new_states[1:]
        # in sequence forecasting scenario we take everything
        # up to the before last step, and predict subsequent
        # steps ergo, 0 ... n - 1, hence:
        inputs = self.input_mat[:, 0:-1]
        num_examples = inputs.shape[0]
        # pass this to Theano's recurrence relation function:
        
        # choose what gets outputted at each timestep:
        if greedy:
            outputs_info = [dict(initial=self.priming_word, taps=[-1])] + [initial_state_with_taps(layer) for layer in self.model.layers[1:-1]]
            result, _ = theano.scan(fn=step,
                                n_steps=200,
                                outputs_info=outputs_info)
        else:
            outputs_info = [initial_state_with_taps(layer, num_examples) for layer in self.model.layers[1:]]
            result, _ = theano.scan(fn=step,
                                sequences=[inputs.T],
                                outputs_info=outputs_info)
                                 
        if greedy:
            return result[0]
        # softmaxes are the last layer of our network,
        # and are at the end of our results list:
        return result[-1].transpose((2,0,1))
        # we reorder the predictions to be:
        # 1. what row / example
        # 2. what timestep
        # 3. softmax dimension

def has_hidden(layer):
    """
    Whether a layer has a trainable
    initial hidden state.
    """
    return hasattr(layer, 'initial_hidden_state')

def matrixify(vector, n):
    return T.repeat(T.shape_padleft(vector), n, axis=0)

def initial_state(layer, dimensions = None):
    """
    Initalizes the recurrence relation with an initial hidden state
    if needed, else replaces with a "None" to tell Theano that
    the network **will** return something, but it does not need
    to send it to the next step of the recurrence
    """
    if dimensions is None:
        return layer.initial_hidden_state if has_hidden(layer) else None
    else:
        return matrixify(layer.initial_hidden_state, dimensions) if has_hidden(layer) else None

def initial_state_with_taps(layer, dimensions = None):
    """Optionally wrap tensor variable into a dict with taps=[-1]"""
    state = initial_state(layer, dimensions)
    if state is not None:
        return dict(initial=state, taps=[-1])
    else:
        return None
	