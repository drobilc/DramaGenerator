\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{drama}[2020/09/25 Drama]

% The default font size is 11pt, but user can change it to 10 or 12 pt
\def\@points{11pt}
\DeclareOption{10pt}{\def\@points{10pt}}
\DeclareOption{12pt}{\def\@points{12pt}}

% Pass all other options to article document class
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}

\ProcessOptions\relax

% Acutally load article class
\LoadClass[\@points]{article}

%------------------------------------------------------------------------(end)
%                             Required packages
%-----------------------------------------------------------------------(fold)
\RequirePackage{fontspec}
\RequirePackage{geometry}

%------------------------------------------------------------------------(end)
%                             Document geometry
%-----------------------------------------------------------------------(fold)
\geometry{a4paper}

% Paragraphs should not be indented
\parindent 0em

%------------------------------------------------------------------------(end)
%                         Beginning of the document
%-----------------------------------------------------------------------(fold)
\AtBeginDocument{
  \setmainfont{GentiumBasic}
  
  \newcounter{scene}
  \setcounter{scene}{1}
  
  \newcounter{act}
  \setcounter{act}{1}
}

%------------------------------------------------------------------------(end)
%                       Commands for drama generation
%-----------------------------------------------------------------------(fold)
\newcommand{\TitlePage}[2]{
  \clearpage %

  \begin{titlepage}
    \begin{center}

      \vspace*{\fill}

      % Drama title
      { \Huge \textbf{#1} }

      \vspace{1em}

      % Drama authors
      { #2 }

      \vspace*{\fill}

    \end{center}
  \end{titlepage}
}

\newcommand{\DramaLine}[2]{
  \noindent
  \makebox[.2 \linewidth][l]{#1:}
  \hspace{.05 \linewidth}
  \parbox[t]{.7 \linewidth}{#2}
  \newline
}

\newcommand{\Line}[2]{
  \DramaLine{\textbf{#1}}{#2}
}

\newcommand{\LineWithDelivery}[3]{
  \DramaLine{\textbf{#1} \textit{(#2)}}{#3}
}

\newcommand{\Delivery}[1]{
  (\textit{#1})
}

\newcommand{\Aside}[2]{
  \textit{\textbf{#1} #2}
}

\newcommand{\Act}[1]{
  \pagebreak

  \begin{center}
    \Huge
    \textbf{ACT \Roman{act}} \\
    \Large
    (#1)
  \end{center}

  \stepcounter{act}
  \setcounter{scene}{1}
}

\newcommand{\Scene}[0]{
  \pagebreak

  \begin{center}

    \Large

    SCENE \arabic{scene}

    \vspace{11pt}

    \hrule

  \end{center}

  \vspace{24pt}

  \stepcounter{scene}
}