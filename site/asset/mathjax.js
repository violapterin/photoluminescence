window.MathJax = {
  options: {
    processHtmlClass: [
      "math-letter", "math-sign", "math-plain",
      "math-bracket-round", "math-bracket-square", "math-bracket-curly",
      "math-bracket-angle", "math-bracket-line",
      "math-pair", "math-triplet", "math-tuple",
      "math-serif", "math-sans", "math-mono",
      "math"
    ],
    ignoreHtmlClass: "body"
  },
  loader: {
    load: ["input/tex", "output/chtml"]
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
  svg: {
    scale: 1.2,
    font: "STIX-Web"
  }
};

