MathJax = {
   loader: {
      load: ['input/tex', 'output/svg']
   },
   tex: {
      inlineMath: [['\\(', '\\)']],
      displayMath: [['\\[', '\\]']],
      packages: {
         '[+]': ['ams'],
         '[+]': ['unicode'],
         '[+]': ['color']
      },
   },
   svg: {
      fontCache: 'local',
      scale: 1
   },
   options: {
      processHtmlClass: [
         "math-letter", "math-sign", "math-plain",
         "math-bracket-round", "math-bracket-square", "math-bracket-curly",
         "math-bracket-angle", "math-bracket-line",
         "math-pair", "math-triplet", "math-tuple",
         "math-serif", "math-sans", "math-mono",
      ],
      ignoreHtmlClass: "body"
   }
};

/*
MathJax = {
   loader: {
      load: ['input/tex', 'output/svg']
   },
   tex: {
      packages: {
         '[+]': ['ams'],
         '[+]': ['unicode'],
         '[+]': ['color']
      },
      inlineMath: ['\\(', '\\)'],
      displayMath: ['\\[', '\\]']
   },
   options: {
      processHtmlClass: [
         "math-letter", "math-sign", "math-plain",
         "math-bracket-round", "math-bracket-square", "math-bracket-curly",
         "math-bracket-angle", "math-bracket-line",
         "math-pair", "math-triplet", "math-tuple",
         "math-serif", "math-sans", "math-mono",
      ],
      ignoreHtmlClass: "body"
  }
};
*/