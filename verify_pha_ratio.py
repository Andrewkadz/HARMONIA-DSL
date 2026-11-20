"""Every numeric claim in the 263/97 note. Run to reproduce."""
import math, hashlib, struct
from sympy import isprime

out = []
def say(s=""): out.append(s); print(s)

say("=" * 62); say("1. PRIMALITY AND COPRIMALITY"); say("=" * 62)
say(f"263 prime: {isprime(263)}    97 prime: {isprime(97)}")
say(f"263 + 97 = {263+97}")
say(f"gcd(263, 97)  = {math.gcd(263,97)}")
say(f"gcd(97, 360)  = {math.gcd(97,360)}")
say(f"gcd(263, 360) = {math.gcd(263,360)}")
say(f"360 factors   = 2^3 * 3^2 * 5  -> any prime > 5 is automatically coprime to 360")
say(f"263 = 360 - 97 -> 263 == -97 (mod 360): {263 % 360 == (-97) % 360}")

say(); say("=" * 62); say("2. THE CONSTRAINED SEARCH: primes p+q=360, ranked by |p/q - e|"); say("=" * 62)
pairs = []
for q in range(2, 180):
    p = 360 - q
    if isprime(p) and isprime(q):
        pairs.append((abs(p/q - math.e), p, q))
pairs.sort()
say(f"total prime pairs summing to 360: {len(pairs)}")
for i, (err, p, q) in enumerate(pairs[:5], 1):
    say(f"  {i}. {p:3d}/{q:3d} = {p/q:.6f}   |diff from e| = {err:.6f}")
say(f"winner beats runner-up by {pairs[1][0]/pairs[0][0]:.1f}x")

say(); say("=" * 62); say("3. BEST RATIONAL APPROXIMATIONS TO e (denominator < 100)"); say("=" * 62)
best = None
for q in range(1, 100):
    p = round(math.e * q); err = abs(p/q - math.e)
    if best is None or err < best:
        best = err; say(f"  {p:3d}/{q:2d} = {p/q:.6f}   rel err {err/math.e*100:.4f}%")
say(f"  263/97 = {263/97:.6f}   rel err {abs(263/97-math.e)/math.e*100:.4f}%  <- NOT a convergent")

say(); say("=" * 62); say("4. UOR KERNEL RING Z/256Z"); say("=" * 62)
M = 256
say(f"97  mod 256 = {97%M:3d}  odd -> unit")
say(f"263 mod 256 = {263%M:3d}  odd -> unit")
i97 = pow(97, -1, M)
say(f"97^-1 mod 256 = {i97}   check 97*{i97} mod 256 = {(97*i97)%M}")
r = (263 * i97) % M
say(f"263/97 in Z/256Z = 263 * 97^-1 = {r}")
say(f"round-trip: {r} * 97 mod 256 = {(r*97)%M}  == 263 mod 256 = {263%M}")
for k in (97, 263):
    say(f"additive span of {k} in Z/256Z: {len({(k*i)%M for i in range(M)})} of 256 residues")
say(f"e in Z/256Z: NO REPRESENTATION (not a ratio of units)")

say(); say("=" * 62); say("5. WHICH PROPERTIES SURVIVE WHICH MODULUS"); say("=" * 62)
say("complementarity (97+263 == 0) holds iff modulus divides 360:")
for m in (8, 16, 24, 32, 64, 72, 128, 256, 360):
    say(f"  mod {m:3d}: 360 mod {m:3d} = {360%m:3d}   complementary: {360%m==0}")
say("unit/generator property holds in EVERY Z/2^n (both are odd)")

say(); say("=" * 62); say("6. CONTENT ADDRESSING"); say("=" * 62)
say(f'CID("263/97")        = {hashlib.sha256(b"263/97").hexdigest()}')
for prec, packer in (("float64", "d"), ("float32", "f")):
    b = struct.pack(packer, math.e)
    say(f"CID(e as {prec:7s})  = {hashlib.sha256(b).hexdigest()}")
say("-> one canonical address vs. one address per encoding")

open("verify_output.txt", "w").write("\n".join(out))
