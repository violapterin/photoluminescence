window.MathJax = {
  jax: {
    load: ["input/tex", "output/chtml"]
  },
  tex2jax: {
    packages: {
      '[+]': ['ams'],
      '[+]': ['unicode'],
      '[+]': ['color']
    },
    inlineMath: ['\\(', '\\)'],
    displayMath: ['\\[', '\\]']
  },
  SVG: {
    scale: 1.2,
    font: "STIX-Web"
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