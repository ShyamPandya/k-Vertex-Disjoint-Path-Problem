%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Inspiration from : https://www.overleaf.com/learn/latex/How_to_write_a_LaTeX_class_file_and_design_your_own_CV_(Part_1)
% and: https://www.overleaf.com/learn/latex/How_to_write_a_LaTeX_class_file_and_design_your_own_CV_(Part_2)
% and lots of help from stackoverflow
%
% Modified further by: Akhil Ravipati
% LinkedIn: https://www.linkedin.com/in/akhilravipati/
% Approx. Initial Date: 01/17/2020
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\ProvidesClass{imports}[2020/04/01 Analysis of Algorithms 1]
\LoadClass[12pt]{article}
\RequirePackage[margin=1in]{geometry}
\RequirePackage{titlesec}
\RequirePackage{mathtools}
\RequirePackage{algorithmic}
\RequirePackage{listings}
\RequirePackage{enumitem}
\RequirePackage[hidelinks]{hyperref}
\RequirePackage{graphicx}
\RequirePackage{tikz}

\RequirePackage{xcolor}
\definecolor{magenta}{cmyk}{3, 100, 0, 0}
