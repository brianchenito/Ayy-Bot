# Ayy-Bot
A reddit bot that replies to posts containing "ayy" with a syntactically parralel "lmao", if a "lmao" is not detected in replies.


known bugs: 


1. nonstandard exit of lmaoCheck() when evaluating comments under rare circumstances: occurs most consistly with superscript or hotlink "ayy"s. 

2. too many "o"s in replies to comments that have words following the "ayy" that contain "y". In practice, many of these comments probably shouldn't actually be replied to, as the "ayy"s are often used in the same way "hey" would be. Considering rework of ayyCheck() to exclude these comments.

