\documentclass[a4paper,smallheadings]{scrartcl}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
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
        \textbf{Name} & ${person.name}\\
        \textbf{Rolle} & ${person.job}\\
        \textbf{Stundenanzahl} & ${person.hours}\\
    \end{tabular}
\end{table}
\vspace{1cm}

\begin{tabular}{lllllll}
    \textbf{Tag} & \textbf{Datum} & \textbf{Von} & \textbf{Bis} & \textbf{Raum} &
    \textbf{Art} & \textbf{Kontakt}\\\hline
% for s in schedule.sort_by_date():
    ${s.weekday} & ${s.day} & ${s.start} & ${s.end} & ${s.room} & ${s.task} & ${s.contact}\\
% endfor
\end{tabular}

\end{document}
