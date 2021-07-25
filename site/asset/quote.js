const texts= [
   `Wherefore is light given to him that is in misery,<br>
   and life unto the bitter in soul;<br>
   Which long for death, but it cometh not;<br>
   and dig for it more than for hid treasures?`,
   // // // // // // // //
   `&emsp;We're not doomed. In the grand scheme of<br>
   things, we're just tiny specks that will one day<br>
   be forgotten. The only thing that matters is right<br>
   now. This one spectacular moment we are sharing<br>
   together. Right, Sarah Lynn?`,
   // // // // // // // //
   `&emsp;O ihr Menschen, die ihr mich für<br>
   feindselig, störrisch oder misanthropisch<br>
   haltet oder erkläret, wie unrecht tut ihr mir!`,
   // // // // // // // //
   `&emsp;&emsp;&emsp;&emsp;Fame is a bee.<br>
   &emsp;&emsp;&emsp;&emsp;It has a song—<br>
   &emsp;&emsp;&emsp;&emsp;It has a sting—<br>
   &emsp;&emsp;&emsp;&emsp;Ah, too, it has a wing.`,
   // // // // // // // //
   `&emsp;Things fall apart; the centre cannot hold;<br>
   &emsp;Mere anarchy is loosed upon the world.`,
   // // // // // // // //
   `&emsp;&emsp;Now—for a breath I tarry<br>
   &emsp;&emsp;Nor yet disperse apart—<br>
   &emsp;&emsp;Take my hand quick and tell me,<br>
   &emsp;&emsp;What have you in your heart.`,
   // // // // // // // //
];
var choice = Math.floor(Math.random() * texts.length);
document.getElementById("footer-quote").innerHTML = texts[choice];