import numpy as np, sys
from scipy.io import wavfile
from scipy.signal import fftconvolve, butter, sosfilt
sr=44100; dur=float(sys.argv[1]); name=sys.argv[2]
N=int(sr*dur); t=np.arange(N)/sr
rng=np.random.default_rng(11)
A=432.0
def hz(semi): return A*2**(semi/12)   # semitones from A4=432
# progression (A=0): A, F#m, D, E  -> I vi IV V ; 4 beats each at 66 bpm, 2 bars per chord
bpm=66; beat=60/bpm; bar=4*beat; chord_len=2*bar
chords=[[-24,-17,-12,-8,-5],[-27,-20,-15,-12,-8],[-31,-24,-19,-15,-12],[-29,-22,-17,-13,-10]]
# A2,E3,A3,C#4,E4 | F#2.. | D2.. | E2..
L=np.zeros(N); R=np.zeros(N)
def add(sig,start,pan=0.5):
    s=int(start*sr); e=min(N,s+len(sig)); 
    if s>=N: return
    L[s:e]+=sig[:e-s]*(1-pan); R[s:e]+=sig[:e-s]*pan
# warm pad per chord, crossfaded
nchords=int(np.ceil(dur/chord_len))+1
for k in range(nchords):
    ch=chords[k%4]; st=k*chord_len; ln=chord_len+2.5
    tt=np.arange(int(ln*sr))/sr
    a=np.minimum(1,tt/1.8)*np.minimum(1,(ln-tt)/2.2)
    sig=np.zeros_like(tt)
    for i,s in enumerate(ch):
        f=hz(s)
        for det in (-0.35,0.35):
            sig+= (0.5/(1+i*0.25))*(np.sin(2*np.pi*(f+det)*tt)+0.25*np.sin(2*np.pi*2*(f+det)*tt)+0.08*np.sin(2*np.pi*3*(f+det)*tt))
    add(0.10*sig*a,st,0.5)
# bell / soft piano note
def bell(f,ln=3.2,vel=1.0):
    tt=np.arange(int(ln*sr))/sr
    e=np.exp(-tt*2.2)*np.minimum(1,tt/0.03)
    s=(np.sin(2*np.pi*f*tt)+0.25*np.sin(2*np.pi*2*f*tt)*np.exp(-tt*4)+0.05*np.sin(2*np.pi*3.01*f*tt)*np.exp(-tt*7))
    return vel*s*e
# gentle arpeggio (eighths) + simple melody on top, A major pentatonic
penta=[0,2,4,7,9]  # A B C# E F#
arp_pat=[0,2,3,4,3,2,1,2]
mel_motifs=[[12,None,9,7,None,4,None,None],[7,None,9,None,12,None,14,None],[9,None,7,4,None,2,None,None],[4,None,7,None,9,None,7,None]]
t0=6.0  # let pad start first
k=0; tcur=t0
while tcur<dur-14:
    ch=chords[k%4]
    tones=[s+24 for s in ch]  # one/two octaves up range
    for bar_i in range(2):
        for j,ix in enumerate(arp_pat):
            if j not in (0,5): continue
            tn=tones[1+ix%4] if ix<4 else tones[4]
            when=tcur+bar_i*bar+j*beat/2
            add(bell(hz(tn-12),2.6,0.25*(0.045+0.01*rng.random())),when,0.35+0.3*rng.random())
        mot=mel_motifs[(k+bar_i)%4]
        root=ch[0]+24+12
        for j,m in enumerate(mot):
            if m is None: continue
            if bar_i==1 or j>2: continue
            when=tcur+bar_i*bar+j*beat/2
            # snap to pentatonic of A
            note=m
            add(bell(hz(note-12),3.6,0.0175),when,0.55)
    tcur+=chord_len; k+=1
mus=np.stack([L,R],1)
# reverb: exponentially decaying stereo noise IR
irl=int(sr*3.2); it=np.arange(irl)/sr
ir=rng.standard_normal((irl,2))*np.exp(-it*1.6)[:,None]; ir[:int(0.02*sr)]*=0.2
sos=butter(2,6000,'low',fs=sr,output='sos'); ir=sosfilt(sos,ir,axis=0); ir/=np.sqrt((ir**2).sum(0))
wet=np.stack([fftconvolve(mus[:,c],ir[:,c])[:N] for c in range(2)],1)
mus=0.7*mus+0.55*wet
mus/=np.abs(mus).max()
# very soft 10 Hz alpha binaural, low carrier (108 = 432/4)
b=np.stack([np.sin(2*np.pi*108*t),np.sin(2*np.pi*118*t)],1)
mix=0.86*mus+0.045*b
f=np.ones(N); fi=int(sr*5); fo=int(sr*14)
f[:fi]=np.linspace(0,1,fi)**2; f[-fo:]=np.linspace(1,0,fo)**1.5
mix*=f[:,None]; mix=mix/np.abs(mix).max()*0.8
wavfile.write(name+'.wav',sr,(mix*32767).astype(np.int16))
