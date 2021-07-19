var texts= [
   `Wherefore is light given to him that is in misery,<br>
   and life unto the bitter in soul;<br>
   Which long for death, but it cometh not;<br>
   and dig for it more than for hid treasures?`,
   // // // // // // // //
   `We're not doomed.
   In the grand scheme of things,
   we're just tiny specks that will one day be forgotten.
   The only thing that matters is right now.
   This one spectacular moment we are sharing together.
   Right, Sarah Lynn?`,
   // // // // // // // //
   `O ihr Menschen, die ihr mich für feindselig,
   störrisch oder misanthropisch haltet oder erkläret,
   wie unrecht tut ihr mir!`,
   // // // // // // // //
   `Fame is a bee.<br>
   It has a song—<br>
   It has a sting—<br>
   Ah, too, it has a wing.`,
   // // // // // // // //
   `Now—for a breath I tarry<br>
   Nor yet disperse apart—<br>
   Take my hand quick and tell me,<br>
   What have you in your heart.`,
   // // // // // // // //
];
var choice = Math.floor(Math.random() * texts.length);
document.getElementById("footer-quote").innerHTML = texts[choice];