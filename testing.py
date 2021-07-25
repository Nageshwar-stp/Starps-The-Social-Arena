import string, random

private_key_length = 15

private_key_characters = string.ascii_letters + string.digits
private_key = []
for x in range(private_key_length):
    private_key.append(random.choice(private_key_characters))
            
private_key = "".join(private_key)
            
print(private_key)