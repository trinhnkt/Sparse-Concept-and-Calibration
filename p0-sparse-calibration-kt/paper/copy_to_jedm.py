import os
import shutil

def main():
    root = r"c:\TRINH\P0\p0-sparse-calibration-kt"
    src_dir = os.path.join(root, "paper")
    dest_dir = os.path.join(root, "jedm_upload_folder")
    
    # 1. Create target directories
    os.makedirs(dest_dir, exist_ok=True)
    
    subdirs = ["sections", "tables", "figures", "appendix"]
    for subdir in subdirs:
        src_sub = os.path.join(src_dir, subdir)
        dest_sub = os.path.join(dest_dir, subdir)
        if os.path.exists(src_sub):
            shutil.copytree(src_sub, dest_sub, dirs_exist_ok=True)
            print(f"Copied directory: {src_sub} -> {dest_sub}")
            
    # 2. Copy ref files
    ref_files = ["references.bib", "references.bbl"]
    for ref_file in ref_files:
        src_f = os.path.join(src_dir, ref_file)
        dest_f = os.path.join(dest_dir, ref_file)
        if os.path.exists(src_f):
            shutil.copy2(src_f, dest_f)
            print(f"Copied file: {src_f} -> {dest_f}")
            
    # 3. Create jedm.cls content
    jedm_cls_content = """%%
%% This is file `jedm.cls', a modified version of 'article.cls'
%% generated with the docstrip utility.
%%
%% The original source files were:
%%
%% classes.dtx  (with options: `article')
%% 
%% Copyright 1993 1994 1995 1996 1997 1998 1999 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009
%% The LaTeX3 Project and any individual authors listed elsewhere
%% in this file.
%% 
%% This file was generated from file(s) of the LaTeX base system.
%% --------------------------------------------------------------
%% 
%% It may be distributed and/or modified under the
%% conditions of the LaTeX Project Public License, either version 1.3c
%% of this license or (at your option) any later version.
%% The latest version of this license is in
%%    http://www.latex-project.org/lppl.txt
%% and version 1.3c or later is part of all distributions of LaTeX
%% version 2005/12/01 or later.
%% 
%% This file has the LPPL maintenance status "maintained".
%% 
%% This file may only be distributed together with a copy of the LaTeX
%% base system. You may however distribute the LaTeX base system without
%% such generated files.
%% 
%% The list of all files belonging to the LaTeX base distribution is
%% given in the file `manifest.txt'. See also `legal.txt' for additional
%% information.
%% 
%% The list of derived (unpacked) files belonging to the distribution
%% and covered by LPPL is defined by the unpacking scripts (with
%% extension .ins) which are part of the distribution.
\\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\\RequirePackage{times}
\\PassOptionsToPackage{left=2.75cm,right=2.75cm,top=2.25cm,bottom=2.25cm}{geometry}
\\ProvidesClass{jedm}
              [2013/09/10 v1.0
 Standard LaTeX document class]

\\newcommand\\@ptsize{}
\\newif\\if@restonecol
\\newif\\if@titlepage
\\@titlepagefalse
\\if@compatibility\\else
\\DeclareOption{a4paper}
   {\\setlength\\paperheight {297mm}%
    \\setlength\\paperwidth  {210mm}}
\\DeclareOption{a5paper}
   {\\setlength\\paperheight {210mm}%
    \\setlength\\paperwidth  {148mm}}
\\DeclareOption{b5paper}
   {\\setlength\\paperheight {250mm}%
    \\setlength\\paperwidth  {176mm}}
\\DeclareOption{letterpaper}
   {\\setlength\\paperheight {11in}%
    \\setlength\\paperwidth  {8.5in}}
\\DeclareOption{legalpaper}
   {\\setlength\\paperheight {14in}%
    \\setlength\\paperwidth  {8.5in}}
\\DeclareOption{executivepaper}
   {\\setlength\\paperheight {10.5in}%
    \\setlength\\paperwidth  {7.25in}}
\\DeclareOption{landscape}
   {\\setlength\\@tempdima   {\\paperheight}%
    \\setlength\\paperheight {\\paperwidth}%
    \\setlength\\paperwidth  {\\@tempdima}}
\\fi
\\if@compatibility
  \\renewcommand\\@ptsize{0}
\\else
\\DeclareOption{10pt}{\\renewcommand\\@ptsize{0}}
\\fi
\\DeclareOption{11pt}{\\renewcommand\\@ptsize{1}}
\\DeclareOption{12pt}{\\renewcommand\\@ptsize{2}}
\\if@compatibility\\else
\\DeclareOption{oneside}{\\@twosidefalse \\@mparswitchfalse}
\\fi
\\DeclareOption{twoside}{\\@twosidetrue  \\@mparswitchtrue}
\\DeclareOption{draft}{\\setlength\\overfullrule{5pt}}
\\if@compatibility\\else
\\DeclareOption{final}{\\setlength\\overfullrule{0pt}}
\\fi
\\DeclareOption{titlepage}{\\@titlepagetrue}
\\if@compatibility\\else
\\DeclareOption{notitlepage}{\\@titlepagefalse}
\\fi
\\if@compatibility\\else
\\DeclareOption{onecolumn}{\\@twocolumnfalse}
\\fi
\\DeclareOption{twocolumn}{\\@twocolumntrue}
\\DeclareOption{leqno}{\\input{leqno.clo}}
\\DeclareOption{fleqn}{\\input{fleqn.clo}}
\\DeclareOption{openbib}{%
  \\AtEndOfPackage{%
   \\renewcommand\\@openbib@code{%
      \\advance\\leftmargin\\bibindent
      \\itemindent -\\bibindent
      \\listparindent \\itemindent
      \\parsep \\z@
      }%
   \\renewcommand\\newblock{\\par}}%
}
\\ExecuteOptions{letterpaper,12pt,oneside,onecolumn,final}
\\ProcessOptions
\\input{size1\\@ptsize.clo}
\\setlength\\lineskip{1\\p@}
\\setlength\\normallineskip{1\\p@}
\\renewcommand\\baselinestretch{1.0}
\\setlength\\parskip{0\\p@ \\@plus \\p@}
\\@lowpenalty   51
\\@medpenalty  151
\\@highpenalty 301
\\setcounter{topnumber}{2}
\\renewcommand\\topfraction{.7}
\\setcounter{bottomnumber}{1}
\\renewcommand\\bottomfraction{.3}
\\setcounter{totalnumber}{3}
\\renewcommand\\textfraction{.2}
\\renewcommand\\floatpagefraction{.5}
\\setcounter{dbltopnumber}{2}
\\renewcommand\\dbltopfraction{.7}
\\renewcommand\\dblfloatpagefraction{.5}
\\if@twoside
  \\def\\ps@headings{%
      \\let\\@oddfoot\\@empty\\let\\@evenfoot\\@empty
      \\def\\@evenhead{\\thepage\\hfil\\slshape\\leftmark}%
      \\def\\@oddhead{{\\slshape\\rightmark}\\hfil\\thepage}%
      \\let\\@mkboth\\markboth
    \\def\\sectionmark##1{%
      \\markboth {\\MakeUppercase{%
        \\ifnum \\c@secnumdepth >\\z@
          \\thesection\\quad
        \\fi
        ##1}}{}}%
    \\def\\subsectionmark##1{%
      \\markright {%
        \\ifnum \\c@secnumdepth >\\@ne
          \\thesubsection\\quad
        \\fi
        ##1}}}
\\else
  \\def\\ps@headings{%
    \\let\\@oddfoot\\@empty
    \\def\\@oddhead{{\\slshape\\rightmark}\\hfil\\thepage}%
    \\let\\@mkboth\\markboth
    \\def\\sectionmark##1{%
      \\markright {\\MakeUppercase{%
        \\ifnum \\c@secnumdepth >\\m@ne
          \\thesection\\quad
        \\fi
        ##1}}}}
\\fi
\\def\\ps@myheadings{%
    \\let\\@oddfoot\\@empty\\let\\@evenfoot\\@empty
    \\def\\@evenhead{\\thepage\\hfil\\slshape\\leftmark}%
    \\def\\@oddhead{{\\slshape\\rightmark}\\hfil\\thepage}%
    \\let\\@mkboth\\@gobbletwo
    \\let\\sectionmark\\@gobble
    \\let\\subsectionmark\\@gobble
    }
  \\if@titlepage
  \\newcommand\\maketitle{\\begin{titlepage}%
  \\let\\footnotesize\\small
  \\let\\footnoterule\\relax
  \\let \\footnote \\thanks
  \\null\\vfil
  \\vskip 60\\p@
    {\\LARGE\\sf\\raggedright\\noindent \\@title \\par}%
    \\vskip 3em%
    {\\large
     \\lineskip .75em%
     \\noindent%
     \\begin{tabular}[t]{l}%
       \\@author
     \\end{tabular}\\par}%
    \\vfil\\null
  \\end{titlepage}%
  \\setcounter{footnote}{0}%
  \\global\\let\\thanks\\relax
  \\global\\let\\maketitle\\relax
  \\global\\let\\@author\\@empty
  \\global\\let\\@date\\@empty
  \\global\\let\\@title\\@empty
  \\global\\let\\title\\relax
  \\global\\let\\author\\relax
  \\global\\let\\date\\relax
  \\global\\let\\and\\relax
}
\\else
\\newcommand\\maketitle{\\par
  \\begingroup
    \\renewcommand\\thefootnote{\\@fnsymbol\\c@footnote}%
    \\def\\@makefnmark{\\rlap{\\@textsuperscript{\\normalfont\\@thefnmark}}}%
    \\long\\def\\@makefntext##1{\\parindent 1em\\noindent
            \\hb@xt@1.8em{%
                \\hss\\@textsuperscript{\\normalfont\\@thefnmark}}##1}%
    \\if@twocolumn
      \\ifnum \\col@number=\\@ne
        \\@maketitle
      \\else
        \\twocolumn[\\@maketitle]%
      \\fi
    \\else
      \\newpage
      \\global\\@topnum\\z@   % Prevents figures from going at top of page.
      \\@maketitle
    \\fi
    \\thispagestyle{plain}%
    \\@thanks
  \\endgroup
  \\setcounter{footnote}{0}%
  \\global\\let\\thanks\\relax
  \\global\\let\\maketitle\\relax
  \\global\\let\\@maketitle\\relax
  \\global\\let\\@thanks\\@empty
  \\global\\let\\@author\\@empty
  \\global\\let\\@date\\@empty
  \\global\\let\\@title\\@empty
  \\global\\let\\title\\relax
  \\global\\let\\author\\relax
  \\global\\let\\date\\relax
  \\global\\let\\and\\relax
}
\\def\\@maketitle{%
  \\newpage
  \\null
  \\vskip 2em%
  \\begin{center}%
  \\let\\footnote\\thanks
    {\\LARGE \\@title \\par}%
    \\vskip 1.5em%
    {\\large
      \\lineskip .5em%
      \\begin{tabular}[t]{c}%
        \\@author
      \\end{tabular}\\par}%
    \\vskip 1em%
    {\\large \\@date}%
  \\end{center}%
  \\par
  \\vskip 1.5em}
\\fi
\\if@compatibility
\\else
\\renewenvironment{abstract}{%
      \\if@twocolumn
        \\section*{Abstract}%
      \\else
        \\small
        \\begin{center}%
          {\\bfseries\\sffamily Abstract\\vspace{-.5em}\\vspace{\\z@}}%
        \\end{center}%
        \\quotation
      \\fi}
      {\\if@twocolumn\\else\\endquotation\\fi}
\\fi

\\input{size12.clo}
\\endinput
"""
    with open(os.path.join(dest_dir, "jedm.cls"), "w", encoding="utf-8") as f:
        f.write(jedm_cls_content)
    print("Created jedm.cls")

if __name__ == "__main__":
    main()
