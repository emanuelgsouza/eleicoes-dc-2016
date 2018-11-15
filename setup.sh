# Setup analysis to docs folder

# enter in analysis folder
cd analysis

# convert ipynb file to html file
$HOME/anaconda3/bin/jupyter nbconvert --to html eleicoes-dc-analysis.ipynb

$HOME/anaconda3/bin/jupyter nbconvert --to html geographic-analysis.ipynb

# move html file to docs folder
mv eleicoes-dc-analysis.html ../docs

mv geographic-analysis.html ../docs

# enter in docs folder
cd ../docs

# rename file to entry point
mv eleicoes-dc-analysis.html index.html

mv geographic-analysis.html geographic.html

# come in back to root folder
cd ..

# add index.html to staging (GIT)
git add docs/index.html

git add docs/geographic.html

# commit
git commit -m"update docs"

# push
git push
