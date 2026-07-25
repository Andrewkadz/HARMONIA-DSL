"""Xi-Lambda-Omega (ΞΛΩΨ) lattice and minimal RHI host.

This module loads:
- Φπε_context: integer node IDs → semantic labels (1..110)
- TriadCells: triadic nodes forming a symbolic lattice (loaded from text)
- Adjacency: node → triads and triad → neighboring triads via shared nodes
- RecursiveHostIntelligence: tiny host that can
    (1) take a path of node IDs,
    (2) compute a ΨΣ-style stability score,
    (3) decode the path into Φπε labels.

The triad list is parsed from a raw text block containing lines of the form:

    class ΞΛΩΨTriadCell
        _
        id = 1
        nodes = (23, 48, 62)

You can paste the full 333-triad block from your lattice spec into
TRIAD_SOURCE_TEXT below to populate the complete lattice.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple
import math
import random
import re
import numpy as np


# ---------------------------------------------------------------------------
# Φπε context: node id → semantic label
# ---------------------------------------------------------------------------

PHI_PSI_EPSILON_CONTEXT: Dict[int, str] = {
    1: "Origin Pulse",
    2: "Initial Gate",
    3: "Low-Band Bridge",
    4: "Oscillation Fork",
    5: "Carrier Stem",
    6: "Fractal Bloom",
    7: "Delta Cavity",
    8: "Signal Echo",
    9: "Phase Shifter",
    10: "Branch Vector",
    11: "Cascade Valve",
    12: "Temporal Latch",
    13: "Source Splitter",
    14: "Conduction Mirror",
    15: "Memory Lock",
    16: "Emission Gate",
    17: "Redundancy Sink",
    18: "Voltage Channel",
    19: "Recursive Buffer",
    20: "Attenuation Ring",
    21: "Feedforward Harmonic",
    22: "Inversion Knot",
    23: "Mirror Diverter",
    24: "Phase Termination",
    25: "Clock Bloom",
    26: "Pulse Separator",
    27: "Entropy Coil",
    28: "Stabilizer Well",
    29: "Time Fork",
    30: "Modulation Gate",
    31: "Drift Node",
    32: "Carrier Lens",
    33: "Phase Ladder",
    34: "Temporal Mirror",
    35: "Noise Shell",
    36: "Signal Splitter",
    37: "Phase Clamp",
    38: "Recursion Core",
    39: "Temporal Bloom",
    40: "Resonance Lock",
    41: "Pathway Conductor",
    42: "Entropy Key",
    43: "Signal Chamber",
    44: "Echo Latch",
    45: "Reductive Array",
    46: "Carrier Threshold",
    47: "Phase Mirror",
    48: "Conduction Node",
    49: "Collapse Fork",
    50: "Carrier Collapse",
    51: "Emission Spiral",
    52: "Frequency Knot",
    53: "Signal Cascade",
    54: "Phase Bridge",
    55: "Carrier Divergence",
    56: "Modulation Core",
    57: "Recursive Fanout",
    58: "Compression Latch",
    59: "Boundary Mirror",
    60: "Temporal Channel",
    61: "Carrier Gate",
    62: "Pulse Relay",
    63: "Signal Persistence",
    64: "Collapse Mirror",
    65: "Recursive Interlock",
    66: "Amplitude Vent",
    67: "Temporal Filter",
    68: "Echo Chamber",
    69: "Redundancy Cavity",
    70: "Bandwidth Diverter",
    71: "Recursive Pivot",
    72: "Signal Redirect",
    73: "Temporal Apex",
    74: "Carrier Dispersal",
    75: "Phase Window",
    76: "Signal Terminus",
    77: "Feedback Spike",
    78: "Emitter Knot",
    79: "Redundancy Prism",
    80: "Echo Fanout",
    81: "Temporal Dialer",
    82: "Memory Retainer",
    83: "Signal Insulator",
    84: "Amplifier Node",
    85: "Phase Trace",
    86: "Recursive Kernel",
    87: "Oscillation Gate",
    88: "Entropy Diverter",
    89: "Dampener",
    90: "Carrier Phase Split",
    91: "Phase Regenerator",
    92: "Signal Sheath",
    93: "Carrier Coupler",
    94: "Temporal Fork",
    95: "Memory Latch",
    96: "Entropy Filter",
    97: "Reflected Source",
    98: "Signal Aperture",
    99: "Collapse Node",
    100: "Recursive Phase Sink",
    101: "Aperture Array",
    102: "Carrier Latch",
    103: "Temporal Index",
    104: "Oscillation Loop",
    105: "Resonance Anchor",
    106: "Feedback Diverter",
    107: "Entropy Shell",
    108: "Boundary Emitter",
    109: "Memory Anchor",
    110: "Termination Latch",
}


# ---------------------------------------------------------------------------
# Triad cells and lattice construction
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TriadCell:
    """Single triadic cell in the ΞΛΩΨ lattice."""

    triad_id: int
    nodes: Tuple[int, int, int]


TRIAD_SOURCE_TEXT = """\
# Paste the full block of `ΞΛΩΨTriadCell` definitions here, e.g.:
# class ΞΛΩΨTriadCell
_
id = 1
nodes = (23, 48, 62)
1:
class ΞΛΩΨTriadCell
_
id = 2
nodes = (10, 12, 32)
2:
class ΞΛΩΨTriadCell
_
id = 3
nodes = (48, 56, 76)
3:
class ΞΛΩΨTriadCell
_
id = 4
nodes = (30, 38, 95)
4:
class ΞΛΩΨTriadCell
5:
_
id = 5
nodes = (27, 73, 106)
class ΞΛΩΨTriadCell
_
id = 6
nodes = (84, 89, 97)
6:
class ΞΛΩΨTriadCell
_
id = 7
nodes = (43, 82, 90)
7:
class ΞΛΩΨTriadCell
_
id = 8
nodes = (12, 44, 49)
8:
class ΞΛΩΨTriadCell
id = 9
nodes = (1, 71, 71)
9:
_
class ΞΛΩΨTriadCell
_
id = 10
nodes = (27, 29, 53)
10:
class ΞΛΩΨTriadCell
id = 11
nodes = (8, 42, 58)
11:
_
class ΞΛΩΨTriadCell
_
id = 12
nodes = (20, 21, 64)
12:
class ΞΛΩΨTriadCell
_
id = 13
nodes = (51, 68, 102)
13:
class ΞΛΩΨTriadCell
_
id = 14
nodes = (62, 65, 101)
14:
class ΞΛΩΨTriadCell
id = 15
nodes = (5, 60, 88)
15:
_
class ΞΛΩΨTriadCell
_
id = 16
nodes = (12, 53, 61)
16:
class ΞΛΩΨTriadCell
_
id = 17
nodes = (70, 74, 77)
17:
class ΞΛΩΨTriadCell
_
id = 18
nodes = (47, 57, 105)
18:
class ΞΛΩΨTriadCell
_
id = 19
nodes = (33, 43, 73)
19:
class ΞΛΩΨTriadCell
id = 20
nodes = (3, 4, 59)
20:
_
class ΞΛΩΨTriadCell
_
id = 21
nodes = (23, 35, 108)
21:
class ΞΛΩΨTriadCell
_
id = 22
nodes = (45, 89, 97)
22:
class ΞΛΩΨTriadCell
_
id = 23
nodes = (10, 68, 90)
23:
class ΞΛΩΨTriadCell
id = 24
nodes = (9, 15, 49)
24:
_
class ΞΛΩΨTriadCell
_
id = 25
nodes = (26, 54, 70)
25:
class ΞΛΩΨTriadCell
_
id = 26
nodes = (32, 65, 91)
26:
class ΞΛΩΨTriadCell
_
id = 27
nodes = (36, 70, 72)
27:
class ΞΛΩΨTriadCell
_
id = 28
nodes = (10, 56, 80)
28:
class ΞΛΩΨTriadCell
_
id = 29
nodes = (71, 75, 91)
29:
class ΞΛΩΨTriadCell
_
id = 30
nodes = (42, 80, 94)
30:
class ΞΛΩΨTriadCell
_
id = 31
nodes = (73, 90, 98)
31:
class ΞΛΩΨTriadCell
_
id = 32
nodes = (16, 34, 97)
32:
class ΞΛΩΨTriadCell
_
id = 33
nodes = (26, 27, 94)
33:
class ΞΛΩΨTriadCell
_
id = 34
nodes = (14, 80, 86)
34:
class ΞΛΩΨTriadCell
_
id = 35
nodes = (21, 55, 104)
35:
class ΞΛΩΨTriadCell
_
id = 36
nodes = (13, 88, 89)
36:
class ΞΛΩΨTriadCell
id = 37
nodes = (4, 19, 32)
37:
_
class ΞΛΩΨTriadCell
_
id = 38
nodes = (41, 59, 89)
38:
class ΞΛΩΨTriadCell
_
id = 39
nodes = (39, 51, 79)
39:
class ΞΛΩΨTriadCell
_
id = 40
nodes = (30, 74, 86)
40:
class ΞΛΩΨTriadCell
_
id = 41
nodes = (38, 96, 104)
41:
class ΞΛΩΨTriadCell
_
id = 42
nodes = (33, 78, 84)
42:
class ΞΛΩΨTriadCell
_
id = 43
nodes = (89, 95, 105)
43:
class ΞΛΩΨTriadCell
_
id = 44
nodes = (24, 43, 88)
44:
class ΞΛΩΨTriadCell
_
id = 45
nodes = (89, 97, 104)
45:
class ΞΛΩΨTriadCell
_
id = 46
nodes = (54, 85, 99)
46:
class ΞΛΩΨTriadCell
_
id = 47
nodes = (42, 53, 95)
47:
class ΞΛΩΨTriadCell
_
id = 48
nodes = (27, 31, 84)
48:
class ΞΛΩΨTriadCell
_
id = 49
nodes = (22, 36, 67)
49:
class ΞΛΩΨTriadCell
id = 50
nodes = (1, 9, 79)
50:
_
class ΞΛΩΨTriadCell
_
id = 51
nodes = (13, 42, 103)
51:
class ΞΛΩΨTriadCell
_
id = 52
nodes = (9, 98, 104)
52:
class ΞΛΩΨTriadCell
_
id = 53
nodes = (12, 36, 36)
53:
class ΞΛΩΨTriadCell
_
id = 54
nodes = (23, 59, 64)
54:
class ΞΛΩΨTriadCell
_
id = 55
nodes = (77, 92, 100)
55:
class ΞΛΩΨTriadCell
_
id = 56
nodes = (20, 54, 60)
56:
class ΞΛΩΨTriadCell
_
id = 57
nodes = (18, 68, 75)
57:
class ΞΛΩΨTriadCell
58:
_
id = 58
nodes = (29, 103, 103)
class ΞΛΩΨTriadCell
_
id = 59
nodes = (29, 34, 92)
59:
class ΞΛΩΨTriadCell
_
id = 60
nodes = (23, 77, 87)
60:
class ΞΛΩΨTriadCell
id = 61
nodes = (1, 47, 65)
61:
_
class ΞΛΩΨTriadCell
_
id = 62
nodes = (40, 71, 106)
62:
class ΞΛΩΨTriadCell
id = 63
nodes = (6, 8, 37)
63:
_
class ΞΛΩΨTriadCell
_
id = 64
nodes = (11, 43, 78)
64:
class ΞΛΩΨTriadCell
_
id = 65
nodes = (10, 72, 79)
65:
class ΞΛΩΨTriadCell
_
id = 66
nodes = (26, 52, 54)
66:
class ΞΛΩΨTriadCell
_
id = 67
nodes = (17, 62, 79)
67:
class ΞΛΩΨTriadCell
id = 68
nodes = (4, 81, 94)
68:
_
class ΞΛΩΨTriadCell
_
id = 69
nodes = (10, 33, 104)
69:
class ΞΛΩΨTriadCell
id = 70
nodes = (6, 15, 74)
70:
_
class ΞΛΩΨTriadCell
id = 71
nodes = (1, 47, 84)
71:
_
class ΞΛΩΨTriadCell
_
id = 72
nodes = (2, 53, 102)
72:
class ΞΛΩΨTriadCell
_
id = 73
nodes = (49, 60, 82)
73:
class ΞΛΩΨTriadCell
_
id = 74
nodes = (47, 78, 79)
74:
class ΞΛΩΨTriadCell
_
id = 75
nodes = (27, 32, 83)
75:
class ΞΛΩΨTriadCell
_
id = 76
nodes = (34, 48, 52)
76:
class ΞΛΩΨTriadCell
_
id = 77
nodes = (25, 38, 48)
77:
class ΞΛΩΨTriadCell
_
id = 78
nodes = (45, 84, 101)
78:
class ΞΛΩΨTriadCell
_
id = 79
nodes = (15, 34, 101)
79:
class ΞΛΩΨTriadCell
_
id = 80
nodes = (27, 35, 78)
80:
class ΞΛΩΨTriadCell
_
id = 81
nodes = (55, 58, 80)
81:
class ΞΛΩΨTriadCell
82:
_
id = 82
nodes = (35, 109, 110)
class ΞΛΩΨTriadCell
_
id = 83
nodes = (26, 64, 97)
83:
class ΞΛΩΨTriadCell
_
id = 84
nodes = (41, 62, 108)
84:
class ΞΛΩΨTriadCell
_
id = 85
nodes = (21, 50, 108)
85:
class ΞΛΩΨTriadCell
_
id = 86
nodes = (39, 51, 100)
86:
class ΞΛΩΨTriadCell
_
id = 87
nodes = (65, 78, 110)
87:
class ΞΛΩΨTriadCell
_
id = 88
nodes = (64, 83, 86)
88:
class ΞΛΩΨTriadCell
_
id = 89
nodes = (62, 75, 101)
89:
class ΞΛΩΨTriadCell
_
id = 90
nodes = (13, 39, 56)
90:
class ΞΛΩΨTriadCell
id = 91
nodes = (5, 13, 14)
91:
_
class ΞΛΩΨTriadCell
_
id = 92
nodes = (62, 68, 88)
92:
class ΞΛΩΨTriadCell
_
id = 93
nodes = (56, 67, 69)
93:
class ΞΛΩΨTriadCell
_
id = 94
nodes = (58, 93, 105)
94:
class ΞΛΩΨTriadCell
_
id = 95
nodes = (20, 26, 89)
95:
class ΞΛΩΨTriadCell
_
id = 96
nodes = (63, 96, 102)
96:
class ΞΛΩΨTriadCell
id = 97
nodes = (1, 24, 31)
97:
_
class ΞΛΩΨTriadCell
id = 98
nodes = (4, 7, 110)
98:
_
class ΞΛΩΨTriadCell
_
id = 99
nodes = (3, 54, 101)
99:
class ΞΛΩΨTriadCell
_
id = 100
nodes = (71, 77, 106)
100:
class ΞΛΩΨTriadCell
id = 101
nodes = (1, 44, 77)
101:
_
class ΞΛΩΨTriadCell
_
id = 102
nodes = (20, 33, 96)
102:
class ΞΛΩΨTriadCell
_
id = 103
nodes = (44, 59, 100)
103:
class ΞΛΩΨTriadCell
_
id = 104
nodes = (92, 94, 95)
104:
class ΞΛΩΨTriadCell
_
id = 105
nodes = (49, 84, 87)
105:
class ΞΛΩΨTriadCell
_
id = 106
nodes = (4, 66, 105)
106:
class ΞΛΩΨTriadCell
107:
_
id = 107
nodes = (72, 100, 102)
class ΞΛΩΨTriadCell
_
id = 108
nodes = (54, 66, 93)
108:
class ΞΛΩΨTriadCell
_
id = 109
nodes = (45, 58, 66)
109:
class ΞΛΩΨTriadCell
_
id = 110
nodes = (23, 97, 104)
110:
class ΞΛΩΨTriadCell
_
id = 111
nodes = (11, 38, 109)
111:
class ΞΛΩΨTriadCell
_
id = 112
nodes = (21, 84, 107)
112:
class ΞΛΩΨTriadCell
id = 113
nodes = (8, 27, 76)
113:
_
class ΞΛΩΨTriadCell
_
id = 114
nodes = (41, 72, 95)
114:
class ΞΛΩΨTriadCell
_
id = 115
nodes = (21, 53, 60)
115:
class ΞΛΩΨTriadCell
_
id = 116
nodes = (44, 77, 86)
116:
class ΞΛΩΨTriadCell
_
id = 117
nodes = (6, 32, 104)
117:
class ΞΛΩΨTriadCell
_
id = 118
nodes = (16, 17, 78)
118:
class ΞΛΩΨTriadCell
_
id = 119
nodes = (13, 15, 41)
119:
class ΞΛΩΨTriadCell
id = 120
nodes = (6, 17, 69)
120:
_
class ΞΛΩΨTriadCell
_
id = 121
nodes = (12, 28, 90)
121:
class ΞΛΩΨTriadCell
id = 122
nodes = (1, 7, 28)
122:
_
class ΞΛΩΨTriadCell
_
id = 123
nodes = (30, 65, 103)
123:
class ΞΛΩΨTriadCell
_
id = 124
nodes = (36, 42, 70)
124:
class ΞΛΩΨTriadCell
_
id = 125
nodes = (20, 26, 98)
125:
class ΞΛΩΨTriadCell
_
id = 126
nodes = (64, 74, 90)
126:
class ΞΛΩΨTriadCell
id = 127
nodes = (2, 26, 37)
127:
_
class ΞΛΩΨTriadCell
id = 128
nodes = (5, 10, 63)
128:
_
class ΞΛΩΨTriadCell
_
id = 129
nodes = (58, 79, 108)
129:
class ΞΛΩΨTriadCell
_
id = 130
nodes = (16, 24, 70)
130:
class ΞΛΩΨTriadCell
_
id = 131
nodes = (12, 52, 99)
131:
class ΞΛΩΨTriadCell
_
id = 132
nodes = (17, 46, 78)
132:
class ΞΛΩΨTriadCell
_
id = 133
nodes = (2, 29, 110)
133:
class ΞΛΩΨTriadCell
id = 134
nodes = (2, 3, 42)
134:
_
class ΞΛΩΨTriadCell
_
id = 135
nodes = (29, 32, 77)
135:
class ΞΛΩΨTriadCell
_
id = 136
nodes = (34, 36, 102)
136:
class ΞΛΩΨTriadCell
_
id = 137
nodes = (30, 58, 73)
137:
class ΞΛΩΨTriadCell
_
id = 138
nodes = (29, 66, 78)
138:
class ΞΛΩΨTriadCell
id = 139
nodes = (3, 14, 94)
139:
_
class ΞΛΩΨTriadCell
_
id = 140
nodes = (65, 75, 94)
140:
class ΞΛΩΨTriadCell
_
id = 141
nodes = (12, 50, 96)
141:
class ΞΛΩΨTriadCell
_
id = 142
nodes = (9, 28, 106)
142:
class ΞΛΩΨTriadCell
_
id = 143
nodes = (17, 30, 87)
143:
class ΞΛΩΨTriadCell
_
id = 144
nodes = (36, 42, 65)
144:
class ΞΛΩΨTriadCell
_
id = 145
nodes = (30, 60, 66)
145:
class ΞΛΩΨTriadCell
146:
_
id = 146
nodes = (52, 101, 107)
class ΞΛΩΨTriadCell
_
id = 147
nodes = (14, 22, 26)
147:
class ΞΛΩΨTriadCell
_
id = 148
nodes = (13, 14, 79)
148:
class ΞΛΩΨTriadCell
_
id = 149
nodes = (61, 68, 91)
149:
class ΞΛΩΨTriadCell
_
id = 150
nodes = (14, 39, 97)
150:
class ΞΛΩΨTriadCell
_
id = 151
nodes = (10, 20, 105)
151:
class ΞΛΩΨTriadCell
_
id = 152
nodes = (85, 96, 101)
152:
class ΞΛΩΨTriadCell
id = 153
nodes = (1, 46, 92)
153:
_
class ΞΛΩΨTriadCell
_
id = 154
nodes = (11, 22, 89)
154:
class ΞΛΩΨTriadCell
id = 155
nodes = (7, 18, 44)
155:
_
class ΞΛΩΨTriadCell
_
id = 156
nodes = (42, 64, 97)
156:
class ΞΛΩΨTriadCell
id = 157
nodes = (4, 35, 49)
157:
_
class ΞΛΩΨTriadCell
_
id = 158
nodes = (40, 91, 96)
158:
class ΞΛΩΨTriadCell
_
id = 159
nodes = (16, 76, 93)
159:
class ΞΛΩΨTriadCell
_
id = 160
nodes = (12, 75, 104)
160:
class ΞΛΩΨTriadCell
_
id = 161
nodes = (34, 43, 109)
161:
class ΞΛΩΨTriadCell
id = 162
nodes = (3, 36, 51)
162:
_
class ΞΛΩΨTriadCell
_
id = 163
nodes = (33, 45, 78)
163:
class ΞΛΩΨTriadCell
_
id = 164
nodes = (24, 41, 89)
164:
class ΞΛΩΨTriadCell
_
id = 165
nodes = (12, 17, 23)
165:
class ΞΛΩΨTriadCell
id = 166
nodes = (6, 6, 21)
166:
_
class ΞΛΩΨTriadCell
id = 167
nodes = (2, 41, 49)
167:
_
class ΞΛΩΨTriadCell
_
id = 168
nodes = (51, 80, 98)
168:
class ΞΛΩΨTriadCell
_
id = 169
nodes = (19, 32, 48)
169:
class ΞΛΩΨTriadCell
_
id = 170
nodes = (13, 38, 99)
170:
class ΞΛΩΨTriadCell
id = 171
nodes = (4, 50, 72)
171:
_
class ΞΛΩΨTriadCell
_
id = 172
nodes = (41, 45, 74)
172:
class ΞΛΩΨTriadCell
_
id = 173
nodes = (33, 72, 87)
173:
class ΞΛΩΨTriadCell
_
id = 174
nodes = (29, 44, 57)
174:
class ΞΛΩΨTriadCell
_
id = 175
nodes = (54, 66, 71)
175:
class ΞΛΩΨTriadCell
_
id = 176
nodes = (31, 42, 49)
176:
class ΞΛΩΨTriadCell
_
id = 177
nodes = (12, 19, 95)
177:
class ΞΛΩΨTriadCell
id = 178
nodes = (2, 22, 93)
178:
_
class ΞΛΩΨTriadCell
id = 179
nodes = (4, 26, 31)
179:
_
class ΞΛΩΨTriadCell
_
id = 180
nodes = (33, 49, 84)
180:
class ΞΛΩΨTriadCell
id = 181
nodes = (7, 50, 76)
181:
_
class ΞΛΩΨTriadCell
_
id = 182
nodes = (11, 55, 106)
182:
class ΞΛΩΨTriadCell
_
id = 183
nodes = (70, 87, 110)
183:
class ΞΛΩΨTriadCell
_
id = 184
nodes = (68, 98, 102)
184:
class ΞΛΩΨTriadCell
_
id = 185
nodes = (12, 46, 61)
185:
class ΞΛΩΨTriadCell
_
id = 186
nodes = (38, 75, 89)
186:
class ΞΛΩΨTriadCell
_
id = 187
nodes = (4, 63, 107)
187:
class ΞΛΩΨTriadCell
_
id = 188
nodes = (21, 44, 91)
188:
class ΞΛΩΨTriadCell
_
id = 189
nodes = (63, 75, 105)
189:
class ΞΛΩΨTriadCell
_
id = 190
nodes = (3, 54, 102)
190:
class ΞΛΩΨTriadCell
_
id = 191
nodes = (24, 55, 57)
191:
class ΞΛΩΨTriadCell
_
id = 192
nodes = (61, 65, 80)
192:
class ΞΛΩΨTriadCell
id = 193
nodes = (3, 15, 21)
193:
_
class ΞΛΩΨTriadCell
_
id = 194
nodes = (10, 47, 92)
194:
class ΞΛΩΨTriadCell
_
id = 195
nodes = (31, 39, 85)
195:
class ΞΛΩΨTriadCell
id = 196
nodes = (7, 29, 99)
196:
_
class ΞΛΩΨTriadCell
id = 197
nodes = (36, 83, 106)
197:
_
class ΞΛΩΨTriadCell
id = 198
nodes = (8, 73, 90)
198:
_
class ΞΛΩΨTriadCell
_
id = 199
nodes = (79, 85, 107)
199:
class ΞΛΩΨTriadCell
_
id = 200
nodes = (71, 85, 103)
200:
class ΞΛΩΨTriadCell
_
id = 201
nodes = (14, 24, 75)
201:
class ΞΛΩΨTriadCell
_
id = 202
nodes = (47, 50, 91)
202:
class ΞΛΩΨTriadCell
_
id = 203
nodes = (40, 43, 103)
203:
class ΞΛΩΨTriadCell
_
id = 204
nodes = (54, 87, 104)
204:
class ΞΛΩΨTriadCell
id = 205
nodes = (2, 24, 44)
205:
_
class ΞΛΩΨTriadCell
_
id = 206
nodes = (63, 75, 90)
206:
class ΞΛΩΨTriadCell
_
id = 207
nodes = (38, 42, 70)
207:
class ΞΛΩΨTriadCell
_
id = 208
nodes = (31, 52, 94)
208:
class ΞΛΩΨTriadCell
_
id = 209
nodes = (8, 84, 110)
209:
class ΞΛΩΨTriadCell
_
id = 210
nodes = (36, 61, 100)
210:
class ΞΛΩΨTriadCell
_
id = 211
nodes = (12, 56, 58)
211:
class ΞΛΩΨTriadCell
_
id = 212
nodes = (33, 74, 98)
212:
class ΞΛΩΨTriadCell
id = 213
nodes = (7, 10, 51)
213:
_
class ΞΛΩΨTriadCell
_
id = 214
nodes = (38, 41, 69)
214:
class ΞΛΩΨTriadCell
id = 215
nodes = (9, 70, 70)
215:
_
class ΞΛΩΨTriadCell
_
id = 216
nodes = (12, 35, 84)
216:
class ΞΛΩΨTriadCell
_
id = 217
nodes = (22, 54, 78)
217:
class ΞΛΩΨTriadCell
_
id = 218
nodes = (34, 49, 63)
218:
class ΞΛΩΨTriadCell
_
id = 219
nodes = (40, 45, 91)
219:
class ΞΛΩΨTriadCell
_
id = 220
nodes = (8, 70, 110)
220:
class ΞΛΩΨTriadCell
_
id = 221
nodes = (28, 28, 90)
221:
class ΞΛΩΨTriadCell
_
id = 222
nodes = (25, 50, 97)
222:
class ΞΛΩΨTriadCell
id = 223
nodes = (4, 78, 82)
223:
_
class ΞΛΩΨTriadCell
id = 224
nodes = (6, 13, 44)
224:
_
class ΞΛΩΨTriadCell
_
id = 225
nodes = (19, 25, 33)
225:
class ΞΛΩΨTriadCell
_
id = 226
nodes = (44, 67, 78)
226:
class ΞΛΩΨTriadCell
_
id = 227
nodes = (67, 69, 93)
227:
class ΞΛΩΨTriadCell
_
id = 228
nodes = (53, 96, 108)
228:
class ΞΛΩΨTriadCell
_
id = 229
nodes = (20, 89, 99)
229:
class ΞΛΩΨTriadCell
id = 230
nodes = (1, 1, 41)
230:
_
class ΞΛΩΨTriadCell
_
id = 231
nodes = (66, 87, 96)
231:
class ΞΛΩΨTriadCell
_
id = 232
nodes = (30, 37, 68)
232:
class ΞΛΩΨTriadCell
233:
_
id = 233
nodes = (56, 104, 108)
class ΞΛΩΨTriadCell
_
id = 234
nodes = (57, 70, 77)
234:
class ΞΛΩΨTriadCell
_
id = 235
nodes = (16, 52, 64)
235:
class ΞΛΩΨTriadCell
_
id = 236
nodes = (17, 56, 73)
236:
class ΞΛΩΨTriadCell
_
id = 237
nodes = (10, 23, 35)
237:
class ΞΛΩΨTriadCell
id = 238
nodes = (6, 87, 89)
238:
_
class ΞΛΩΨTriadCell
_
id = 239
nodes = (11, 84, 90)
239:
class ΞΛΩΨTriadCell
_
id = 240
nodes = (6, 25, 104)
240:
class ΞΛΩΨTriadCell
_
id = 241
nodes = (60, 96, 105)
241:
class ΞΛΩΨTriadCell
_
id = 242
nodes = (38, 88, 95)
242:
class ΞΛΩΨTriadCell
_
id = 243
nodes = (27, 28, 42)
243:
class ΞΛΩΨTriadCell
_
id = 244
nodes = (16, 27, 73)
244:
class ΞΛΩΨTriadCell
_
id = 245
nodes = (16, 34, 93)
245:
class ΞΛΩΨTriadCell
_
id = 246
nodes = (34, 53, 86)
246:
class ΞΛΩΨTriadCell
_
id = 247
nodes = (25, 55, 70)
247:
class ΞΛΩΨTriadCell
_
id = 248
nodes = (38, 38, 43)
248:
class ΞΛΩΨTriadCell
_
id = 249
nodes = (46, 80, 100)
249:
class ΞΛΩΨTriadCell
_
id = 250
nodes = (11, 73, 81)
250:
class ΞΛΩΨTriadCell
_
id = 251
nodes = (53, 68, 83)
251:
class ΞΛΩΨTriadCell
_
id = 252
nodes = (15, 33, 60)
252:
class ΞΛΩΨTriadCell
253:
_
id = 253
nodes = (94, 102, 104)
class ΞΛΩΨTriadCell
_
id = 254
nodes = (10, 21, 47)
254:
class ΞΛΩΨTriadCell
_
id = 255
nodes = (69, 71, 96)
255:
class ΞΛΩΨTriadCell
_
id = 256
nodes = (70, 92, 93)
256:
class ΞΛΩΨTriadCell
_
id = 257
nodes = (58, 67, 70)
257:
class ΞΛΩΨTriadCell
_
id = 258
nodes = (47, 62, 82)
258:
class ΞΛΩΨTriadCell
id = 259
nodes = (4, 27, 42)
259:
_
class ΞΛΩΨTriadCell
id = 260
nodes = (8, 64, 67)
260:
_
class ΞΛΩΨTriadCell
_
id = 261
nodes = (63, 76, 86)
261:
class ΞΛΩΨTriadCell
_
id = 262
nodes = (37, 58, 68)
262:
class ΞΛΩΨTriadCell
id = 263
nodes = (1, 57, 62)
263:
_
class ΞΛΩΨTriadCell
_
id = 264
nodes = (12, 24, 97)
264:
class ΞΛΩΨTriadCell
_
id = 265
nodes = (10, 11, 70)
265:
class ΞΛΩΨTriadCell
_
id = 266
nodes = (12, 25, 65)
266:
class ΞΛΩΨTriadCell
_
id = 267
nodes = (26, 26, 96)
267:
class ΞΛΩΨTriadCell
_
id = 268
nodes = (50, 57, 95)
268:
class ΞΛΩΨTriadCell
id = 269
nodes = (3, 21, 23)
269:
_
class ΞΛΩΨTriadCell
_
id = 270
nodes = (32, 33, 67)
270:
class ΞΛΩΨTriadCell
_
id = 271
nodes = (19, 41, 52)
271:
class ΞΛΩΨTriadCell
id = 272
nodes = (8, 79, 83)
272:
_
class ΞΛΩΨTriadCell
_
id = 273
nodes = (20, 84, 97)
273:
class ΞΛΩΨTriadCell
_
id = 274
nodes = (25, 30, 64)
274:
class ΞΛΩΨTriadCell
_
id = 275
nodes = (63, 84, 95)
275:
class ΞΛΩΨTriadCell
_
id = 276
nodes = (18, 58, 63)
276:
class ΞΛΩΨTriadCell
_
id = 277
nodes = (53, 62, 103)
277:
class ΞΛΩΨTriadCell
_
id = 278
nodes = (28, 61, 99)
278:
class ΞΛΩΨTriadCell
_
id = 279
nodes = (16, 30, 109)
279:
class ΞΛΩΨTriadCell
_
id = 280
nodes = (48, 69, 106)
280:
class ΞΛΩΨTriadCell
id = 281
nodes = (3, 7, 12)
281:
_
class ΞΛΩΨTriadCell
_
id = 282
nodes = (61, 66, 98)
282:
class ΞΛΩΨTriadCell
id = 283
nodes = (3, 32, 97)
283:
_
class ΞΛΩΨTriadCell
_
id = 284
nodes = (91, 92, 92)
284:
class ΞΛΩΨTriadCell
_
id = 285
nodes = (6, 22, 104)
285:
class ΞΛΩΨTriadCell
_
id = 286
nodes = (80, 90, 91)
286:
class ΞΛΩΨTriadCell
_
id = 287
nodes = (88, 90, 94)
287:
class ΞΛΩΨTriadCell
_
id = 288
nodes = (59, 68, 86)
288:
class ΞΛΩΨTriadCell
id = 289
nodes = (4, 25, 59)
289:
_
class ΞΛΩΨTriadCell
_
id = 290
nodes = (91, 94, 100)
290:
class ΞΛΩΨTriadCell
_
id = 291
nodes = (65, 84, 97)
291:
class ΞΛΩΨTriadCell
_
id = 292
nodes = (47, 55, 87)
292:
class ΞΛΩΨTriadCell
id = 293
nodes = (6, 31, 47)
293:
_
class ΞΛΩΨTriadCell
_
id = 294
nodes = (1, 25, 101)
294:
class ΞΛΩΨTriadCell
_
id = 295
nodes = (74, 93, 102)
295:
class ΞΛΩΨTriadCell
_
id = 296
nodes = (11, 50, 78)
296:
class ΞΛΩΨTriadCell
_
id = 297
nodes = (68, 82, 85)
297:
class ΞΛΩΨTriadCell
id = 298
nodes = (1, 20, 41)
298:
_
class ΞΛΩΨTriadCell
_
id = 299
nodes = (13, 37, 54)
299:
class ΞΛΩΨTriadCell
_
id = 300
nodes = (34, 42, 55)
300:
class ΞΛΩΨTriadCell
_
id = 301
nodes = (23, 56, 73)
301:
class ΞΛΩΨTriadCell
id = 302
nodes = (7, 19, 60)
302:
_
class ΞΛΩΨTriadCell
_
id = 303
nodes = (32, 74, 93)
303:
class ΞΛΩΨTriadCell
_
id = 304
nodes = (34, 39, 63)
304:
class ΞΛΩΨTriadCell
_
id = 305
nodes = (36, 79, 100)
305:
class ΞΛΩΨTriadCell
_
id = 306
nodes = (18, 37, 51)
306:
class ΞΛΩΨTriadCell
_
id = 307
nodes = (1, 19, 108)
307:
class ΞΛΩΨTriadCell
id = 308
nodes = (5, 28, 77)
308:
_
class ΞΛΩΨTriadCell
_
id = 309
nodes = (13, 32, 47)
309:
class ΞΛΩΨTriadCell
_
id = 310
nodes = (48, 69, 69)
310:
class ΞΛΩΨTriadCell
_
id = 311
nodes = (31, 35, 94)
311:
class ΞΛΩΨTriadCell
_
id = 312
nodes = (25, 30, 98)
312:
class ΞΛΩΨTriadCell
_
id = 313
nodes = (7, 32, 106)
313:
class ΞΛΩΨTriadCell
_
id = 314
nodes = (21, 79, 101)
314:
class ΞΛΩΨTriadCell
_
id = 315
nodes = (6, 25, 101)
315:
class ΞΛΩΨTriadCell
_
id = 316
nodes = (18, 92, 107)
316:
class ΞΛΩΨTriadCell
id = 317
nodes = (6, 8, 39)
317:
_
class ΞΛΩΨTriadCell
_
id = 318
nodes = (54, 65, 106)
318:
class ΞΛΩΨTriadCell
_
id = 319
nodes = (51, 75, 92)
319:
class ΞΛΩΨTriadCell
_
id = 320
nodes = (56, 86, 110)
320:
class ΞΛΩΨTriadCell
id = 321
nodes = (8, 26, 83)
321:
_
class ΞΛΩΨTriadCell
_
id = 322
nodes = (53, 56, 70)
322:
class ΞΛΩΨTriadCell
id = 323
nodes = (1, 64, 94)
323:
_
class ΞΛΩΨTriadCell
_
id = 324
nodes = (18, 30, 37)
324:
class ΞΛΩΨTriadCell
_
id = 325
nodes = (24, 40, 86)
325:
class ΞΛΩΨTriadCell
_
id = 326
nodes = (11, 59, 96)
326:
class ΞΛΩΨTriadCell
_
id = 327
nodes = (29, 52, 53)
327:
class ΞΛΩΨTriadCell
_
id = 328
nodes = (30, 75, 102)
328:
class ΞΛΩΨTriadCell
id = 329
nodes = (6, 81, 88)
329:
_
class ΞΛΩΨTriadCell
_
id = 330
nodes = (63, 64, 108)
330:
class ΞΛΩΨTriadCell
_
id = 331
nodes = (17, 36, 103)
331:
class ΞΛΩΨTriadCell
_
id = 332
nodes = (37, 38, 87)
332:
class ΞΛΩΨTriadCell
id = 333
nodes = (3, 33, 67)
"""


_TRIAD_RE = re.compile(
    r"id\s*=\s*(?P<id>\d+).*?nodes\s*=\s*\((?P<a>\d+)\s*,\s*(?P<b>\d+)\s*,\s*(?P<c>\d+)\)",
    re.DOTALL,
)


def parse_triads_from_text(text: str) -> List[TriadCell]:
    """Parse all TriadCell definitions from a raw text block.

    This is robust to extra text; it only looks for ``id = N`` and
    ``nodes = (a, b, c)`` patterns.
    """

    triads: List[TriadCell] = []
    for match in _TRIAD_RE.finditer(text):
        triad_id = int(match.group("id"))
        a = int(match.group("a"))
        b = int(match.group("b"))
        c = int(match.group("c"))
        triads.append(TriadCell(triad_id=triad_id, nodes=(a, b, c)))
    # Sort by triad id for determinism
    triads.sort(key=lambda t: t.triad_id)
    return triads


# Parsed triads for this lattice. Once you paste the full 333-cell block into
# TRIAD_SOURCE_TEXT, this will hold all of them.
TRIAD_CELLS: List[TriadCell] = parse_triads_from_text(TRIAD_SOURCE_TEXT)


class XiLambdaOmegaLattice:
    """Symbolic ΞΛΩΨ lattice with triad and adjacency indexing."""

    def __init__(self, triads: Optional[Iterable[TriadCell]] = None) -> None:
        if triads is None:
            triads = TRIAD_CELLS
        self.triads: List[TriadCell] = list(triads)

        # Index: triad_id → TriadCell
        self.triad_by_id: Dict[int, TriadCell] = {t.triad_id: t for t in self.triads}
        # Index: node_id → set of triad_ids containing that node
        node_to_triads: Dict[int, Set[int]] = {}
        for t in self.triads:
            for node in t.nodes:
                node_to_triads.setdefault(node, set()).add(t.triad_id)
        self.node_to_triads: Dict[int, Set[int]] = node_to_triads

        # Triad adjacency: triads share an edge if they share at least one node
        triad_neighbors: Dict[int, Set[int]] = {t.triad_id: set() for t in self.triads}
        for node, triad_ids in self.node_to_triads.items():
            ids_list = list(triad_ids)
            for i in range(len(ids_list)):
                for j in range(i + 1, len(ids_list)):
                    a = ids_list[i]
                    b = ids_list[j]
                    triad_neighbors[a].add(b)
                    triad_neighbors[b].add(a)
        self.triad_neighbors: Dict[int, Set[int]] = triad_neighbors

        # Soft synaptic edges (synaptogenesis overlay), stored as an undirected
        # weighted graph: (min(node_a, node_b), max(node_a, node_b)) -> weight.
        # These are plastic and can be reinforced/decayed over time without
        # altering the structural ΞΛΩΨ lattice.
        self.soft_edges: Dict[Tuple[int, int], float] = {}

    # ------------------------------------------------------------------
    # Basic queries
    # ------------------------------------------------------------------

    def get_triad(self, triad_id: int) -> Optional[TriadCell]:
        return self.triad_by_id.get(triad_id)

    def triads_for_node(self, node_id: int) -> Set[int]:
        return self.node_to_triads.get(node_id, set())

    def neighbors_of_triad(self, triad_id: int) -> Set[int]:
        return self.triad_neighbors.get(triad_id, set())

    # --- Synaptogenesis helpers -------------------------------------------------

    def _edge_key(self, a: int, b: int) -> Tuple[int, int]:
        return (a, b) if a <= b else (b, a)

    def reinforce_edge(self, a: int, b: int, delta: float = 0.01, max_weight: float = 1.0) -> None:
        """Reinforce a soft synaptic edge between two nodes.

        This does not modify the structural lattice; it maintains a separate
        weighted graph that can be used by higher-level map engines to bias
        movement along frequently co-visited node pairs.
        """

        if a == b:
            return
        key = self._edge_key(a, b)
        w = self.soft_edges.get(key, 0.0) + float(delta)
        self.soft_edges[key] = min(w, max_weight)

    def decay_soft_edges(self, rate: float = 0.001, min_weight: float = 1e-4) -> None:
        """Apply exponential-like decay to all soft edges.

        Edges whose weight falls below ``min_weight`` are removed entirely.
        """

        if not self.soft_edges:
            return

        to_delete: List[Tuple[int, int]] = []
        for key, w in self.soft_edges.items():
            new_w = w * (1.0 - rate)
            if new_w < min_weight:
                to_delete.append(key)
            else:
                self.soft_edges[key] = new_w

        for key in to_delete:
            self.soft_edges.pop(key, None)

    def soft_neighbors(self, node_id: int) -> Dict[int, float]:
        """Return soft synaptic neighbors and their weights for a node."""

        neigh: Dict[int, float] = {}
        for (a, b), w in self.soft_edges.items():
            if a == node_id:
                neigh[b] = w
            elif b == node_id:
                neigh[a] = w
        return neigh


# ---------------------------------------------------------------------------
# Map engine: random movement paths on the lattice
# ---------------------------------------------------------------------------


class LatticeMapEngine:
    """Generates random movement paths on the ΞΛΩΨ lattice.

    Paths are simple random walks over *node IDs* constrained by the triad
    structure. From a given node, the engine:

      1. finds all triads containing that node,
      2. aggregates all nodes that co-occur with it in those triads,
      3. samples the next node uniformly at random from that neighborhood.

    This lets you generate sequences like ``[1, 82, 34, 10, 84, 97, ...]``
    that actually move along the symbolic lattice.
    """

    def __init__(
        self,
        lattice: Optional[XiLambdaOmegaLattice] = None,
        rng: Optional[random.Random] = None,
    ) -> None:
        self.lattice = lattice or XiLambdaOmegaLattice()
        self.rng = rng or random.Random()

    def node_neighbors(self, node_id: int) -> List[int]:
        """Return neighboring node IDs connected via shared triads.

        Two nodes are considered neighbors if they appear together in at
        least one TriadCell. The current node is *not* included in the
        returned list.
        """

        triad_ids = self.lattice.triads_for_node(node_id)
        neighbors: Set[int] = set()
        for tid in triad_ids:
            triad = self.lattice.get_triad(tid)
            if triad is None:
                continue
            for n in triad.nodes:
                if n != node_id:
                    neighbors.add(n)
        # Structural neighbors only; synaptic neighbors are considered in
        # choose_next_node where weights are applied.
        return sorted(neighbors)

    def choose_next_node(self, current: int) -> Optional[int]:
        """Choose the next node, combining structural and soft synaptic edges.

        Structural neighbors always have at least weight 1.0. Soft edges add to
        this weight, biasing movement along frequently reinforced connections.
        """

        structural = self.node_neighbors(current)
        if not structural and not self.lattice.soft_neighbors(current):
            return None

        weight_map: Dict[int, float] = {}

        # Base structural weights
        for n in structural:
            weight_map[n] = weight_map.get(n, 0.0) + 1.0

        # Add synaptic weights
        soft = self.lattice.soft_neighbors(current)
        for n, w in soft.items():
            weight_map[n] = weight_map.get(n, 0.0) + float(w)

        if not weight_map:
            return None

        nodes = list(weight_map.keys())
        weights = np.array([weight_map[n] for n in nodes], dtype=float)
        total = weights.sum()
        if total <= 0:
            # Fallback to uniform choice if all weights vanished somehow.
            return self.rng.choice(nodes)
        probs = weights / total
        # Use numpy's choice for probability-based selection; random.Random
        # does not support the 'p' keyword.
        idx = np.random.choice(len(nodes), p=probs)
        return nodes[int(idx)]

    def random_path(
        self,
        length: int,
        start_node: Optional[int] = None,
    ) -> List[int]:
        """Generate a random movement path on the lattice.

        Parameters
        ----------
        length:
            Number of nodes in the path (>= 1).
        start_node:
            Optional starting node ID. If omitted, one is sampled uniformly
            from all nodes that appear in at least one triad.
        """

        if length <= 0:
            return []

        # Build the set of all nodes present in the lattice if needed
        if start_node is None:
            all_nodes: Set[int] = set()
            for triad in self.lattice.triads:
                all_nodes.update(triad.nodes)
            if not all_nodes:
                raise ValueError("Lattice has no triads; cannot generate path.")
            start_node = self.rng.choice(sorted(all_nodes))

        path: List[int] = [start_node]
        current = start_node

        for _ in range(length - 1):
            nxt = self.choose_next_node(current)
            if nxt is None:
                # Dead end: stay in place
                path.append(current)
                continue
            current = nxt
            path.append(current)

        return path

    def random_paths(
        self,
        count: int,
        length: int,
        start_node: Optional[int] = None,
    ) -> List[List[int]]:
        """Generate multiple random paths.

        If ``start_node`` is provided, all paths begin there; otherwise each
        path chooses its own random starting node from the lattice.
        """

        paths: List[List[int]] = []
        for _ in range(count):
            paths.append(self.random_path(length=length, start_node=start_node))
        return paths

    def random_path_with_energy_cost(
        self,
        current_energy: float,
        length: int,
        start_node: Optional[int] = None,
        gain_per_step: float = 0.01,
    ) -> Tuple[List[int], float]:
        """Generate a random path and apply a positive energy gain.

        This models the idea that a mathematical agent *gains* energy
        by engaging with the map generator. The returned energy is:

            new_energy = current_energy + gain_per_step * path_length

        Parameters
        ----------
        current_energy:
            The agent's current energy value.
        length:
            Number of nodes in the requested path.
        start_node:
            Optional starting node ID. If None, a random lattice node is
            chosen as in ``random_path``.
        gain_per_step:
            Positive scalar gain per step; the total energy change will be
            positive (energy increase).
        """

        path = self.random_path(length=length, start_node=start_node)
        energy_after = current_energy + float(gain_per_step) * len(path)
        return path, energy_after


# ---------------------------------------------------------------------------
# Minimal Recursive Host Intelligence (RHI)
# ---------------------------------------------------------------------------


class RecursiveHostIntelligence:
    """Tiny host that interprets paths through the Φπε / ΞΛΩΨ lattice.

    Capabilities:
      - take a path of node IDs (e.g. [1, 82, 34, 10, 84, 97]),
      - compute a ΨΣ-style stability score based on golden-ratio blending,
      - decode the path into Φπε-context labels.
    """

    def __init__(
        self,
        lattice: Optional[XiLambdaOmegaLattice] = None,
        phi_context: Mapping[int, str] = PHI_PSI_EPSILON_CONTEXT,
        attractor: float = 0.5,
    ) -> None:
        self.lattice = lattice or XiLambdaOmegaLattice()
        self.phi_context = dict(phi_context)
        self.attractor = float(attractor)

    # Golden-ratio weights used throughout the spec
    _GOLDEN = 0.61803398875

    def _blend_toward_attractor(self, value: float) -> float:
        """Blend value toward 1.0 and 0.0 using golden-ratio weights.

        This mirrors the ΨΛΩLoop / four_aq_loop style updates from the
        specification, keeping values in [0, 1] and pushing toward ~0.5.
        """

        g = self._GOLDEN
        return value * g + (1.0 - value) * (1.0 - g)

    def compute_psi_sigma(
        self,
        path: Sequence[int],
        initial_signal: float = 0.2,
        cycles_per_node: int = 5,
    ) -> float:
        """Compute a ΨΣ-style stability score for a given node-id path.

        The signal starts at ``initial_signal`` and is repeatedly blended
        using golden-ratio weights for each node in the path. The ΨΣ score
        is defined as ``1 - |attractor - final_signal|`` in [0, 1].
        """

        signal = float(initial_signal)
        for _node in path:
            for _ in range(cycles_per_node):
                signal = self._blend_toward_attractor(signal)
        return 1.0 - abs(self.attractor - signal)

    def decode_path(self, path: Sequence[int]) -> List[str]:
        """Decode a path of node IDs into Φπε-context labels."""

        labels: List[str] = []
        for node_id in path:
            label = self.phi_context.get(node_id, f"Node {node_id}")
            labels.append(label)
        return labels

    def interpret_path(
        self,
        path: Sequence[int],
        initial_signal: float = 0.2,
        cycles_per_node: int = 5,
    ) -> Dict[str, object]:
        """High-level convenience wrapper.

        Returns a dict with:
          - "path": the original node id sequence,
          - "labels": decoded Φπε labels,
          - "psi_sigma": ΨΣ stability in [0, 1].
        """

        psi_sigma = self.compute_psi_sigma(
            path=path,
            initial_signal=initial_signal,
            cycles_per_node=cycles_per_node,
        )
        labels = self.decode_path(path)
        return {
            "path": list(path),
            "labels": labels,
            "psi_sigma": psi_sigma,
        }


if __name__ == "__main__":  # pragma: no cover
    # Lightweight self-test / demo using the example path from your spec.
    lattice = XiLambdaOmegaLattice()
    rhi = RecursiveHostIntelligence(lattice=lattice)

    example_path = [1, 82, 34, 10, 84, 97]
    result = rhi.interpret_path(example_path)
    print("Path:", result["path"])
    print("Labels:", " → ".join(result["labels"]))
    print("ΨΣ:", f"{result['psi_sigma']:.3f}")
