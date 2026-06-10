#!/bin/bash
# Build proposal_damsa_at_sns.pdf (requires pandoc and typst; any font works)
set -e
cd "$(dirname "$0")"
cp ../study/damsa_at_sns.png /tmp/damsa_at_sns_fig.png
sed 's|\.\./study/damsa_at_sns\.png|damsa_at_sns_fig.png|' proposal_damsa_at_sns.md > /tmp/proposal_build.md
(cd /tmp && pandoc proposal_build.md -f markdown-subscript-superscript --wrap=none \
  -o "$OLDPWD/proposal_damsa_at_sns.pdf" --pdf-engine=typst \
  -V mainfont="DejaVu Serif" -V margin-x=2.2cm -V margin-y=2.2cm -V fontsize=10pt)
