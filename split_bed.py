import sys
from pathlib import Path

doc = f"""Usage: python {__file__} sorted.bed outdir prefix"""


def main(bed, outdir, prefix):
    outdir = Path(outdir).absolute()
    outdir.mkdir(parents=True, exist_ok=True)
    n = 1
    ends = {n: 0}
    contigs = {n: None}
    out = f"{outdir}/{prefix}.{n}.bed"
    outs = {n: open(out, "w")}
    with open(bed) as f:
        for line in f:
            contig, start, end = line.strip().split("\t")
            start = int(start)
            end = int(end)
            for i in range(1, n + 1):
                if start > ends[i] or contig != contigs[i]:
                    outs[i].write(line)
                    ends[i] = end
                    contigs[i] = contig
                    break
            else:
                n += 1
                out = f"{outdir}/{prefix}.{n}.bed"
                outs[n] = open(out, "w")
                outs[n].write(line)
                ends[n] = end
                contigs[n] = contig
    for n, out in outs.items():
        out.close()


if __name__ == "__main__":
    if len(sys.argv) not in [4, 5]:
        sys.exit(doc)
    else:
        main(*sys.argv[1:])
