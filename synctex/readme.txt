Source:
 http://ubuntuforums.org/showthread.php?t=1716268

A few corrections to make the scripts work:
 http://ubuntuforums.org/archive/index.php/t-1716268.html
 http://www.benwhale.com/blog/2012/09/06/evince-synctex-support-broke-for-me-today/


Software requirements:
 vim or gvim
 evince
 python2.7
 (vim-latexsuite)
 (screen)
 (urxvt)



Add the following code to ~/.vimrc if you don't want to depend on
vim-latexsuite. Else, use the original function for forward search described on
the first source
-------------------------------------------------------------------------------
" SyncTex forward search (Vim -> Evince)
function! SyncTex_ForwardSearch()
    let cmd = 'evince_forward_search ' . w:mainfile  . ' ' . line(".") . ' ' . expand("%:p")
    let output = system(cmd)
endfunction

" Shortcut for forward search (Vim -> Evince)
:nmap \ls :call SyncTex_ForwardSearch()<CR>
-------------------------------------------------------------------------------



If you wanted to use vim-latexsuite, the code below can be added to
~/.vim/after/ftplugin/tex.vim
However, it requires you to somehow set the main filename so that
Tex_GetMainFileName points to the correct pdf file. Else, it assumes that there
exists a pdf file with the same name as the file invoke forward substitute from.
-------------------------------------------------------------------------------
function! Tex_ForwardSearchLaTeX()
  let cmd = 'evince_forward_search ' . fnamemodify(Tex_GetMainFileName(), ":p:r") .  '.pdf ' . line(".") . ' ' . expand("%:p")
  let output = system(cmd)
endfunction
-------------------------------------------------------------------------------



Move the following scripts to a directory within $PATH - fx. /usr/local/bin/
 evince-sync
 evince_forward_search
 evince_backward_search



Add the code below to your makefile. If you're not using urxvt, simply change
the code to use your favorite terminal emulator. If you use another terminal
emulator, you may also have to change the flag '-e' to '-x' or even something
else.
The variable $(MAIN) in the code below is supposed to be the filename of the
pdf file that is generated 
-------------------------------------------------------------------------------
MAIN = main
SYNCTEX_PDFREADER = evince-sync

sopen: $(MAIN).pdf
	@echo ""
	@echo "Opening $(MAIN).pdf"
	(urxvt -e vim --servername $(MAIN) -c "let w:mainfile='$(CURDIR)/$(MAIN).pdf'" &) &>/dev/null
	screen -d -m ${SYNCTEX_PDFREADER} $(MAIN).pdf
-------------------------------------------------------------------------------


Finally, we have to make sure we compile with synctex. Do this by adding the
code below to your preamble.tex file and add the synctex compile flag when
when compiling with pdflatex or any other latex compiler. It may not be
necessary to add any flags if compiling with rubber (maybe i have added the
flag to pdflatex somewhere that i'm not aware of)
-------------------------------------------------------------------------------
\synctex=1
-------------------------------------------------------------------------------


Now, if you are using the makefile code, simply type 'make sopen' in the
terminal and a vim and evince session will be started.
Clicking 'Ctrl+leftclick' on some text in evince will open the source file in
the vim session.
Typing '\ls' in a tex file in vim will make evince navigate to the corresponding text in
the pdf file.

