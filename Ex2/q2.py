from q2_atm import ATM, ServerResponse


def extract_PIN(encrypted_PIN) -> int:
    """Extracts the original PIN string from an encrypted PIN."""
    atm = ATM()
    for p in [i for i in range(10**3, 10**4)]:
        if encrypted_PIN == atm.encrypt_PIN(p):
            return p
    return 0


def extract_credit_card(encrypted_credit_card) -> int:
    """Extracts a credit card number string from its ciphertext."""
    # We now need new instance of the encription.
    return round(encrypted_credit_card**(1/float(ATM().rsa_card.e)))


def forge_signature():
    """Forge a server response that passes verification."""
    # Return a ServerResponse instance.
    return ServerResponse(1,1)
