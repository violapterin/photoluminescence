window.MathJax = {
  options: {
    processHtmlClass: "math",
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

