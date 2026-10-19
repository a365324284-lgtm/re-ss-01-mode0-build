from pathlib import Path
import sys

root = Path(sys.argv[1])
p = root / 'target/linux/qualcommax/dts/ipq6000-re-ss-01.dts'
s = p.read_text()
assert s.count('qcom,ath11k-fw-memory-mode = <1>;') == 1, 'Unexpected source; stop'
assert '#include "ipq6018-512m.dtsi"' in s
assert '&q6_region {' not in s, 'Existing override; review required'
s = s.replace('qcom,ath11k-fw-memory-mode = <1>;', 'qcom,ath11k-fw-memory-mode = <0>;')
s += '''
/* EXPERIMENTAL: restore upstream IPQ6018 85 MiB Q6 reservation for
 * Mode 0 evaluation. This does not prove firmware/hardware compatibility.
 * Override only this board; do not change other 512 MiB devices.
 */
&q6_region {
    reg = <0x0 0x4ab00000 0x0 0x5500000>;
};
'''
p.write_text(s)
print('Experimental board-only Mode 0 / 85 MiB Q6 override prepared')
