from hashlib import sha256
import matplotlib.pyplot as plt


def SHA256(text):
    return sha256(text.encode('ascii')).hexdigest()


def mine(block_number, transactions, previous_hash):
    prefix_zeros_effect = dict()
    nonce = 1
    text = str(block_number) + transactions + previous_hash + str(nonce)
    new_hash = SHA256(text)
    for prefix_zeros in range(1, 7):
        count = 1
        while not new_hash.startswith('0' * prefix_zeros):
            print(f'prefix_zeros: {prefix_zeros}, count: {count}')
            count += 1
            nonce += 1
            text = str(block_number) + transactions + previous_hash + str(nonce)
            new_hash = SHA256(text)
        prefix_zeros_effect[prefix_zeros] = count
        count = 1
    return prefix_zeros_effect


if __name__ == '__main__':

    block_number = 5
    transactions = '''
    Bryan->Maria->20,
    Bob->Marcel->40'''
    previous_hash = '69f0fb8cb1d2195340160eb0e4fcf019b4500be11e00fc55f5d3d108b4914d44'

    prefix_zeros_effect = mine(block_number, transactions, previous_hash)
    prefix_zeros_effect_ratios = {k: (v/prefix_zeros_effect[k-1] if k != 1 else 1)
                                  for k, v in prefix_zeros_effect.items()}

    print(prefix_zeros_effect, prefix_zeros_effect_ratios)

    plt.plot(list(prefix_zeros_effect_ratios.keys()), list(prefix_zeros_effect_ratios.values()))
    plt.ylabel('Prefix Zeros | Computing Power')
    plt.show()
