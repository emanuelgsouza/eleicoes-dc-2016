# Setup analysis to docs folder

# enter in analysis folder
cd analysis

# convert ipynb file to html file
$HOME/anaconda3/bin/jupyter nbconvert --to html eleicoes-dc-analysis.ipynb

# move html file to docs folder
mv eleicoes-dc-analysis.html ../docs

# enter in docs folder
cd ../docs

# rename file to entry point
mv eleicoes-dc-analysis.html index.html
