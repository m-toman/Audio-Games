pyinstaller --distpath ../dist labyrinth.spec
pyinstaller --distpath ../dist memory.spec
svn export --force ../data ../dist/data
