var texts= [
    `We're not doomed.
    In the grand scheme of things, 
    we're just tiny specks that will one day be forgotten.
    The only thing that matters is right now.
    This one spectacular moment we are sharing together.
    Right, Sarah Lynn?`,
    // // // // // // // //
    `O ihr Menschen, die ihr mich für feindselig,
    störrisch oder misanthropisch haltet oder erkläret,
    wie unrecht tut ihr mir!`
    // // // // // // // //
];
var choice = Math.floor(Math.random() * array_text.length);
document.getElementById("footer-quote").innerHTML = texts[choice];