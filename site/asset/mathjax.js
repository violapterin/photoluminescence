window.MathJax = {
   loader: {
      load: ['input/tex', 'output/chtml'],
   },
   tex: {
      inlineMath: [['\\(', '\\)']],
      displayMath: [['\\[', '\\]']],
      packages: {
         '[+]': ['ams'],
         '[+]': ['unicode'],
         '[+]': ['color'],
      },
   },
   chtml: {
      scale: 0.92,
   },
   options: {
      processHtmlClass: [
         "math-letter", "math-sign", "math-plain",
         "math-bracket-round", "math-bracket-square", "math-bracket-curly",
         "math-bracket-angle", "math-bracket-line",
         "math-pair", "math-triplet", "math-tuple",
         "math-serif", "math-sans", "math-mono", "math-void",
      ],
      ignoreHtmlClass: ["body"],
   },
};
