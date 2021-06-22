import random
random.seed(111)


def generate_private_key(gen_order: int) -> int:
    #private_key = int.from_bytes(b'Andrej is cool :P', 'big') # this is how I will do it for reproducibility
    private_key = random.randrange(1, gen_order)
    assert 1 <= private_key < gen_order
    return private_key


if __name__ == '__main__':
    from crypto_identity import bitcoin_gen
    
    key = generate_private_key(gen_order=bitcoin_gen.n)
    print('pvt:', key)