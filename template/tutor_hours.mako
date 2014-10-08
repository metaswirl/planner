% vim:ft=tex:
% document/font type
\documentclass[a4paper,smallheadings]{scrartcl}

% enable mutated vowls
\usepackage[utf8]{inputenc}

% vector fonts
\usepackage[T1]{fontenc}

% break up syllables
\usepackage[english,ngerman]{babel}

\newcommand{\Author}{MPGI1: Einführung in die Programmierung}
\newcommand{\Title}{C-Kurs Einsatzplan}
\newcommand{\note}[1]{\marginnote{\textit{\textbf{#1}} }}
\newcommand{\corr}[2]{\marginnote{\textcolor{red}{#1} }}

\begin{document}
\title{\Title}
\author{\Author}
\date{}
\maketitle
\thispagestyle{empty}
\begin{table}[h!]
    \centering
    \begin{tabular}{ll}
        \textbf{Vorname} & Erika\\
        \textbf{Name} & Mustermann\\
        \textbf{Rolle} & Tutor\\
        \textbf{Stundenanzahl} & 60\\
    \end{tabular}
\end{table}
\vspace{1cm}

\begin{tabular}{lllllll}
    \textbf{Tag} & \textbf{Datum} & \textbf{Von} & \textbf{Bis} & \textbf{Raum} &
    \textbf{Art} & \textbf{Kontakt}\\\hline
    Dienstag & 10.10.2014 & 10 & 12 & MAR 4.0029 & Tutorium & Niklas\\
\end{tabular}

\end{document}
