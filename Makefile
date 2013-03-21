all: code.tar.gz all.tar.gz comp1.gif comp2.gif
	pdflatex ./tex/report.tex
	pdflatex ./tex/report.tex
	pdflatex ./tex/report.tex
	rm *.out *.log *.aux *.toc *.lof *.equ

code.tar.gz:
	tar -czvf code.tar.gz ./py ./mat2

all.tar.gz:
	tar -czvf all.tar.gz *

comp1.gif:
	convert -delay 10 -loop 0 ./img/comparray_1_* ./img/comp1.gif

comp2.gif:
	convert -delay 10 -loop 0 ./img/comparray_2_* ./img/comp2.gif
