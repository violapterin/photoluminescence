const texts= [
   `Wherefore is light given to him that is in misery,<br>
   and life unto the bitter in soul;<br>
   Which long for death, but it cometh not;<br>
   and dig for it more than for hid treasures?`,
   // // // // // // // //
   `&emsp;And why beholdest thou the mote that is<br>
   in thy brother’s eye, but considerest not the<br>
   beam that is in thine own eye?`,
   // // // // // // // //
   `&emsp;&emsp;Love seeketh only self to please,<br>
   &emsp;&emsp;To bind another to its delight,<br>
   &emsp;&emsp;Joys in another’s loss of ease,<br>
   &emsp;&emsp;And builds a Hell in Heaven’s despite.`,
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
   `&emsp;&emsp;Now—for a breath I tarry<br>
   &emsp;&emsp;Nor yet disperse apart—<br>
   &emsp;&emsp;Take my hand quick and tell me,<br>
   &emsp;&emsp;What have you in your heart.`,
   // // // // // // // //
   `&emsp;Things fall apart; the centre cannot hold;<br>
   &emsp;Mere anarchy is loosed upon the world.`,
   // // // // // // // //
   `&emsp;We’re not doomed. In the grand scheme<br>
   of things, we’re just tiny specks that will one<br>
   day be forgotten. The only thing that matters<br>
   is right now. This one spectacular moment we<br>
   are sharing together. Right, Sarah Lynn?`,
   // // // // // // // //
];
var choice = Math.floor(Math.random() * texts.length);
document.getElementById("footer-quote").innerHTML = texts[choice];